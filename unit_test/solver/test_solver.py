"""Tests for warm starts and one-time singular-matrix recovery."""

import unittest
from unittest.mock import patch

import numpy as np
import scipy as sp

from omotes_simulator_core.solver.matrix.equation_object import EquationObject
from omotes_simulator_core.solver.matrix.matrix import SingularMatrixError
from omotes_simulator_core.solver.network.assets.base_asset import BaseAsset
from omotes_simulator_core.solver.network.assets.node import Node
from omotes_simulator_core.solver.network.network import Network
from omotes_simulator_core.solver.solver import Solver


class ScalarAsset(BaseAsset):
    def __init__(self) -> None:
        """Create a scalar equation with a configurable right-hand side."""
        super().__init__("scalar", "scalar", number_of_unknowns=1, number_connection_points=0)
        self.setpoint = 2.0
        self.singular_at: float | None = None
        self.guesses: list[float] = []

    def get_equations(self) -> list[EquationObject]:
        self.guesses.append(float(self.prev_sol[0]))
        equation = EquationObject()
        equation.indices = np.array([self.matrix_index])
        equation.coefficients = np.array([0.0 if self.prev_sol[0] == self.singular_at else 1.0])
        equation.rhs = self.setpoint
        return [equation]


class SolverTest(unittest.TestCase):
    def setUp(self) -> None:
        self.asset = ScalarAsset()
        self.network = Network()
        self.network.add_existing_asset(self.asset)
        self.solver = Solver(self.network)

    def test_warm_start_still_solves_current_setpoints(self) -> None:
        self.solver.solve()
        self.assertEqual(self.asset.guesses, [0.0, 2.0])
        self.asset.guesses.clear()
        self.solver.solve()
        self.assertEqual(self.asset.guesses, [2.0])
        self.asset.guesses.clear()
        self.asset.setpoint = -100.0
        self.solver.solve()
        self.assertEqual(self.asset.guesses, [2.0, -100.0])
        np.testing.assert_array_equal(self.solver.matrix.sol_new, [-100.0])

    def test_existing_estimates_are_used_without_validation_or_reset(self) -> None:
        self.solver.solve()
        self.asset.prev_sol[0] = 3.0
        self.asset.guesses.clear()
        with patch.object(self.network, "reset_prev_solution") as reset:
            with patch.object(self.solver.matrix, "reset_solution") as matrix_reset:
                self.solver.solve()
        self.assertEqual(self.asset.guesses, [3.0])
        reset.assert_not_called()
        matrix_reset.assert_not_called()

    def test_singularity_resets_matrix_assets_and_nodes_and_reassembles(self) -> None:
        node = Node(name="node", _id="node")
        self.network.nodes[node.name] = node
        self.solver = Solver(self.network)
        node_guesses = []

        def node_equations() -> list[EquationObject]:
            node_guesses.append(list(node.prev_sol))
            equations = []
            for index, value in enumerate((5.0, 6.0, 7.0)):
                equation = EquationObject()
                equation.indices = np.array([node.matrix_index + index])
                equation.coefficients = np.array([1.0])
                equation.rhs = value
                equations.append(equation)
            return equations

        original_solve = self.solver.matrix.solve
        matrix_guesses = []

        def solve_equations(equations: list[EquationObject], dump: bool = False) -> list[float]:
            matrix_guesses.append(self.solver.matrix.sol_new.copy())
            return original_solve(equations, dump=dump)

        with patch.object(node, "get_equations", side_effect=node_equations):
            self.solver.solve()
            self.asset.setpoint = 3.0
            self.asset.singular_at = 2.0
            self.asset.guesses.clear()
            node_guesses.clear()
            with (
                patch.object(self.solver.matrix, "solve", side_effect=solve_equations),
                patch.object(self.solver.matrix, "dump_matrix") as dump,
                patch.object(
                    self.solver.matrix, "reset_solution", wraps=self.solver.matrix.reset_solution
                ) as matrix_reset,
                patch.object(
                    self.network, "reset_prev_solution", wraps=self.network.reset_prev_solution
                ) as reset,
                patch.object(
                    self.solver, "results_to_assets", wraps=self.solver.results_to_assets
                ) as transfer,
                self.assertWarns(sp.sparse.linalg.MatrixRankWarning),
                self.assertLogs("omotes_simulator_core.solver.solver", level="WARNING") as logs,
            ):
                self.solver.solve()
        self.assertEqual(self.asset.guesses, [2.0, 0.0, 3.0])
        self.assertEqual(node_guesses, [[5.0, 6.0, 7.0], [0.0, 0.0, 0.0], [5.0, 6.0, 7.0]])
        np.testing.assert_array_equal(
            matrix_guesses, [[2.0, 5.0, 6.0, 7.0], [1.0, 1.0, 1.0, 1.0], [3.0, 5.0, 6.0, 7.0]]
        )
        np.testing.assert_array_equal(self.solver.matrix.sol_new, [3.0, 5.0, 6.0, 7.0])
        matrix_reset.assert_called_once()
        reset.assert_called_once()
        dump.assert_called_once()
        self.assertEqual(transfer.call_count, 2)
        self.assertEqual(len(logs.records), 1)
        self.assertIn("retrying once", logs.output[0])

    def test_second_singularity_propagates_without_another_retry(self) -> None:
        second_error = SingularMatrixError("second failure")
        with (
            patch.object(
                self.solver.matrix,
                "solve",
                side_effect=[SingularMatrixError("first failure"), second_error],
            ) as solve,
            patch.object(
                self.network, "reset_prev_solution", wraps=self.network.reset_prev_solution
            ) as reset,
            patch.object(
                self.solver.matrix, "reset_solution", wraps=self.solver.matrix.reset_solution
            ) as matrix_reset,
            patch.object(self.solver, "results_to_assets") as transfer,
            patch.object(self.solver.matrix, "is_converged") as converged,
            self.assertLogs("omotes_simulator_core.solver.solver", level="WARNING"),
            self.assertRaises(SingularMatrixError) as raised,
        ):
            self.solver.solve()
        self.assertIs(raised.exception, second_error)
        self.assertEqual(solve.call_count, 2)
        reset.assert_called_once()
        matrix_reset.assert_called_once()
        transfer.assert_not_called()
        converged.assert_not_called()

    def test_later_singularity_restarts_iteration_budget(self) -> None:
        original_solve = self.solver.matrix.solve
        calls = 0

        def solve_equations(equations: list[EquationObject], dump: bool = False) -> list[float]:
            nonlocal calls
            calls += 1
            if calls == 2:
                self.solver.matrix.sol_new[:] = np.nan
                raise SingularMatrixError("failed on second iteration")
            return original_solve(equations, dump=dump)

        with (
            patch.object(self.solver.matrix, "solve", side_effect=solve_equations),
            patch.object(self.solver, "_iteration_limit", 1),
            self.assertLogs("omotes_simulator_core.solver.solver", level="WARNING") as logs,
        ):
            self.solver.solve()
        self.assertEqual(calls, 4)
        self.assertEqual(self.asset.guesses, [0.0, 2.0, 0.0, 2.0])
        self.assertTrue(self.solver.matrix.is_converged())
        self.assertEqual(len(logs.records), 1)

    def test_each_solve_has_its_own_retry_allowance(self) -> None:
        self.solver.solve()
        for previous, target in ((2.0, 3.0), (3.0, 4.0)):
            with (
                self.subTest(previous=previous, target=target),
                patch.object(self.solver.matrix, "dump_matrix"),
                self.assertWarns(sp.sparse.linalg.MatrixRankWarning),
                self.assertLogs("omotes_simulator_core.solver.solver", level="WARNING"),
            ):
                self.asset.setpoint = target
                self.asset.singular_at = previous
                self.asset.guesses.clear()
                self.solver.solve()
                self.assertEqual(self.asset.guesses, [previous, 0.0, target])
                self.assertTrue(self.solver.matrix.is_converged())

    def test_unrelated_matrix_errors_are_not_retried(self) -> None:
        for error in (
            RuntimeError("other failure"),
            ValueError("invalid equations"),
            OSError("dump"),
        ):
            with (
                self.subTest(error=error),
                patch.object(self.solver.matrix, "solve", side_effect=error) as solve,
                patch.object(self.network, "reset_prev_solution") as reset,
                patch.object(self.solver.matrix, "reset_solution") as matrix_reset,
                self.assertRaises(type(error)) as raised,
            ):
                self.solver.solve()
            self.assertIs(raised.exception, error)
            solve.assert_called_once()
            reset.assert_not_called()
            matrix_reset.assert_not_called()

    def test_singular_exception_outside_matrix_solve_is_not_retried(self) -> None:
        for method in ("get_equations", "results_to_assets"):
            error = SingularMatrixError(method)
            with (
                self.subTest(method=method),
                patch.object(self.solver, method, side_effect=error) as operation,
                patch.object(self.network, "reset_prev_solution") as reset,
                patch.object(self.solver.matrix, "reset_solution") as matrix_reset,
                self.assertRaises(SingularMatrixError) as raised,
            ):
                self.solver.solve()
            self.assertIs(raised.exception, error)
            operation.assert_called_once()
            reset.assert_not_called()
            matrix_reset.assert_not_called()

    def test_iteration_limit_keeps_existing_warning_without_retry(self) -> None:
        with (
            patch.object(self.solver.matrix, "is_converged", return_value=False),
            patch.object(self.solver, "_iteration_limit", 0),
            patch.object(self.network, "reset_prev_solution") as reset,
            patch.object(self.solver.matrix, "reset_solution") as matrix_reset,
            self.assertLogs("omotes_simulator_core.solver.solver", level="WARNING") as logs,
        ):
            self.solver.solve()
        self.assertIn("No converged solution reached", logs.output[0])
        reset.assert_not_called()
        matrix_reset.assert_not_called()

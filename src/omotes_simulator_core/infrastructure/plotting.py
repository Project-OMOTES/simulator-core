#  Copyright (c) 2023. Deltares & TNO
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""Plot result on the map for debugging."""
import esdl
import geopandas as gpd
import numpy as np
import plotly.express as px
from numpy.typing import NDArray
from pandas import DataFrame
from shapely.geometry import LineString

from omotes_simulator_core.adapter.transforms.string_to_esdl import OmotesAssetLabels
from omotes_simulator_core.entities.assets.asset_defaults import (
    PROPERTY_MASSFLOW,
    PROPERTY_PRESSURE,
    PROPERTY_TEMPERATURE,
)
from omotes_simulator_core.entities.esdl_object import EsdlObject


class Plotting:
    """Plotting plot the results of asset (currently pipe) for inspection."""

    def __init__(self, esdl_object: EsdlObject) -> None:
        """Initialize plotting instance.

        :param EsdlObject esdl_object: esdl object of the network
        """
        self.esdl_object = esdl_object

    def simulation_output(self, result: DataFrame) -> None:
        """Function to plot the simulation results to the map.

        :param DataFrame result: simulation result in dataframe format
        """
        geo_df = self.prepare_data(result)
        Plotting.plot_line_mapbox(geo_df)

    def prepare_data(self, result: DataFrame) -> gpd.GeoDataFrame:
        """Function to prepare geopandas dataframe."""
        geo_df = gpd.GeoDataFrame(
            {},
            columns=[
                "asset_id",
                "asset_name",
                "geometry",
                "mass_flow",
                "pressure_in",
                "pressure_out",
                "temperature_in",
                "temperature_out",
            ],
            crs="EPSG:4326",
        )

        assets = self.esdl_object.get_all_assets_of_type(OmotesAssetLabels.PIPE)

        for asset_object in assets:
            asset = asset_object.esdl_asset
            if isinstance(asset.geometry, esdl.esdl.Line):
                coor_pipe = []
                for point in asset.geometry.point:
                    coor_pipe.append([point.lon, point.lat])

                last_data_index = len(result) - 1
                data = {
                    "asset_id": asset.id,
                    "asset_name": asset.name,
                    "geometry": LineString(coor_pipe),
                    "mass_flow": result[(asset_object.get_port_ids()[0], PROPERTY_MASSFLOW)][
                        last_data_index
                    ],
                    "pressure_in": result[(asset_object.get_port_ids()[0], PROPERTY_PRESSURE)][
                        last_data_index
                    ],
                    "pressure_out": result[(asset_object.get_port_ids()[1], PROPERTY_PRESSURE)][
                        last_data_index
                    ],
                    "temperature_in": result[
                        (asset_object.get_port_ids()[0], PROPERTY_TEMPERATURE)
                    ][last_data_index],
                    "temperature_out": result[
                        (asset_object.get_port_ids()[1], PROPERTY_TEMPERATURE)
                    ][last_data_index],
                }

                geo_df.loc[len(geo_df)] = data

        return geo_df

    @staticmethod
    def plot_line_mapbox(geo_df: gpd.GeoDataFrame, output_filename: str = "map.html") -> None:
        """Function to plot using plotly express line mapbox."""
        lats: NDArray = np.array(None)
        lons: NDArray = np.array(None)
        names: NDArray = np.array(None)
        for _, row in geo_df.iterrows():
            if isinstance(row["geometry"], LineString):
                linestrings = [row["geometry"]]
            else:
                continue
            for linestring in linestrings:
                x, y = linestring.xy
                lats = np.append(lats, y)
                lons = np.append(lons, x)

                text = (
                    row["asset_name"]
                    + ", mass_flow: "
                    + "{:.2f}".format(row["mass_flow"])
                    + " kg/s"
                    + ", Pin: "
                    + "{:.2f}".format(row["pressure_in"] / 1e5)
                    + " bar"
                    + ", Pout: "
                    + "{:.2f}".format(row["pressure_out"] / 1e5)
                    + " bar"
                    + ", Tin: "
                    + "{:.2f}".format(row["temperature_in"] - 273)
                    + " C"
                    + ", Tout: "
                    + "{:.2f}".format(row["temperature_out"] - 273)
                    + " C"
                )

                names = np.append(names, [text] * len(y))
                lats = np.append(lats, np.array(None))
                lons = np.append(lons, np.array(None))
                names = np.append(names, np.array(None))

        fig = px.line_mapbox(
            lat=lats, lon=lons, hover_name=names, zoom=14, mapbox_style="carto-positron"
        )
        fig.write_html(output_filename)

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
import plotly.express as px
import geopandas as gpd
import numpy as np
from shapely.geometry import LineString
from numpy.typing import NDArray
from simulator_core.entities.assets.asset_abstract import AssetAbstract


class Plotting:
    """Plotting plot the results of asset (currently pipe) for inspection."""

    @staticmethod
    def plot_map(assets: list[AssetAbstract]) -> None:
        """Static function to plot the simulation results to the map.

        :param assets: list collection of assets
        """
        geo_df = Plotting.prepare_data(assets)
        Plotting.plot_line_mapbox(geo_df)

    @staticmethod
    def prepare_data(assets: list[AssetAbstract]) -> gpd.GeoDataFrame:
        """Function to prepare geopandas dataframe."""
        geo_df = gpd.GeoDataFrame(
            columns=['asset_id', 'asset_name', 'geometry', 'mass_flow', 'pressure_in',
                     'pressure_out', 'temperature_in', 'temperature_out'], crs="EPSG:4326")

        for asset in assets:
            if isinstance(asset.geometry, esdl.esdl.Line):
                coor_pipe = []
                for point in asset.geometry.point:
                    coor_pipe.append([point.lon, point.lat])

                data = {'asset_id': asset.asset_id,
                        'asset_name': asset.name,
                        'geometry': LineString(coor_pipe),
                        'mass_flow': asset.output[-1]['mass_flow'],
                        'pressure_in': asset.output[-1]['pressure_supply'],
                        'pressure_out': asset.output[-1]['pressure_return'],
                        'temperature_in': asset.output[-1]['temperature_supply'],
                        'temperature_out': asset.output[-1]['temperature_return'],
                        }

                geo_df.loc[len(geo_df)] = data

        return geo_df

    @staticmethod
    def plot_line_mapbox(geo_df: gpd.GeoDataFrame) -> None:
        """Function to plot using plotly express line mapbox."""
        lats: NDArray = np.array(None)
        lons: NDArray = np.array(None)
        names: NDArray = np.array(None)
        for _, row in geo_df.iterrows():
            if isinstance(row['geometry'], LineString):
                linestrings = [row['geometry']]
            else:
                continue
            for linestring in linestrings:
                x, y = linestring.xy
                lats = np.append(lats, y)
                lons = np.append(lons, x)

                text = row['asset_name'] + \
                    ", mass_flow: " + "{:.2f}".format(row['mass_flow']) + " kg/s" + \
                    ", Pin: " + "{:.2f}".format(row['pressure_in'] / 1e5) + " bar" + \
                    ", Pout: " + "{:.2f}".format(row['pressure_out'] / 1e5) + " bar" + \
                    ", Tin: " + "{:.2f}".format(row['temperature_in'] - 273) + " C" + \
                    ", Tout: " + "{:.2f}".format(row['temperature_out'] - 273) + " C"

                names = np.append(names, [text] * len(y))
                lats = np.append(lats, np.array(None))
                lons = np.append(lons, np.array(None))
                names = np.append(names, np.array(None))

        fig = px.line_mapbox(lat=lats, lon=lons,
                             hover_name=names, zoom=14, mapbox_style="carto-positron")
        fig.show()

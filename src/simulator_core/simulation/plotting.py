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


class Plotting:
    """Plotting plot the results of asset (currently pipe) for inspection."""

    @staticmethod
    def plot_map(assets: list):
        """Static function to plot the simulation results to the map.

        :param assets: list collection of assets
        """
        # prepare list
        geometry = []
        asset_id = []
        asset_name = []
        mass_flow = []
        pressure_in = []
        pressure_out = []
        temperature_in = []
        temperature_out = []

        for asset in assets:
            if isinstance(asset.geometry, esdl.esdl.Line):
                coor_pipe = []
                for point in asset.geometry.point:
                    coor_pipe.append([point.lon, point.lat])

                geometry.append(LineString(coor_pipe))

                asset_name.append(asset.name)
                asset_id.append(asset.asset_id)
                mass_flow.append(asset.output[-1]['mass_flow'])
                temperature_in.append(asset.output[-1]['temperature_supply'])
                temperature_out.append(asset.output[-1]['temperature_return'])
                pressure_in.append(asset.output[-1]['pressure_supply'])
                pressure_out.append(asset.output[-1]['pressure_return'])

        # create geopanda instance
        data = {'asset_id': asset_id,
                'asset_name': asset_name,
                'geometry': geometry,
                'mass_flow': mass_flow,
                'pressure_in': pressure_in,
                'pressure_out': pressure_out,
                'temperature_in': temperature_in,
                'temperature_out': temperature_out,
                }
        geo_df = gpd.GeoDataFrame(data, crs="EPSG:4326")

        # plotting pipe properties
        lats = []
        lons = []
        names = []
        for ii in range(len(geo_df)):
            if isinstance(geo_df['geometry'][ii], LineString):
                linestrings = [geo_df['geometry'][ii]]
            else:
                continue
            for linestring in linestrings:
                x, y = linestring.xy
                lats = np.append(lats, y)
                lons = np.append(lons, x)

                text = geo_df['asset_name'][ii] + \
                    ", mass_flow: " + "{:.2f}".format(geo_df['mass_flow'][ii]) + " kg/s" + \
                    ", Pin: " + "{:.2f}".format(geo_df['pressure_in'][ii] / 1e5) + " bar" + \
                    ", Pout: " + "{:.2f}".format(geo_df['pressure_out'][ii] / 1e5) + " bar" + \
                    ", Tin: " + "{:.2f}".format(geo_df['temperature_in'][ii] - 273) + " C" + \
                    ", Tout: " + "{:.2f}".format(geo_df['temperature_out'][ii] - 273) + " C"

                names = np.append(names, [text] * len(y))
                lats = np.append(lats, None)
                lons = np.append(lons, None)
                names = np.append(names, None)

        fig = px.line_mapbox(lat=lats, lon=lons,
                             hover_name=names, zoom=14, mapbox_style="carto-positron")
        fig.show()

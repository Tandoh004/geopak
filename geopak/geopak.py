"""Main module."""

import ipyleaflet
from ipyleaflet import basemaps

class Map(ipyleaflet.Map):
    """_This ia a map class that is inherit from ipyleaflet.Map

    Args:
        ipyleaflet (_type_): The ipyleaflet.Map class
    """

    def __init__(self, center=[20, 0], zoom=2, **kwargs):
        """Initialize map
        Args:
            center (list, optional): Set the center of the map. Defaults to [20, 0].
            zoom (int, optional): Set the zoom level of the map. Defaults to 2.
        """
        super().__init__(center=center, zoom=zoom, **kwargs)
        
        self.layers_control = ipyleaflet.LayersControl(position='topright')
        self.add_control(self.layers_control)


    def add_tile_layer(self, url, name, **kwargs):
        """
        Add a tile layer to the map.

        Parameters:
        - url: The URL of the tile layer.
        - name: The name of the tile layer.
        - **kwargs: Additional options for the tile layer.
        """
        layer = ipyleaflet.TileLayer(url=url, name=name, **kwargs)
        self.add(layer)

    def add_basemap(self, name):
        """
        Add a basemap to the map.

        Parameters:
        - name: The name of the basemap. Should be a string or a basemap instance.
        """
        if isinstance(name, str):
            url = eval(f"basemaps.{name}").build_url()
            self.add_tile_layer(url, name)
            
        else:
            self.add(name)


    def add_geojson(self, data, name="geojson", **kwargs):
        """
        Args:
            data (_type_): _description_
            name (str, optional): _description_. Defaults to "geojson".
        """              
        import json

        if isinstance(data, str):
            with open(data) as f:
                data = json.load(f)
                
        if "style" not in kwargs:
            kwargs["style"] = {"color": "blue", "weight": 1, "fillOpacity":0}

        if "hover_style" not in kwargs:
            kwargs["hover_style"] = {"fillcolor": "#ff0000", "fillOpacity":0.5}

        layer = ipyleaflet.GeoJSON(data=data, name=name, **kwargs )
        self.add(layer)


    def add_shp(self, data, name="shp", **kwargs):
        """
        Args:
                data (str): Path to the shapefile (including .shp extension).
                name (str, optional): Name for the added GeoJSON data. Defaults to "shp".
                **kwargs: Additional keyword arguments passed to the `add_geojson` method.
       """
        import shapefile
                   
        import json

        if isinstance(data, str):
            with shapefile.Reader(data) as shp:
                data = shp.__geo_interface__
                
        self.add_geojson(data, name, **kwargs )

    

    
       
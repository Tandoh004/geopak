"""Main module."""

import ipyleaflet
from ipyleaflet import basemaps, WidgetControl
import ipywidgets as widgets 
from ipywidgets import ColorPicker


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
         
        self.toolbar = self.add_toolbar()
        self.cord = self.add_latlon()

                 
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
            data (_type_): Path to the geojson data (including .geojson extension)
            name (str, optional): Name for the added Geojson data. Defaults to "geojson".
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
                name (str, optional): Name for the added Shapefile data. Defaults to "shp".
                **kwargs: Additional keyword arguments passed to the `add_geojson` method.

         Raises:
            TypeError: If the data is neither a string nor a dictionary representing a shapefile.

        Returns:
            None     
       """
        import shapefile
        import json

        if isinstance(data, str):
            with shapefile.Reader(data) as shp:
                data = shp.__geo_interface__

        self.add_geojson(data, name, **kwargs)



    def add_raster(self, data, name="raster", zoom_to_layer=True, **kwargs):
        """Add a raster to the current map.

        Args:
            data (str or dict): Path to the raster as a string or a dictionary representation (including .Tif extension)
            name (str, optional): Name for the added Raster data. Defaults to "raster".
            zoom_to_layer (bool, optional): Whether to zoom to the added layer. Defaults to True.
            **kwargs: Additional keyword arguments to pass to the underlying functions.
        """

        try:
            from localtileserver import TileClient, get_leaflet_tile_layer
        except ImportError:
            raise ImportError("Please install the localtileserver package")

        client = TileClient(data)

        layer = get_leaflet_tile_layer(client, name=name, **kwargs)
        self.add(layer)

        if zoom_to_layer:
            self.center = client.center()
            self.zoom = client.default_zoom
    


    def add_image(self, url, bounds, name="image", **kwargs):
        """adds an image overlay to the map.

        Args:
            url (str): the url of the image
            bounds (list): the bounds of the image
            name (str, optional): the name of the layer. Defaults to "image".
        """
        
        layer = ipyleaflet.ImageOverlay(url=url, bounds=bounds, name="image", **kwargs)
        self.add(layer)
        

    def add_toolbar(self, position="topright"):
        """Adds a toolbar to the map.

        Args:
            position (str, optional): The position of the toolbar. Defaults to "topright".
        """

        padding = "0px 0px 0px 5px"  # upper, right, bottom, left

        toolbar_button = widgets.ToggleButton(
            value=False,
            tooltip="Toolbar",
            icon="wrench",
            button_style="success",
            layout=widgets.Layout(width="28px", height="28px", padding=padding),
        )

        close_button = widgets.ToggleButton(
            value=False,
            tooltip="Close the tool",
            icon="times",
            button_style="primary",
            layout=widgets.Layout(height="28px", width="28px", padding=padding),
        )

        toolbar = widgets.VBox([toolbar_button])

        def close_click(change):
            if change["new"]:
                toolbar_button.close()
                close_button.close()
                toolbar.close()

        close_button.observe(close_click, "value")

        rows = 2
        cols = 2
        grid = widgets.GridspecLayout(
            rows, cols, grid_gap="0px", layout=widgets.Layout(width="65px")
        )

        icons = ["folder-open", "map", "info", "question"]

        for i in range(rows):
            for j in range(cols):
                grid[i, j] = widgets.Button(
                    description="",
                    button_style="primary",
                    icon=icons[i * rows + j],
                    layout=widgets.Layout(width="28px", padding="0px"),
                )

        def toolbar_click(change):
            if change["new"]:
                toolbar.children = [widgets.HBox([close_button, toolbar_button]), grid]
            else:
                toolbar.children = [toolbar_button]

        toolbar_button.observe(toolbar_click, "value")
        toolbar_ctrl = WidgetControl(widget=toolbar, position="topright")
        self.add(toolbar_ctrl)

        
        output = widgets.Output()
        output_control = WidgetControl(widget=output, position="bottomright")
        self.add(output_control)

        def toolbar_callback(change):
            if change.icon == "folder-open":
                with output:
                    output.clear_output()
                    print(f"You can open a file")

            elif change.icon == "map":
                with output:
                    output.clear_output()
                    widget = self.add_widget()
                    
            else:
                with output:
                    output.clear_output()
                    print(f"Icon: {change.icon}")

        for tool in grid.children:
            tool.on_click(toolbar_callback)


    def add_widget(self, basemaps=None, position='topright'):
                """_add widgets with basemaps , zoom slider  and color picker to map

                Args:
                    basemaps (_type_, optional): _description_. Defaults to None.
                    position (str, optional): _description_. Defaults to 'topright'.
                """

                basemap_selector = widgets.Dropdown(
                    options=[
                        "OpenTopoMap",
                        "Gaode.Satellite",
                        "Esri.WorldStreetMap", "Esri.WorldTopoMap",
                        "Esri.WorldImagery", "Esri.NatGeoWorldMap",
                        "CartoDB.Positron", "CartoDB.DarkMatter",
                        "Strava.All",
                    ],
                    description='Basemap'
                )
                basemap_selector.layout.width = "250px"

                def update_basemap(change):
                    self.add_basemap(change['new'])

                basemap_selector.observe(update_basemap, 'value')

                btn = widgets.Button(icon="map", button_style="primary")
                btn.layout.width = "28px"

                box = widgets.HBox([basemap_selector, btn])

                zoom_slider = widgets.IntSlider(description='Zoom level:', min=0, max=15, value=2)
                widgets.jslink((zoom_slider, 'value'), (self, 'zoom'))

                opacity_slider_widget = self.opacity_slider()

                item = [zoom_slider, opacity_slider_widget]
                vbox = widgets.VBox(item)


                # Define function to handle button click
                def on_button_click(btn):
                    if vbox in control.widget.children:
                        control.widget.children = [box]
                    else:
                        control.widget.children = [box, vbox]

                # Set button click behavior
                btn.on_click(on_button_click)

                control = WidgetControl(widget=widgets.VBox([box, vbox]), position=position)
                self.add_control(control)
    
     

    def opacity_slider(self, layer_index=0, description='Opacity'):
            layer = self.layers[layer_index]
            opacity_slider = widgets.FloatSlider(description=description, min=0, max=1, value=layer.opacity)
            opacity_slider.layout.width = "250px"

            def update_opacity(change):
                 layer.opacity = change['new']

            opacity_slider.observe(update_opacity, 'value')

            return opacity_slider

    def add_latlon (self, position="bottomleft"):

        output_widget = widgets.Output(layout={"border": "0.5px solid black"})
        output_control = WidgetControl(widget=output_widget, position=position)
        self.add_control(output_control)
       

        def handle_interaction(**kwargs):
            latlon = kwargs.get("coordinates")
            latlon = [round(x, 5) for x in latlon]

            if kwargs.get("type") == "click":
                with output_widget:
                    output_widget.clear_output()
                    print("{}".format(latlon))

        self.on_interaction(handle_interaction)


    
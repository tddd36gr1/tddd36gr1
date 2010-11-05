# -*- coding: utf-8 -*-
from xml.dom import minidom
import data_storage

class MapXML:
    __name = None
    __levels = {}
    __path = None

    def handle_name_node(self, node):
        self.__name = node.attributes['id'].value

    def handle_area_node(self, node):
        tiles = self.create_tiles(node.attributes['path'].value)
        self.__levels[int(node.attributes['level'].value)] = tiles

    def handle_base_node(self, node):
        return [node.attributes['width'].value,
                node.attributes['height'].value]

    def handle_size_node(self, node):
        return [node.attributes['cols'].value,
                node.attributes['rows'].value]

    def handle_tile_node(self, node):
        bounds = {"min_latitude":float(node.attributes['minlat'].value),
                  "max_latitude":float(node.attributes['maxlat'].value),
                  "min_longitude":float(node.attributes['minlon'].value),
                  "max_longitude":float(node.attributes['maxlon'].value)}

        return [int(node.attributes['id'].value),
                self.__path + node.attributes['file'].value,
                bounds,
                node.attributes['type'].value]

    def create_tiles(self, path):
        def largest(a, b):
            if a > b:
                return a
            else:
                return b

        tiles = None
        xmldoc = minidom.parse(open(path)).documentElement
        self.__path = path[0:path.rfind("/") + 1]

        for node in xmldoc.childNodes:
            if node.nodeType != node.TEXT_NODE:
                # <base />
                if node.tagName == "base":
                    width, height = self.handle_base_node(node)
                    tiles = data_storage.Tiles(width, height)
                # <size />
                elif node.tagName == "size":
                    cols, rows = self.handle_size_node(node)
                    tiles.create_empty_tiles(int(cols), int(rows))
                # <tile />
                elif node.tagName == "tile":
                    id, file, bounds, type = self.handle_tile_node(node)
                    if tiles:
                        tiles.add_tile(data_storage.MapTile(id,
                                                            file,
                                                            bounds,
                                                            type))
                    else:
                        print "<base /> must come before all <tile /> in the xml!"
                        exit()
        return tiles

    def get_name(self):
        return self.__name

    def get_levels(self):
        return self.__levels

    def __init__(self, filename):
        xmldoc = minidom.parse(open(filename)).documentElement

        # <map>
        for node in xmldoc.childNodes:
            if node.nodeType != node.TEXT_NODE:
                # <name />
                if node.tagName == "name":
                    self.handle_name_node(node)
                # <area />
                elif node.tagName == "area":
                    self.handle_area_node(node)
        # </map>

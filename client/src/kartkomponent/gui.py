# -*- coding: utf-8 -*-
import gtk
import hildon
import gobject
import gui_map
import data_storage
import map_xml_reader


class Gui():
    __map = None
    __map_change_zoom = None

    def on_key_press(self, widget, event, *args):
        # Pil vänster, byter vy
        if event.keyval == 65361:
            if (self.view.get_current_page() != 0):
                self.view.prev_page()
        # Pil höger, byter vy
        elif event.keyval == 65363:
            if (self.view.get_current_page() != 1):
                self.view.next_page()
        # Zoom -
        elif event.keyval == 65477:
            self.__map_change_zoom("-")
        # Zoom +
        elif event.keyval == 65476:
            self.__map_change_zoom("+")

    def __init__(self, map):

        # Sparar handdatorns karta.
        self.__map = map

        # Skapar en notebook-komponent i vilken vi har olika sidor som fungerar
        # som vyer. En sida är för kartvyn, en sida för uppdragsvyn osv.
        # Mer om hur Notebook fungerar står här:
        # http://www.pygtk.org/pygtk2tutorial/sec-Notebooks.html
        self.view = gtk.Notebook()
        self.view.set_show_tabs(False)
        self.view.set_show_border(False)
        self.view.insert_page(self.create_map_view())
        self.view.insert_page(self.create_settings_view())

    # Skapar vyn för kartan
    def create_map_view(self):
        frame = gtk.Frame(self.__map.get_name() + " <longitude, latitude>")
        frame.set_border_width(5)
        map = gui_map.Map(self.__map)
        frame.add(map)
        # Sparar undan funktionen som möjliggör zoomning
        self.__map_change_zoom = map.change_zoom
        return frame

    # Skapar vyn för inställningar
    def create_settings_view(self):
        frame = gtk.Frame("Inställningar")
        frame.set_border_width(5)

        # Skicka GPS-koordinater till basen?
        hbox2 = gtk.HBox(homogeneous=False, spacing=0)
        lblSkickaGPSKoordinater = gtk.Label("Skicka GPS koordinater till basen")
        lblSkickaGPSKoordinater.set_justify(gtk.JUSTIFY_LEFT)
        chkSkickaGPSKoordinater = gtk.CheckButton("Ja")
        #chkSkickaGPSKoordinater.connect("toggled", self.chkSkickaGPSKoordinater_callback)
        hbox2.pack_start(lblSkickaGPSKoordinater, True, True, 5)
        hbox2.pack_start(chkSkickaGPSKoordinater, False, False, 5)

        # Skapar knappen som sparar inställningarna
        btnSpara = gtk.Button("Spara!")
        btnSpara.connect("clicked", self.handle_menu_items, 0)

        vbox = gtk.VBox(homogeneous=False, spacing=0)
        #vbox.pack_start(hbox1, False, False, 0)
        vbox.pack_start(hbox2, False, False, 5)
        vbox.pack_start(btnSpara, False, False, 5)

        frame.add(vbox)
        return frame



    def get_treeview(self, args):
        if len(args) == 1:
            return args[0]
        else:
            return args[2]

    def get_row_number_from_treeview(self, treeview):
        row = treeview.get_selection().get_selected_rows()
        return row[1][0][0]

    # Denna funktion har skapats eftersom det är aningen omständigt att få ut
    # värden från en markering i en lista. Skicka in listan och kolumnen du
    # vill ha ut värdet ifrån så sköter funktionen resten. Första kolumnen är 0,
    # andra 1 osv. 
    def get_value_from_treeview(self, treeview, column):
        # Läs mer om vad row innehåller här (gtk.TreeSelection.get_selected_row):
        # http://www.pygtk.org/pygtk2reference/class-gtktreeselection.html
        row = treeview.get_selection().get_selected_rows()
      
        if len(row[1]) > 0:
            # row innehåller en tuple med (ListStore(s), path(s))
            # Vi plockar ut första värdet i paths. Eftersom vi enbart tillåter
            # användaren att markera en rad i taget kommer det alltid bara finnas
            # ett värde i paths.
            path = row[1][0]
          
            # Hämtar modellen för treeview
            treemodel = treeview.get_model()
          
            # Returnerar värdet
            return treemodel.get_value(treemodel.get_iter(path), column)
        else:
            return None

    def handle_menu_items(self, widget, num):
        self.view.set_current_page(num)

    def menu_exit(self, widget, data=None):
        # Stänger net GUI:t.
        gtk.main_quit()
        


    def run(self):
        print "Kartan inladdad"
        #gtk.main()
        

print "Läser in kartinformation från kartdata/map.xml"
mapxml = map_xml_reader.MapXML("kartkomponent/map.xml")

map = data_storage.MapData(mapxml.get_name(),
                           mapxml.get_levels())

map.set_focus(15.5726, 58.4035)

# Ritar ut tre objekt
#map.add_object("Ambulans1", data_storage.MapObject({"longitude":15.57796,
#                                                    "latitude":58.40479},
#                                                   "ikoner/ambulans.png"))
#map.add_object("Brandbil1", data_storage.MapObject({"longitude":15.5729,
#                                                    "latitude":58.40193},
#                                                   "ikoner/brandbil.png"))
#map.add_object("Sjukhus1", data_storage.MapObject({"longitude":15.5629,
#                                                   "latitude":58.4093},
#                                                  "ikoner/sjukhus.png"))
map.add_object("Employee1", data_storage.MapObject({"longitude":15.5629,
                                                   "latitude":58.4093},
                                                  "ikoner/employee.png"))
#map.add_object("Mission1", data_storage.MapObject({"longitude":db.get_one(Mission).long,
#                                                 "latitude":db.get_one(Mission).lat},
#                                                   "ikoner/Mission.png"))
map.add_object("Shape1", data_storage.MapObject({"longitude":15.5829,
                                                 "latitude":58.4093},
                                                "arc(x - 5, y - 5, 10, 0, 2 * math.pi)",
                                                "set_source_rgb(0, 0, 0)"))
        
app = Gui(map)
app.run()

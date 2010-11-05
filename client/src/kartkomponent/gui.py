# -*- coding: utf-8 -*-
import gtk
import hildon
import gobject
import gui_map

class Gui(hildon.Program):
    __map = None
    __map_change_zoom = None

    def on_window_state_change(self, widget, event, *args):
        if event.new_window_state & gtk.gdk.WINDOW_STATE_FULLSCREEN:
            self.window_in_fullscreen = True
        else:
            self.window_in_fullscreen = False

    def on_key_press(self, widget, event, *args):
        # Ifall "fullscreen"-knappen på handdatorn har aktiverats.
        if event.keyval == gtk.keysyms.F6:
            if self.window_in_fullscreen:
                self.window.unfullscreen()
            else:
                self.window.fullscreen()
        # Pil vänster, byter vy
        elif event.keyval == 65361:
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
        # Initierar hildon (GUI-biblioteket för N810)
        hildon.Program.__init__(self)

        # Sparar handdatorns karta.
        self.__map = map

        # Skapar programmets fönster
        self.window = hildon.Window()
        # Någon storlek så att PyGTK inte klagar
        self.window.set_size_request(200, 200)
        # Funktion som körs när prorammet ska stängas av
        self.window.connect("destroy", self.menu_exit)
        self.add_window(self.window)

        # Möjliggör fullscreen-läge
        self.window.connect("key-press-event", self.on_key_press)
        self.window.connect("window-state-event", self.on_window_state_change)
        # Programmet är inte i fullscreen-läge från början.
        self.window_in_fullscreen = False

        # Skapar en notebook-komponent i vilken vi har olika sidor som fungerar
        # som vyer. En sida är för kartvyn, en sida för uppdragsvyn osv.
        # Mer om hur Notebook fungerar står här:
        # http://www.pygtk.org/pygtk2tutorial/sec-Notebooks.html
        self.view = gtk.Notebook()
        self.view.set_show_tabs(False)
        self.view.set_show_border(False)
        self.view.insert_page(self.create_map_view())
        self.view.insert_page(self.create_settings_view())

        # Lägger in vyn i fönstret
        self.window.add(self.view)

        # Skapar menyn
        self.window.set_menu(self.create_menu())

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

    # Skapar en meny som kommer ligga längst upp i vårt program.
    def create_menu(self):
        # Skapar tre stycken meny-inlägg.
        menuItemKarta = gtk.MenuItem("Karta")
        menuItemInstallningar = gtk.MenuItem("Inställningar")
        menuItemSeparator = gtk.SeparatorMenuItem()
        menuItemExit = gtk.MenuItem("Exit")

        menuItemKarta.connect("activate", self.handle_menu_items, 0)
        menuItemInstallningar.connect("activate", self.handle_menu_items, 1)
        menuItemExit.connect("activate", self.menu_exit)

        # Skapar en meny som vi lägger in dessa inlägg i.
        menu = gtk.Menu()
        menu.append(menuItemKarta)
        menu.append(menuItemInstallningar)
        menu.append(menuItemSeparator)
        menu.append(menuItemExit)

        return menu

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
        self.window.show_all()
        gtk.main()

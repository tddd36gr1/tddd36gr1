import gtk
from mapwidget import MapWidget


class MainWindow(gtk.Window):
    mapwidget = None
    label = None

    def __init__(self):
        gtk.Window.__init__(self)
        self.connect('destroy', gtk.main_quit)

        vbox = gtk.VBox()
        self.add(vbox)

        topbox = gtk.HBox()
        vbox.pack_start(topbox, False)

        self.label = gtk.Label("lat, long")
        topbox.pack_start(self.label)

        zoomInButton = gtk.Button("+")
        zoomInButton.connect("clicked", self.zoom_in)
        topbox.pack_start(zoomInButton, False)

        zoomOutButton = gtk.Button("-")
        zoomOutButton.connect("clicked", self.zoom_out)
        topbox.pack_start(zoomOutButton, False)

        goLiuButton = gtk.Button("Go to LiU")
        goLiuButton.connect("clicked", self.goto_liu)
        topbox.pack_start(goLiuButton, False)

        goRydButton = gtk.Button("Go to Ryd")
        goRydButton.connect("clicked", self.goto_ryd)
        topbox.pack_start(goRydButton, False)

        self.mapwidget = MapWidget(58.3953, 15.5691)
        vbox.pack_start(self.mapwidget)

        self.mapwidget.connect("focus-changed", self.focus_changed_handler)
        self.mapwidget.connect("map-clicked", self.map_clicked_handler)
        self.show_all()

 
    def focus_changed_handler(self, widget, coord):
        #print "focus changed: ", coord
        self.label.set_text("lat: %s, long: %s" % (coord[0], coord[1]))

    def map_clicked_handler(self, widget, coord):
        print "map-clicked: ", coord

    def goto_liu(self, widget):
        self.mapwidget.focus = (58.398, 15.578)
        self.mapwidget.zoom_level = 14

    def goto_ryd(self, widget):
        self.mapwidget.focus = (58.409, 15.567)
        self.mapwidget.zoom_level = 16

    def zoom_in(self, widget):
        self.mapwidget.zoom_level += 1

    def zoom_out(self, widget):
        self.mapwidget.zoom_level -= 1


if __name__ == '__main__':
    win = MainWindow()
    gtk.main()

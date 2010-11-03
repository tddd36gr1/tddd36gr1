import gtk

class MainWindow(gtk.Window):
    label = None

    def __init__(self):
        gtk.Window.__init__(self)
        self.connect('destroy', gtk.main_quit)

        vbox = gtk.VBox()
        self.add(vbox)

        topbox = gtk.HBox()
        vbox.pack_start(topbox, False)

        self.label = gtk.Label("Projektgrupp 1 aeger")
        topbox.pack_start(self.label)

        zoomInButton = gtk.Button("WOOT")
        zoomInButton.connect("clicked", self.hello)
        topbox.pack_start(zoomInButton, False)

        zoomOutButton = gtk.Button("1337")
        zoomOutButton.connect("clicked", self.mongo)
        topbox.pack_start(zoomOutButton, False)
        
        self.show_all()
   
    def hello(self, widget):
        print "Hej projektgrupp 1!"
        
    def mongo(self, widget):
        print "AWESOME AWESOME AWESOME AWESOME AWESOME"


if __name__ == '__main__':
    win = MainWindow()
    gtk.main()
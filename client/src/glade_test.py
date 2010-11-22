'''
Created on 17 nov 2010

@author: Mandrill
'''
#coding=utf8
import gtk
import hildon
import pango
import pygtk
import sys
import gtk.glade
from mapwidget.mapwidget import MapWidget
from class_.base_objects import Mission, StatusCode

class MainGUI(hildon.Program):

    def __init__(self, db):
        hildon.Program.__init__(self)
        
        #set reference to databaseworker
        self.db = db
        
        self.setup_window()
        self.load_and_fix_glade()
        self.add_map()
        self.insert_data()
    
    def setup_window(self):
        """
        Setups main window of the program, links exit buttons
        """
        self.window = hildon.Window()
        self.window.set_title("TDDD36gr1 - Ignis ALPHA")
        self.add_window(self.window)
        self.window.fullscreen()
        self.window.connect("destroy", gtk.main_quit)
        
    def load_and_fix_glade(self):
        self.builder = gtk.Builder()
        self.builder.add_from_file("new_GUI.glade") 
        
	    #Should fix button actions
        self.builder.connect_signals(self)
        
        #reparent the hbox1 from glade to self.window
        hbox1 = self.builder.get_object("hbox1")
        hbox1.reparent(self.window)
        
        self.main_notebook = self.builder.get_object("main_notebook")

    def on_map_button_clicked(self, widget, data=None):
        self.main_notebook.set_current_page(0)
    
    def on_mission_button_clicked(self, widget, data=None):
        self.main_notebook.set_current_page(1)

    def on_phone_button_clicked(self, widget, data=None):
        self.main_notebook.set_current_page(2)

    def on_messaging_button_clicked(self, widget, data=None):
        self.main_notebook.set_current_page(3)
        
    def on_missions_my_row_changed(self, widget, data=None):
        entry1, entry2 = self.builder.get_object("missions_my_treeview").get_selection().get_selected()
        entry = entry1.get_value(entry2, 0)
        

    def __quit__(self, widget, data=None): 
        sys.exit(1)
        
    def add_map(self):
        self.map_placeholder = self.builder.get_object("map_placeholder")
        self.mapWidget = MapWidget(58.3953, 15.5691)
        temp = self.builder.get_object("map_placeholder_label")
        temp.destroy()
        self.map_placeholder.add(self.mapWidget)
        
    def insert_data(self):
        self.insert_my_missions()
    
    def insert_my_missions(self):
        mission_my_liststore = self.builder.get_object("mission_my_liststore")
        my_missions = self.db.get_all(Mission)
        for mission in my_missions:
            mission_my_liststore.append((mission.title, mission.status_object.name))
        
    def run(self):
        self.window.show_all()
        gtk.main()
        
def start(db):
    MainGUI(db).run()

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
    """
    This class basically creats and controls the whole GUI (except map widget) 
    """

    def __init__(self, db):
        hildon.Program.__init__(self)
        
        #set reference to databaseworker
        self.db = db
        
        #Self-explanary function names ftw
        self.setup_window()
        self.load_and_fix_glade()
        self.set_self_variables()
        self.add_map()
        self.insert_data()
    
    def setup_window(self):
        """
        Setups main window of the program, links exit buttons
        """
        self.window = hildon.Window()
        self.window.set_title("TDDD36gr1 - Ignis ALPHA")
        #Adds window to program
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
    
    def set_self_variables(self):
        """
        Gets commonly used GTK-components from glade file + some other variables
        """
        self.mission_my_liststore = self.builder.get_object("mission_my_liststore")
        self.main_notebook = self.builder.get_object("main_notebook")
        self.mission_my_info_button = self.builder.get_object("mission_my_info_button")
        self.mission_my_treeview = self.builder.get_object("missions_my_treeview")
        self.mission_my_button_layout = self.builder.get_object("mission_my_button_layout")
        self.mission_selected = 0

    def __quit__(self, widget, data=None):
        """
        This function should be called whenever you wish to quit the program
        """ 
        sys.exit(1)
        
    def add_map(self):
        """
        Adds map to the topmost view in the main menu
        """
        #Destroy random placeholder label
        self.builder.get_object("map_placeholder_label").destroy()
        
        #Import map widget and add to our GUI
        self.map_placeholder = self.builder.get_object("map_placeholder")
        self.mapWidget = MapWidget(58.3953, 15.5691)
        self.map_placeholder.add(self.mapWidget)
        
    def insert_data(self):
        """
        This function is used to populate various data models
        """
        self.insert_my_missions()
    
    def insert_my_missions(self):
        """
        Populates my missions-view
        """
        self.my_missions = self.db.get_all(Mission)
        for mission in self.my_missions:
            self.mission_my_liststore.append((mission.title, mission.status_object.name))

    def on_map_button_clicked(self, widget, data=None):
        """
        Runs when the map button in the main menu is clicked, change to map view
        """
        self.main_notebook.set_current_page(0)
    
    def on_mission_button_clicked(self, widget, data=None):
        """
        Runs when the mission button in the main menu is clicked, change to mission view
        """
        self.main_notebook.set_current_page(1)

    def on_phone_button_clicked(self, widget, data=None):
        """
        Runs when the phone button in the main menu is clicked, change to phone view
        """
        self.main_notebook.set_current_page(2)

    def on_messaging_button_clicked(self, widget, data=None):
        """
        Runs when the messaging button in the main menu is clicked, change to messaging view
        """
        self.main_notebook.set_current_page(3)
        
    def on_missions_my_selected_changed(self, widget, data=None):
        """
        Runs when the user selects a mission row in the My Missions-view
        """
        model, iter = self.mission_my_treeview.get_selection().get_selected()
        self.mission_selected = model.get_path(iter)[0]
        self.mission_my_button_layout.move(self.mission_my_info_button, 0, self.mission_selected*32)
        
    def on_mission_my_info_button_clicked(self, widget, data=None):
        """
        Runs when user clicks on an "open" button next to a row in the my missions view
        Switches view to a detailed view about the selected mission
        """
        #Switch view
        self.main_notebook.set_current_page(4)
        #Sets texts in the new view
        self.builder.get_object("mission_dialog_title").set_text(self.my_missions[self.mission_selected].title)
        self.builder.get_object("mission_dialog_label").set_text(self.my_missions[self.mission_selected].__repr__())
        
        #Sets checkbox if mission has finished status
        if (self.my_missions[self.mission_selected].status == 3):
            self.builder.get_object("mission_finished_checkbutton").set_active(True)
        else:
            self.builder.get_object("mission_finished_checkbutton").set_active(False)
    
    def mission_close_dialog(self, widget, data=None):
        """
        Runs when user presses "back" button in the mission detailed dialog view,
        switches view back to mission view
        """
        self.main_notebook.set_current_page(1)
    
    def mission_toggle_finished(self, widget, data=None):
        """
        Runs when user checks/unchecks the "finished" checkbox in the detailed mission dialog view
        Sets status of mission to finished when checked and status 2 when unchecked
        """
        button = self.builder.get_object("mission_finished_checkbutton")
        if(button.get_active()):
            self.my_missions[self.mission_selected].status = 3
            self.db.commit()
            self.builder.get_object("mission_dialog_label").set_text(self.my_missions[self.mission_selected].__repr__())
        else:
            self.my_missions[self.mission_selected].status = 2
            self.db.commit()
            self.builder.get_object("mission_dialog_label").set_text(self.my_missions[self.mission_selected].__repr__())
        
    def mission_zoom_to_map(self, widget, data=None):
        """
        Placeholder function, should switch to map view and zoom to the mission's placemark
        """
        return
        
    def run(self):
        self.window.show_all()
        gtk.main()
        
def start(db):
    MainGUI(db).run()

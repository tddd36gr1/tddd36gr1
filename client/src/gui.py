# -*- coding: utf-8 -*-
'''
Created on 17 nov 2010

@author: Mandrill
'''
import gtk
import gtk.gdk
import hildon
import pango
import pygtk
import sys
import pickle
import gtk.glade
import requesthandler
import SETTINGS
import threading
from mapwidget.mapwidget import MapWidget
from class_.base_objects import *

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
        
        gtk.gdk.threads_init()

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
        self.mission_notified = False
        self.message_notified = False
        
        
        self.mission_my_liststore = self.builder.get_object("mission_my_liststore")
        self.mission_all_liststore = self.builder.get_object("mission_all_liststore")
        self.mission_finished_liststore = self.builder.get_object("mission_finished_liststore")
        self.mission_images_liststore = self.builder.get_object("mission_images_liststore")
        
        self.message_inbox_liststore = self.builder.get_object("message_inbox_liststore")
        self.message_sent_liststore = self.builder.get_object("message_sent_liststore")
        
        self.status_codes_liststore = self.builder.get_object("status_codes_liststore")
        
        self.main_notebook = self.builder.get_object("main_notebook")
        self.mission_notebook = self.builder.get_object("mission_notebook")
        self.message_notebook = self.builder.get_object("message_notebook")
        
        self.mission_my_info_button = self.builder.get_object("mission_my_info_button")
        self.mission_all_info_button = self.builder.get_object("mission_all_info_button")
        self.mission_finished_info_button = self.builder.get_object("mission_finished_info_button")
        
        self.message_inbox_open_button = self.builder.get_object("message_inbox_open_button")
        self.message_sent_open_button = self.builder.get_object("message_sent_open_button")
        
        self.mission_my_treeview = self.builder.get_object("missions_my_treeview")
        self.mission_all_treeview = self.builder.get_object("mission_all_treeview")
        self.mission_finished_treeview = self.builder.get_object("mission_finished_treeview")
        
        self.mission_my_button_layout = self.builder.get_object("mission_my_button_layout")
        self.mission_all_button_layout = self.builder.get_object("mission_all_button_layout")
        self.mission_finished_button_layout = self.builder.get_object("mission_finished_button_layout")
        
        self.message_inbox_button_layout = self.builder.get_object("message_inbox_button_layout")
        self.message_sent_button_layout = self.builder.get_object("message_sent_button_layout")
        
        self.message_inbox_treeview = self.builder.get_object("message_inbox_treeview")
        self.message_sent_treeview = self.builder.get_object("message_sent_treeview")
        
        self.mission_status_combobox = self.builder.get_object("mission_status_combobox")
        self.mission_selected = 0
        self.message_selected = 0
        self.employee_id = SETTINGS.employee_id
        self.selected_mission = None

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
        self.mapwidget = MapWidget(58.3953, 15.5691, self.db)
        self.map_placeholder.add(self.mapwidget)
        
    def insert_data(self):
        """
        This function is used to populate various data models
        """
        self.insert_missions()
        self.insert_messages()
        self.insert_statuscodes()
    
    def insert_missions(self):
        """
        Populates the missions view
        """
        self.mission_my_liststore.clear()
        self.my_missions = self.db.get_one_by_id(Employee, self.employee_id).missions
        for mission in self.my_missions:
            self.mission_my_liststore.append((mission.title, mission.status_object.name))
            
        self.mission_all_liststore.clear()
        self.missions = self.db.get_all(Mission)
        for mission in self.missions:
            self.mission_all_liststore.append((mission.title, mission.status_object.name))
        
        self.mission_finished_liststore.clear()        
        self.finished_missions = self.db.get_all_finished_missions()
        for mission in self.finished_missions:
            self.mission_finished_liststore.append((mission.title, mission.status_object.name))
            
    def insert_messages(self):
        """
        Populates the messages view
        """
        self.message_inbox_liststore.clear()
        self.message_sent_liststore.clear()
        
        self.inbox_messages = self.db.get_one_by_id(Employee, self.employee_id).txt_received
        self.sent_messages = self.db.get_one_by_id(Employee, self.employee_id).txt_sent
        
        for message in self.inbox_messages:
            self.message_inbox_liststore.append((message.src_object.fname+' '+message.src_object.lname, message.msg))
            
        for message in self.sent_messages:
            self.message_sent_liststore.append((message.dst_object.fname+' '+message.dst_object.lname, message.msg))
            
    def insert_statuscodes(self):
        """
        Inserts all status codes from DB
        """
        self.status_codes_liststore.clear()
        self.status_codes_liststore.append(("Ändra status: ", 0))
        
        for statuscode in self.db.get_all(StatusCode):
            self.status_codes_liststore.append((statuscode.name, statuscode.id))
        
        self.mission_status_combobox.set_active(0)

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
        if (self.mission_notified == True):
            self.builder.get_object("mission_button_img").set_from_file("menybilder/uppdrag.png")
            self.mission_notified = False

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
        if (self.message_notified == True):
            self.builder.get_object("messaging_button_img").set_from_file("menybilder/brev.png")
            self.message_notified = False
        
    def on_missions_my_selected_changed(self, widget, data=None):
        """
        Runs when the user selects a mission row in the My Missions-view
        """
        model, iter = self.mission_my_treeview.get_selection().get_selected()
        self.mission_selected = model.get_path(iter)[0]
        self.mission_my_button_layout.move(self.mission_my_info_button, 0, self.mission_selected*32)
        
    def on_missions_all_selected_changed(self, widget, data=None):
        """
        Runs when the user selects a mission row in the All Missions-view
        """
        model, iter = self.mission_all_treeview.get_selection().get_selected()
        self.mission_selected = model.get_path(iter)[0]
        self.mission_all_button_layout.move(self.mission_all_info_button, 0, self.mission_selected*32)
        
    def on_missions_finished_selected_changed(self, widget, data=None):
        """
        Runs when the user selects a mission row in the Finished Missions-view
        """
        model, iter = self.mission_finished_treeview.get_selection().get_selected()
        self.mission_selected = model.get_path(iter)[0]
        self.mission_finished_button_layout.move(self.mission_finished_info_button, 0, self.mission_selected*32)
        
        
    def on_message_inbox_selected_changed(self, widget, data=None):
        """
        Runs when the user selects a message row in the Inbox Messages-view
        """
        model, iter = self.message_inbox_treeview.get_selection().get_selected()
        self.message_selected = model.get_path(iter)[0]
        self.message_inbox_button_layout.move(self.message_inbox_open_button, 0, self.message_selected*32)
        
        
    def on_message_sent_selected_changed(self, widget, data=None):
        """
        Runs when the user selects a mission row in the Sent Messages-view
        """
        model, iter = self.message_sent_treeview.get_selection().get_selected()
        self.message_selected = model.get_path(iter)[0]
        self.message_sent_button_layout.move(self.message_sent_open_button, 0, self.message_selected*32)
        
    def send_new_message(self, widget, data=None):
        """
        Runs when user presses the send-button in the new message view
        """
        entry = self.builder.get_object("message_new_receiver")
        to = entry.get_text()
        buffer = self.builder.get_object("message_new_textview").get_buffer()
        msg = buffer.get_text(buffer.get_start_iter(),buffer.get_end_iter())
        employee = self.db.get_employee_by_name(to)
        
        if (employee == None):
            print "Hittade ingen anställd"
            entry.modify_base(gtk.STATE_NORMAL, gtk.gdk.color_parse("red"))
            self.builder.get_object("message_new_title").set_markup("<span foreground=\"red\"><big>Ingen anställd med det namnet</big></span>")
        else:
            requesthandler.send_message(TextMessage(SETTINGS.employee_id, employee.id, msg), self.db)
            entry.set_text('')
            buffer.set_text('')
            entry.modify_base(gtk.STATE_NORMAL, gtk.gdk.color_parse("white"))
            self.builder.get_object("message_new_title").set_markup("<big>Nytt meddelande</big>")
            self.insert_messages()

            
    def clear_message(self, widget, data=None):
        """
        Runs when user presses the clear button in the new message view
        """
        entry = self.builder.get_object("message_new_receiver")
        entry.set_text("")
        entry.modify_base(gtk.STATE_NORMAL, gtk.gdk.color_parse("white"))
        buffer = self.builder.get_object("message_new_textview").get_buffer()
        buffer.set_text("")
        self.builder.get_object("message_new_title").set_markup("<big>Nytt meddelande</big>")
        
    def on_mission_info_button_clicked(self, widget, data=None):
        """
        Runs when user clicks on an "open" button next to a row in the my missions view
        Switches view to a detailed view about the selected mission
        """
        #Switch view
        self.main_notebook.set_current_page(4)
        #Sets texts in the new view
        if (self.mission_notebook.get_current_page() == 2):
            self.selected_mission = self.finished_missions[self.mission_selected]

        elif (self.mission_notebook.get_current_page() == 1):
            self.selected_mission = self.missions[self.mission_selected]
        else:
            self.selected_mission = self.my_missions[self.mission_selected]
            
        self.builder.get_object("mission_dialog_title").set_markup("<big>Uppdrag: "+self.selected_mission.title+"</big>")
        self.builder.get_object("mission_dialog_status").set_text(self.selected_mission.status_object.name)
        
        #Display description texts
        str = ""
        for text in self.selected_mission.missiontexts:
            str = str+text.descr+"\n"
        self.builder.get_object("mission_dialog_description").get_buffer().set_text(str)
        
        #Display mission images
        self.mission_images_liststore.clear()
        for image in self.selected_mission.images:
            self.mission_images_liststore.append((gtk.gdk.pixbuf_new_from_file("db/images/thumb_"+image.filename), image.title, image.id))
    
    def open_message(self, widget, data=None):
        """
        Runs when the user presses an "open"-button in the message inbox or sent-view
        """
        
        #Switch view
        self.main_notebook.set_current_page(5)
        
        #Sets texts in the new view
        if (self.message_notebook.get_current_page() == 0):
            self.selected_message = self.inbox_messages[self.message_selected]
            self.builder.get_object("message_top_label").set_markup("<big>Meddelande från: "+self.selected_message.src_object.fname+" "+self.selected_message.src_object.lname+"</big>")
        
        elif (self.message_notebook.get_current_page() == 2):
            self.selected_message = self.sent_messages[self.message_selected]
            self.builder.get_object("message_top_label").set_markup("<big>Meddelande till: "+self.selected_message.dst_object.fname+" "+self.selected_message.dst_object.lname+"</big>")

        self.builder.get_object("message_text_label").set_markup(self.selected_message.msg)
        
    def message_close_dialog(self, widget, data=None):
        """
        Runs when user presses "back" button in the opened message view,
        switches view back to messages view
        """
        self.main_notebook.set_current_page(3)
        
    def mission_close_dialog(self, widget, data=None):
        """
        Runs when user presses "back" button in the mission detailed dialog view,
        switches view back to mission view
        """
        self.main_notebook.set_current_page(1)
    
    def mission_close_image(self, widget, data=None):
        """
        Runs when user presses "back" button in the mission full screen image view,
        switches view back to detailed mission view
        """
        self.main_notebook.set_current_page(4)
        
    def change_mission_status(self):
        """
        Runs when user changes status of a mission in a combobox and decides to save the changes
        """
        i = self.mission_status_combobox.get_active()
        if (i == 0):
            return
        
        self.selected_mission.status = i
        try:
            self.selected_mission.status_object = self.db.get_one_by_id(StatusCode, i)
        except:
        #except InvalidRequestError:
            self.db.add_or_update(self.selected_mission)
            self.insert_missions()
            self.builder.get_object("mission_dialog_status").set_text(self.selected_mission.status_object.name)
            self.mission_status_combobox.set_active(0)
        else:
            self.db.add_or_update(self.selected_mission)
            self.insert_missions()
            self.builder.get_object("mission_dialog_status").set_text(self.selected_mission.status_object.name)
            self.mission_status_combobox.set_active(0)
        
    def mission_save(self, widget, data=None):
        """
        Runs when user presses save button in the detailed mission view,
        saves all changes to the mission
        """
        self.change_mission_status()
        
        
    def mission_zoom_to_map(self, widget, data=None):
        """
        Switch to map view and zoom to the mission's placemark in the opened mission view
        """
        self.mapwidget.set_focus((float(self.selected_mission.lat), float(self.selected_mission.long)))
        self.main_notebook.set_current_page(0)
        
    def on_mission_image_activated(self, widget, data=None):
        """
        Opens up mission image in full screen when user presses enter or double-clicks a mission image
        """
        self.main_notebook.set_current_page(6)
        image = self.selected_mission.images[self.builder.get_object("mission_image_iconview").get_selected_items()[0][0]]
        self.builder.get_object("mission_image_title").set_markup("<big>"+image.title+"</big>")
        self.builder.get_object("mission_full_image").set_from_file("db/images/"+image.filename)
        
    def run(self):
        self.window.show_all()
        gtk.main()
    
    def notify(self, object):
        """
        Run this to notify the GUI about new / updated data, 
        for example when receiving data from the network
        
        Just send the new / updated data object as an argument
        """
        
        if (object.__class__ == Mission):
            self.insert_missions()
            if (self.mission_notified == False):
                self.builder.get_object("mission_button_img").set_from_file("menybilder/uppdrag_new.png")
                self.mission_notified = True
        elif (object.__class__ == TextMessage):
            self.insert_messages()
            if (self.message_notified == False):
                self.builder.get_object("messaging_button_img").set_from_file("menybilder/brev_new.png")
                self.message_notified = True
        elif (object.__class__ == StatusCode):
            self.insert_statuscodes()
            
def start(db):
    global maingui
    maingui = MainGUI(db)
    maingui.run()
    
def notify(object):
    """
    See notify inside of MainGUI-class
    """
    maingui.notify(object)
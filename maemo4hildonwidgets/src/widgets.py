#!/usr/bin/env python2.5

# 
# Copyright (c) 2007-2008 INdT.
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

# ============================================================================
# Name        : widgets.py
# Author      : 
# Version     : 0.1
# Description : A Python Hildon Widgets Example for Diablo SDK 
# ============================================================================


import gtk
import hildon

class Widgets(hildon.Program):
    def __init__(self):
       hildon.Program.__init__(self)
   
       self.window = hildon.Window()
       self.window.connect("delete_event", self.quit)
       self.window.set_title("Hildon Widgets Example")
       self.add_window(self.window)
       
       hbox = gtk.HBox(False, 10)
       
       vbox1 = gtk.VBox(False, 10)
       vbox2 = gtk.VBox(False, 10)
       
       #Calendar
       button = gtk.Button("Calendar Popup")
       button.connect("clicked", self.button_callendar, self.window)
       vbox1.pack_start(button)
       
       #Font Selector
       button = gtk.Button("Font Dialog")
       button.connect("clicked", self.button_font_selector, self.window)
       vbox2.pack_start(button)
       
       #Password
       button = gtk.Button("Login Prompt")
       button.connect("clicked", self.button_login, self.window)
       vbox1.pack_start(button)
       
        #Password
       button = gtk.Button("Confirmation Note")
       button.connect("clicked", self.button_note, self.window)
       vbox2.pack_start(button)

       #Time Picker
       button = gtk.Button("Time Picker")
       button.connect("clicked", self.button_time_picker, self.window)
       vbox1.pack_start(button)

       #Code Dialog
       button = gtk.Button("Code Dialog")
       button.connect("clicked", self.button_code_dialog, self.window)
       vbox2.pack_start(button)

       #Sort Dialog
       button = gtk.Button("Sort Dialog")
       button.connect("clicked", self.button_sort_dialog, self.window)
       vbox1.pack_start(button)
       
       #Set Password Dialog
       button = gtk.Button("Set Password Dialog")
       button.connect("clicked", self.button_set_password, self.window)
       vbox2.pack_start(button)

       hbox.add(vbox1)
       hbox.add(vbox2)
       
       #Adding Vbox
       self.window.add(hbox)
       self.window.show_all()

    def quit(self, *args):
       gtk.main_quit()
   
    def button_callendar(widget, button, window):
       dialog = hildon.CalendarPopup(window, 2008, 04, 29)
       dialog.run()
       date_tuple = dialog.get_date()
       dialog.destroy()
      
    def button_font_selector(widget, button, window):
       fontDialog = hildon.FontSelectionDialog(window, "Choose a font...")
       fontDialog.set_preview_text ("Hildon Widgets")
       fontDialog.run()
       fontDialog.hide()

    def button_login(widget, button, window):
        dialog = hildon.LoginDialog(window)
        response = dialog.run()
        dialog.hide()
        dialog.destroy()

    def button_note(widget, button, window):
        dialog = hildon.Note ("confirmation", (window, "Do you confirm?", gtk.STOCK_DIALOG_WARNING) )
        dialog.set_button_texts ("Yes", "No")
        response = dialog.run()
        dialog.destroy()
   
    def button_time_picker(widget, button, window):
       time_picker = hildon.TimePicker(window)
       response = time_picker.run()
       time_picker.hide()
       
    def button_code_dialog(widget, button, window):
       dialog = hildon.CodeDialog()
       response = dialog.run()
       dialog.hide()

    def button_sort_dialog(widget, button, window):
        dialog = hildon.SortDialog(window)
        response = dialog.run()
        dialog.hide()

    def button_set_password(widget, button, window):
       dialog = hildon.SetPasswordDialog(window, False)
       response = dialog.run()
       dialog.hide()
   
    def run(self):
       self.window.show_all()
       gtk.main()

if __name__ == "__main__":
   app = Widgets()
   app.run()
        


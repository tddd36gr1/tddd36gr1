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
# Name        : banner.py
# Author      : 
# Version     : 0.1
# Description : Hildon Banner Example  
# ============================================================================

import pygtk
pygtk.require("2.0")

import gtk
import hildon

class HildonBannerExample:

    def __init__(self):
        self.window = hildon.Window()
        self.window.connect("destroy", gtk.main_quit)
        self.vbox = gtk.VBox()

        # Text Frame
        self.frame_text = gtk.Frame("Text")
        hbox = gtk.HBox()
        hbox.pack_start(gtk.Label("Text"), False, False)

        self.text_entry = gtk.Entry()
        hbox.pack_start(self.text_entry)

        self.frame_text.add(hbox)

        self.vbox.pack_start(self.frame_text)
        
        # Information frame
        self.frame_inform = gtk.Frame("Information")
        vbox = gtk.VBox()

        self.markup_check = gtk.CheckButton("Use markup")
        vbox.pack_start(self.markup_check)

        hbox = gtk.HBox()
        hbox.pack_start(gtk.Label("icon-name"), False, False)
        self.icon_entry = gtk.Entry()
        hbox.pack_start(self.icon_entry)
        vbox.pack_start(hbox)

        button = gtk.Button("Show information banner")
        button.connect("clicked", self.show_information)
        vbox.pack_start(button)

        self.frame_inform.add(vbox)

        self.vbox.pack_start(self.frame_inform)

        self.window.add(self.vbox)

        self.window.show_all()

    def show_information(self, button, data=None):
        icon_text = self.icon_entry.get_text()

        if icon_text == "":
            icon_text = None
            
        if not self.markup_check.get_active():
            hildon.hildon_banner_show_information(self.window,
                    icon_text, self.text_entry.get_text())
        else:
            hildon.hildon_banner_show_information_with_markup(self.window,
                    icon_text, self.text_entry.get_text())
            

        
if __name__ == "__main__":
    prog = HildonBannerExample()
    gtk.main()

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
# Name        : handle_special_keys.py
# Author      : 
# Version     : 0.1
# Description : Handling Special Keys  
# ============================================================================

import hildon
import gtk

def key_pressed_cb(widget, event, label):
    if event.keyval == hildon.KEY_UP:
        label.set_text("Up")
    elif event.keyval == hildon.KEY_DOWN:
        label.set_text("Down")
    elif event.keyval == hildon.KEY_LEFT:
        label.set_text("Left")
    elif event.keyval == hildon.KEY_RIGHT:
        label.set_text("Right")
    elif event.keyval == hildon.KEY_SELECT:
        label.set_text("SELECT")
    elif event.keyval == hildon.KEY_MENU:
        label.set_text("Menu")
    elif event.keyval == hildon.KEY_HOME:
        label.set_text("Home")
    elif event.keyval == hildon.KEY_ESC:
        label.set_text("Esc")
    elif event.keyval == hildon.KEY_FULLSCREEN:
        label.set_text("Fullscreen")
    elif event.keyval == hildon.KEY_INCREASE:
        label.set_text("Increase")
    elif event.keyval == hildon.KEY_DECREASE:
        label.set_text("Decrease")
    else:
        label.set_text("press any special key: menu, navigation,\n resize, increase/descrease...")

def main():
    window = hildon.Window()
    window.connect("destroy", gtk.main_quit)

    label = gtk.Label("press any special key: menu, navigation,\n resize, increase/descrease...")
    window.add(label)
    
    window.connect("key-press-event", key_pressed_cb, label)

    window.show_all()

    gtk.main()

if __name__ == "__main__":
    main()


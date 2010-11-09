#coding=utf8
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
# Name        : hello_world.py
# Author      : 
# Version     : 0.1
# Description : Python Hildon Hello World
# ============================================================================


import gtk 
import hildon

class HelloWorldApp(hildon.Program):
    def __init__(self):
        hildon.Program.__init__(self)

        self.window = hildon.Window()
        self.window.connect("delete_event", self.quit)  
        self.add_window(self.window)

        label = gtk.Label("Hello World!!!")
        self.window.add(label)
        label.show()   

    def quit(self, *args):
        print "Goodbye world!"
        gtk.main_quit()
        
    def run(self):     
        self.window.show_all()
        gtk.main() 

if __name__ == "__main__":  
    app = HelloWorldApp() 
    app.run()         

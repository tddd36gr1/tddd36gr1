from easy import camera
from easy import ui

global picture_number

resolution_dict = {'176x144': camera.RESOLUTION_176x144,
                   '320x240': camera.RESOLUTION_320x240,
                   '352x288': camera.RESOLUTION_352x288,
                   '640x480': camera.RESOLUTION_640x480}

def start(app):
    camera.display()
    return False

def click(app, button):
    global picture_number
    camera.click(app['file_name'])
    picture_number += 1
    app['file_name'] = 'Image' + str(picture_number) + '.jpg'

def set_resolution(app, widget, resolution):
    camera.stop_display()
    camera.display(resolution=resolution_dict[resolution])

app = ui.App(title='Easy Camera Snapshot',

                top=(ui.Entry(id='file_name', label='Snapshot name:', value=''),
                     ui.Selection(id='resolution', label='Resolution:',
                                     options=['176x144', '320x240', '352x288', '640x480'],
                                     value='352x288', callback=set_resolution),
                     ui.Button(id='click', label='Click', callback=click)),
                 center=ui.XWindow(id='xwindow'))

app.idle_add(callback=start)

picture_number = 0
app['file_name'] = 'Image' + str(picture_number) + '.jpg'
camera.set_window_id(app['xwindow'].get_window_id())

ui.run()
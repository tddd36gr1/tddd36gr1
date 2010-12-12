from easy import camera
from easy import ui
import Image
import os
import gtk

picture_number = 0
bild = 'image' + str(picture_number) + '.jpg'
    
def click():
    global picture_number
    global bild
    camera.click("db/images/"+bild)
    camera.stop_display()
    print "Picture saved"
    filename = bild
    saveThumbFile(filename)
    picture_number = picture_number + 1
    bild = 'image' + str(picture_number) + '.jpg'
    return filename

def saveThumbFile(filename):
    print filename
    im = Image.open("db/images/"+filename)
    im = im.resize((180, 180))
    im.save("db/images/thumb_" + filename)
    print "Thumb saved"
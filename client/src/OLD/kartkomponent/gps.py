#import gobject
#import location
import random

def get_gps_lat():
    latt = random.uniform(58.3894400, 58.4184000)
    return float(latt)
def get_gps_lon():
    lonn = random.uniform(15.5501000, 15.6141500)
    return float(lonn)



#get_gps_lat()
#get_gps_lon()
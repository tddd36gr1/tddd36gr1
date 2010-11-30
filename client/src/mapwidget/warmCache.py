# by teh jonerer and the elofferer.
# just grabs some images (like... linkoping) to populate the cache.

from tilenames import tileXY, tileEdges
from urllib import urlretrieve
import os


def GetOsmTileData(z,x,y):
    """Download OSM data for the region covering a slippy-map tile"""
    if(x < 0 or y < 0 or z < 0 or z > 25):
        print "Disallowed %d,%d at %d" % (x,y,z)
        return
  
    directory = 'cache/%d/%d/' % (z,x)
    filename = '%s/%s.png' % (directory, y)
    if(not os.path.exists(directory)):
        os.makedirs(directory)

    (S,W,N,E) = tileEdges(x,y,z)

    # Download the data
    #URL = 'http://dev.openstreetmap.org/~ojw/api/?/map/%d/%d/%d' % (z,x,y)
    #URL = 'http://map02.eniro.com/geowebcache/service/tms1.0.0/map/%s/%s/%s.png' % (z,x,y)
    #URL = 'http://%s/api/0.6/map?bbox=%f,%f,%f,%f' % ('api.openstreetmap.org',W,S,E,N)
    URL = 'http://c.tile.openstreetmap.org/%s/%s/%s.png' % (z, x, y)
    print URL
     
    if(not os.path.exists(filename)): # TODO: allow expiry of old data
        print "Downloading %d/%d/%d from network" % (z,x,y)
        urlretrieve(URL, filename)
    return(filename)


if __name__ == "__main__":
    bbox = (58.258000000000003, 15.282, 58.539000000000001, 15.976000000000001)

    zoom_level = 10
    scalr = 100.0
    for lat in range(bbox[0]*scalr, bbox[2]*scalr):
      lat /= scalr
      for long in range(bbox[1]*scalr, bbox[3]*scalr):
        long /= scalr
        (x, y) = tileXY(lat, long, zoom_level)
        GetOsmTileData(zoom_level, x, y)


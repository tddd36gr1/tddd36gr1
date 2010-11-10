#coding=utf8

def pushStart():
    import db
    from class_.base_objects import Mission, StatusCode
    import networkcomponent
    
    for statuscode in db.get_all(StatusCode):
        networkcomponent.send('192.168.2.15', statuscode, 'dbObject')
        
    for mission in db.get_all(Mission):
        networkcomponent.send('192.168.2.15', mission, 'dbObject')
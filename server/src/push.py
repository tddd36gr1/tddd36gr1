#coding=utf8

def pushStart():
    from class_.base_objects import Mission, StatusCode
    import networkcomponent
    import db

    ip = '127.0.0.1'
    
    #Send all status codes
    for statuscode in db.get_all(StatusCode):
        networkcomponent.send(ip,statuscode,'dbObject')
        
    #Send all missions
    for mission in db.get_all(Mission):
        networkcomponent.send(ip,mission,'dbObject')

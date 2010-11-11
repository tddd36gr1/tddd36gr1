#coding=utf8

def pushStart():
    from class_.base_objects import Mission, StatusCode
    import networkcomponent
    import db

    ip = '192.168.2.15'
    
    #Send all status codes
    for statuscode in db.get_all(StatusCode):
        networkcomponent.send(ip,statuscode,'db_add')
        
    #Send all missions
    for mission in db.get_all(Mission):
        networkcomponent.send(ip,mission,'db_add')

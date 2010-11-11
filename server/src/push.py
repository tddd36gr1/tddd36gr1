#coding=utf8

def pushStart():
    from class_.base_objects import Mission, StatusCode
    import networkcomponent
    import db
   
    #networkcomponent.send('127.0.0.1', Employee('aasdasd', 'f', 'asd'), 'fail')

    ip = '127.0.0.1'
    
    for statuscode in db.get_all(StatusCode):
        networkcomponent.send(ip,statuscode,'dbObject')
        
    for mission in db.get_all(Mission):
        networkcomponent.send(ip,mission,'dbObject')

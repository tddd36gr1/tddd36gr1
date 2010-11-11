#coding=utf8

def pushStart():
    from class_.base_objects import Employee, Mission, StatusCode
    import networkcomponent
    import db
   
    #networkcomponent.send('127.0.0.1', Employee('aasdasd', 'f', 'asd'), 'fail')
    
    for statuscode in db.get_all(StatusCode):
        networkcomponent.send('127.0.0.1',statuscode,'dbObject')
        print 'statuscode'
        
    for mission in db.get_all(Mission):
        networkcomponent.send('127.0.0.1',mission,'dbObject')

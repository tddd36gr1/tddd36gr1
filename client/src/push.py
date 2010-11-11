#coding=utf8

def pushStart():
    from class_.base_objects import Mission, StatusCode, Employee
    import networkcomponent
    import db

    ip = '127.0.0.1'
    
    #Send all status codes
    for statuscode in db.get_all(StatusCode):
        networkcomponent.send(ip,statuscode,'db_add_or_update')
        
    #Send all missions
    for mission in db.get_all(Mission):
        networkcomponent.send(ip,mission,'db_add_or_update')
    
    #Send all employees
    for employee in db.get_all(Employee): 
        networkcomponent.send(ip,employee,'db_add_or_update')
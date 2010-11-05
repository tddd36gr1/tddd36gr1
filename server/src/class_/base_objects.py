class Employee(object):
    def __init__(self, n810mac, fname, lname):
        self.fname = fname
        self.lname = lname
        self.n810mac = n810mac
        
    def __repr__(self):
        return "<Employee>\n\t<n810mac>%s</n810mac>\n\t<fname>%s</fname>\n\t<lname>%s</lname>\n</Employee>" % (self.n810mac, self.fname, self.lname)
    
class Mission(object):
    def __init__(self, n810mac, fname, lname):
        self.fname = fname
        self.lname = lname
        self.n810mac = n810mac
        
    def __repr__(self):
        return "<Employee>\n\t<n810mac>%s</n810mac>\n\t<fname>%s</fname>\n\t<lname>%s</lname>\n</Employee>" % (self.n810mac, self.fname, self.lname)

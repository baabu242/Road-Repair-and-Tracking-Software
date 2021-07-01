

class Complaint:
    def __init__(self,id = '',branch = '',loc = '',desc = ''):
        self.id=id
        self.Branch=branch
        self.Location=loc
        self.Description=desc
        self.Supervised=False
        self.Priority=0
        self.Damage_severity=0
        self.Resources_reqd=(0,0,0)

    def updateComplaint(self, priority, damage, resources):
        self.Supervised = True
        self.Priority = priority
        self.Damage_severity = damage
        self.Resources_reqd = resources

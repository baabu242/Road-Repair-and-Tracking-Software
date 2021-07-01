class user:
    id = ""
    password = ""

    def __init__(self, id, password=""):
        self.id = id
        self.password = password
        print("object constructed")

    def setID(self, id):
        self.id = id

    def setPassword(self, password):
        self.password = password
        print("password set to " + password)

    def getID(self):
        return self.id

    def getPassword(self):
        return self.password

    def checkPassword(self, password):
        if self.password == password:
            return True
        else:
            return False


class Resources:
    laborers = 0
    road_rollers = 0
    asphalt_pavers = 0
    Bitumen = 0  # units in kgs

    def __init__(self, l=0, r=0, a=0, b=0):
        self.laborers = l
        self.road_rollers = r
        self.asphalt_pavers = a
        self.Bitumen = b

    def updateResources(self, l=0, r=0, a=0, b=0):
        self.laborers = l
        self.road_rollers = r
        self.asphalt_pavers = a
        self.Bitumen = b
        print("Resources updated")


class Complaint:
    id = ""
    Branch = ""
    Road = ""
    Location = ""
    Description = ""
    Supervised = False
    Priority = 0
    Damage_severity = 0
    Resources_reqd = Resources(0, 0, 0)

    def __init__(self, id, road="", branch="", loc="", desc=""):
        self.id = id
        self.Road = road
        self.Branch = branch
        self.Location = loc
        self.Description = desc
        self.Supervised = False
        self.Priority = 0
        self.Damage_severity = 0
        self.Resources_reqd = Resources(0, 0, 0)

    def registerComplaint(self, id, road, branch, loc, desc):
        self.id = id
        self.Road = road
        self.Branch = branch
        self.Location = loc
        self.Description = desc
        self.Supervised = False
        self.Priority = 0
        self.Damage_severity = 0
        self.Resources_reqd = Resources(0, 0, 0)
        print("complaint is registered")

    def updateComplaint(self, priority, damage, resources):
        self.Supervised = True
        self.Priority = priority
        self.Damage_severity = damage
        self.Resources_reqd = resources
        print("complaint supervised")


if __name__ == "__main__":
    id = 1
    person = user(id)
    password = "abc123"
    # checking setPassword()
    print("1.1 checking setPassword()")
    person.setPassword(password)
    if person.getPassword() == password:
        print("PASS")
    else:
        print("FAIL")
    # checkPassword()
    print("\n1.2checking checkPassword()")
    # inputpassword="abc123"
    result = person.checkPassword("abc123")
    if result == True:
        print("Password is verified :" + str(result))
        print("PASS")
    else:
        print("FAIL")

    # checking registerComplaint()
    print("\n2.1 checking registerComplaint()")
    cid = 1
    complaint1 = Complaint(cid)
    iroad = "abc Road"
    iloc = "xyz colony"
    ibranch = "3"
    idesc = "potholes"
    complaint1.registerComplaint(cid, iroad, ibranch, iloc, idesc)
    if complaint1.Road == iroad and complaint1.Location == iloc and complaint1.Branch == ibranch and complaint1.Description == idesc:
        print("Complaint is created succesfully with:")
        print("\tRoad: " + complaint1.Road)
        print("\tLocation: " + complaint1.Location)
        print("\tBranch: " + complaint1.Branch)
        print("\tDescription: " + complaint1.Description)
        print("PASS")
    else:
        print("FAIL")

    # checking updateComplaint()
    print("\n2.2 checking updateComplaint()")
    priority = 4
    damage = 3
    # resources reqd
    road_rollers = 1
    asphalt_pavers = 3
    laborers = 10
    bitumen = 200  # kgs
    resources = Resources(laborers, road_rollers, asphalt_pavers, bitumen)
    complaint1.updateComplaint(priority, damage, resources)
    if complaint1.Priority == priority and complaint1.Damage_severity == damage and complaint1.Resources_reqd == resources:
        print("\tcomplaint is successfully updated with:")
        print("\tpriority=" + str(complaint1.Priority))
        print("damage=" + str(complaint1.Damage_severity))
        print("Resources_reqd:")
        print("\troad_rollers=" + str(complaint1.Resources_reqd.road_rollers))
        print("\tasphalt_pavers=" + str(complaint1.Resources_reqd.asphalt_pavers))
        print("\tWorkers=" + str(complaint1.Resources_reqd.laborers))
        print("\tBitumen(kgs)=" + str(complaint1.Resources_reqd.Bitumen))
        print("PASS")
    else:
        print("FAIL")

    # checking updateResources()
    print("\n3.1 checking updateResources()")
    road_rollers = 16
    asphalt_pavers = 10
    laborers = 110
    bitumen = 5000  # kgs
    resources.updateResources(laborers, road_rollers, asphalt_pavers, bitumen)
    if resources.asphalt_pavers == asphalt_pavers and resources.road_rollers == road_rollers and resources.laborers == laborers and resources.Bitumen == bitumen:
        print("Resources been updated succesfully with:")
        print("\tRroad_rollers=" + str(resources.road_rollers))
        print("\tAsphalt_pavers=" + str(resources.asphalt_pavers))
        print("\tWorkers=" + str(resources.laborers))
        print("\tBitumen(kgs)=" + str(resources.Bitumen))
        print("PASS")
    else:
        print("FAIL")
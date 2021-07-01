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
class user:

   def __init__(self, id = '', branch='', password = '', type = ''):
       self.__id = id
       self.__password = password
       self.__type = type
       self.__branch = branch

   def setID(self, id):
       self.__id = id

   def setPassword(self, password):
       self.__password = password

   def getID(self):
       return self.__id

   def getPassword(self):
       return self.__password

class Clerk(user):

   def __init__(self, id,branch, password):
       super().__init__(id,branch, password)


class Administrator(user):
    def __init__(self, id,branch, password):
        super().__init__(id,branch, password)

    def addEmploy(self, id, job):
        if job == 'supervisor':
            # add id to supervisor list
            pass
        elif job == 'clerk':
            # add id to clerk list
            pass


class Supervisor(user):

   def __init__(self, id,branch, password):
       super().__init__(id,branch,  password)


from random import randint
import uuid

class FamilyStructure:
    
    def __init__(self, last_name):
        self.last_name = last_name
        # example list of members
        self._members = [{
            "id": self._generateId(),
            "first_name": "John",
            "last_name": last_name
        }]
        
    def __init__(self, last_name):
        self.last_name = last_name
        self._members = []

    def _generateId(self):
        return randint(0, 99999999)

    def add_member(self, member):
        member["last_name"]= self.last_name
        member["id"] = self._generateId()
        self._members.append(member)


    def delete_member(self, id):
        for member in self._members:
            if member.get("id") == id:
                return self._members.remove(member)
        else:
            return None
        
    def get_member(self, id):
        for member in self._members:
            if member.get("id") == id:
                return member
        else:
            return None

    def get_all_members(self):
        return self._members
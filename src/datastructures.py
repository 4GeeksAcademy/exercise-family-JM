
"""
update this file to implement the following already declared methods:
- add_member: Should add a member to the self._members list
- delete_member: Should delete a member from the self._members list
- update_member: Should update a member from the self._members list
- get_member: Should return a member from the self._members list
"""
from random import randint

class FamilyStructure:
    def __init__(self,  last_name):
        self.last_name = last_name
        self._next_id = 4
        self._members = []

    # read-only: Use this method to generate random members ID's when adding members into the list
    def _generateId(self):
        generated_id = self._next_id
        self._next_id += 1
        return generated_id

    # def add_member(self, member):
    #     self._members.append(member)
    #     return member

    def add_member(self, member):
    # Asegurarse que el miembro tiene todos los campos requeridos
        required_fields = ['first_name', 'age', 'lucky_numbers', 'id']
        if all(field in member for field in required_fields):
            self._members.append(member)
            return True
        return False
    
    # def delete_member(self, id):
    #      for member in self._members:
    #          if member['id']==id:
    #              self._members.remove(member)
    #              return True
    #      return False

    def delete_member(self, id):
        for i, member in enumerate(self._members):
            if member['id'] == id:
                del self._members[i]
                return True
        return False
  
    def get_member(self, id):
        for member in self._members:
            if member['id']==id:
                return member
        return None
    
    def update_member(self, id, update_data):
        member = self.get_member(id)
        if member:
            # Prevent changing ID and last_name
            if 'id' in update_data:
                del update_data['id']
            if 'last_name' in update_data:
                del update_data['last_name']
            member.update(update_data)
            return True
        return False

    
    # this method is done, it returns a list with all the family members
    def get_all_members(self):
        return self._members

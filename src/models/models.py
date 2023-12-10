from flask_login import UserMixin
from aclimate_orm import Users, Roles

class User(UserMixin):
    def __init__(self, user_obj):
        self.user_obj = user_obj

    @staticmethod
    def get(user_id):
        user_obj = Users.objects(UserName=user_id).using('db2').first()
        print(user_obj['Roles'])
        if user_obj:
            return User(user_obj)
        return None

    def check_password(self, password):
        return self.user_obj.PasswordHash == password

    def get_id(self):
        return str(self.user_obj.UserName)
    
    def is_admin(self):
        user_roles_ids = self.user_obj['Roles']
        
        roles = Roles.objects(_id__in=user_roles_ids).using('db2')

        for role in roles:
            print(role.Name)

            if role.Name == 'ADMIN':
                return True
        
        return False

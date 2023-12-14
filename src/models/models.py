from flask_login import UserMixin
from aclimate_orm import Users, Roles
import os
from hashlib import pbkdf2_hmac, sha1
import base64

PBKDF2_ITER_COUNT = 1000
PBKDF2_SUBKEY_LENGTH = 256 // 8  
SALT_SIZE = 128 // 8  

class User(UserMixin):
    def __init__(self, user_obj):
        self.user_obj = user_obj

    @staticmethod
    def get(user_id):
        user_obj = Users.objects(UserName=user_id).using('db2').first()
        if user_obj:
            return User(user_obj)
        return None

    def check_password(self, password):
        hashed_password_bytes = base64.b64decode(self.user_obj.PasswordHash.encode('utf-8'))

        if len(hashed_password_bytes) != (1 + SALT_SIZE + PBKDF2_SUBKEY_LENGTH) or hashed_password_bytes[0] != 0x00:
            return False

        salt = hashed_password_bytes[1:1+SALT_SIZE]
        stored_subkey = hashed_password_bytes[1+SALT_SIZE:]

        generated_subkey = pbkdf2_hmac('sha1', password.encode('utf-8'), salt, PBKDF2_ITER_COUNT, dklen=PBKDF2_SUBKEY_LENGTH)
        return stored_subkey == generated_subkey

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

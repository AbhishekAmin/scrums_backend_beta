from flask import g
from mongoengine import DynamicDocument, StringField, GenericReferenceField, ListField
from passlib.apps import custom_app_context as pwd_context


class User(DynamicDocument):
    email = StringField(unique=True)
    password = StringField()
    profile_pic = StringField()
    pinned_board = ListField(GenericReferenceField())


    def encrypt_set_password(self, password):
        self.password = pwd_context.encrypt(password)

    @staticmethod
    def authenticate(email, password):
        user = User.objects(email=email).first()
        if user:
            user.id = str(user.id)
            if pwd_context.verify(password, user.password):
                return user
        return None

    @staticmethod
    def identity(payload):
        user = User.objects(id=payload['identity']).first()
        g.user = user
        user.id = str(user.id)
        return user

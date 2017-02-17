from mongoengine import DynamicDocument, StringField, ReferenceField, ListField

from .task import Task
from .user import User


class Board(DynamicDocument):
	admin = ReferenceField(User)
	header = StringField()
	tasks = ListField(ReferenceField(Task))
	members = ListField(ReferenceField(User), default=[])

from datetime import datetime

from mongoengine import DynamicDocument, StringField, ReferenceField, ListField, DateTimeField

from .user import User


class Task(DynamicDocument):
	title = StringField()
	description = StringField()
	attachments = ListField(StringField(), default=[])
	status = StringField(default="to-do")
	AssignedTo = ListField(ReferenceField(User, default=[]))
	tags = ListField(StringField(), default=[])
	deadline = DateTimeField(default=datetime.now())
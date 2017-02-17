from mongoengine import connect

from constants import DB_URI


connect('scrums', host=DB_URI)
print('Connection established.')
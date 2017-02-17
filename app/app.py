from datetime import timedelta

from flask import Flask, request, redirect, jsonify
from flask_reqparse import RequestParser
from flask_jwt import JWT, jwt_required

import connector
from constants import APP_SECRET_KEY
from models.user import User
from models.board import Board
from models.task import Task


app = Flask(__name__)
jwt = JWT(app, User.authenticate, User.identity)
parser = RequestParser()


app.config['SECRET_KEY'] = APP_SECRET_KEY
app.config['JWT_SECRET_KEY'] = APP_SECRET_KEY
app.config['JWT_EXPIRATION_DELTA'] = timedelta(days=1)


@app.route('/')
def index():
    return jsonify({'response': 'Server is up and running bitch!'})



@app.route('/auth/register', methods=['POST'])
@parser.validate_arguments([
	{
		"name" : "username",
		"type" : str,
		"source" : "json",
		"required" : True
	},
	{
		"name" : "email",
		"type" : str,
		"source" : "json",
		"required" : True
	},
	{
		"name" : "password",
		"type" : str,
		"source" : "json",
		"required" : True
	},
	{
		"name" : "profile_pic_url",
		"type" : str,
		"source" : "json",
		"required" : False
	}
])
def register(args):
    """
        REGISTER
    """
	user_object = User()
	user_object.username = args['username']
	user_object.email = args['email']
	user_object.encrypt_set_password(args['password'])
	#user_object.profile_pic_url = args['profile_pic_url']
	user_object.save()

	return jsonify({
		"response" : "Registered successfully.",
		"User_id" : str(user_object.id),
		"email" : user_object.email,
		#"profile_pic_url" : user_object.profile_pic_url
	})


#board
#create board
@app.route('/api/board/', methods=['POST'])
@parser.validate_arguments([
	{
		"name" : "header",
		"type" : str,
		"source" : "json",
		"required" : True
	}
])
@jwt_required()
def create_board(args):
	board_object = Board()
	board_object.header = args['header']
	board_object.admin = g.user
	board_object.save()
	return jsonify({
		"response" : "board created",
		"board_id" : str(board_object.id)
	})


@app.route('/api/board/<board_id>', methods=['GET'])
def find_board(board_id):
	
	return jsonify({
		"response" : "boards"
	})


#Tasks
#create tasks
@app.route('/api/task', methods=['POST'])
@parser.validate_arguments([
	{
		"name" : "title",
		"type" : str,
		"source" : "json",
		"required" : True
	},
	{
		"name" : "description",
		"type" : str,
		"source" : "json",
		"required" : True
	},
	{
		"name" : "attachments",
		"type" : list,
		"source" : "json",
		"required" : False
	},
	{
		"name" : "tags",
		"type" : list,
		"source" : "json",
		"required" : False
	},
	{
		"name" : "status",
		"type" : str,
		"source" : "json",
		"required" : False
	},
	{
		"name" : "AssignedTo",
		"type" : list,
		"source" : "json",
		"required" : False
	}
])
@jwt_required()
def create_task(args):
	task_object = Task()
	task_object.title = args['title']
	task_object.description = args['description']
	#import pdb; pdb.set_trace()
	if "status" in args:
		task_object.status = args['status']
	if "AssignedTo" in args:
		task_object.AssignedTo = args['AssignedTo']
	if "tags" in args:
		task_object.tags = args['tags']
	if "attachments" in args:
		task_object.attachments = args['attachments']
	task_object.save()
	return jsonify({
		"response" : "Task created.",
		"task_id" : str(task_object.id),
		"title" : task_object.title,
		"description" : task_object.description,
		"deadline" : task_object.deadline,
		"status" : task_object.status,
		"AssignedTo" : task_object.AssignedTo
	})


if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0')

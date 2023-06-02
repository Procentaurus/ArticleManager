from customUser.models import MyUser
from ..models import *

def sample_user(username, email, isEditor=False):
	sample = {
		"username": username,
		"email": email,
		"password": "123456PIOTR",
		"isEditor": isEditor
    }
	return MyUser.objects.create(**sample)

def sample_comment_json(author, text, body, creationDate):
	sample = {
		"author": author.username,
		"text": text.id,
		"body": body,
		"creationDate": creationDate
    }
	return sample

def sample_comment(author, text, body, creationDate):
	sample = {
		"author": author,
		"text": text,
		"body": body,
		"creationDate": creationDate
    }
	return Comment.objects.create(**sample)

def sample_text_json(author, project, body, creationDate):
	sample = {
		"author": author.username,
		"project": project.name,
		"body": body,
		"creationDate": creationDate
    }
	return sample
    
def sample_text(author, project, body, creationDate):
	sample = {
		"author": author,
		"project": project,
		"body": body,
		"creationDate": creationDate
    }
	return Text.objects.create(**sample)

def sample_project_json(name, manager, writers, startDate, isFinished=False):	
	sample = {
		"name": name,
		"manager": manager.username,
		"writers": [writer.username for writer in writers],
		"startDate": startDate,
		"isFinished": isFinished	
    }
	return sample

def sample_project(name, manager, writers, startDate, isFinished=False):
	sample = {
		"name": name,
		"manager": manager,
		"startDate": startDate,
		"isFinished": isFinished	
    }
	project = Project.objects.create(**sample)
	project.writers.set(writers)	
	return project

    
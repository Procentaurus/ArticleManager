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

def sample_comment_json(text, body, author):
	sample = {
		"text": text.id,
		"body": body,
		"author":author.username
    }
	return sample

def sample_comment(text, body, author):
	sample = {
		"text": text,
		"body": body,
		"author":author
    }
	return Comment.objects.create(**sample)

def sample_text_json(project, body, author):
	sample = {
		"project": project.name,
		"body": body,
		"author":author.username
    }
	return sample
    
def sample_text(project, body, author):
	sample = {
		"project": project,
		"body": body,
		"author":author
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

    
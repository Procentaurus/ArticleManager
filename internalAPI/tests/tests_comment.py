from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from datetime import date

from .samples import *


def get_list_url():
	return reverse('comment_list')

def get_detail_url(id):
	return reverse('comment_detail', args=[id])


class CommentListTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.editor = sample_user("xxxxxxxxxx","e@wp.pl", True)
        self.author = sample_user("yyyyyyyyyy", "n@wp.pl")
        self.normal = sample_user("wwwwwwwww", "w@wp.pl")
        self.project = sample_project("asd",self.author,[self.author], date.today())
        self.text = sample_text(self.author,self.project,"asdasdasdasdasdasdasdasd", date.today())

        self.editor.save()
        self.normal.save()
        self.author.save()

        self.project.save()
        self.text.save()
        
    def tearDown(self):
        self.editor.delete()
        self.normal.delete()
        self.author.delete()

        self.project.delete()
        self.text.delete()


    # check get method
    def test_get_all_comments_authenticated_project_member(self):
        self.client.force_authenticate(user=self.author)

        res = self.client.get(get_list_url())

        self.assertEqual(res.status_code, status.HTTP_200_OK)


    def test_get_all_comments_authenticated_not_projectmember(self):
        self.client.force_authenticate(user=self.normal)

        res = self.client.get(get_list_url())

        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_get_all_comments_unauthenticated(self):
        res = self.client.get(get_list_url())

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


    # ckeck post method
    def test_post_comment_unauthenticated(self):
        data = sample_comment_json(self.author,self.text,"asdasdasdasdasdasdasdasd", date.today())

        res = self.client.post(get_list_url(), data, format='json')

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_post_comment_authenticated_editor_right_input(self):
        data = sample_comment_json(self.editor,self.text,"asdasdasdasdasdasdasdasd", date.today())
        self.client.force_authenticate(user=self.editor)

        res = self.client.post(get_list_url(), data, format='json')

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_post_comment_authenticated_projectmember_right_input(self):
        data = sample_comment_json(self.author,self.text,"asdasdasdasdasdasdasdasd", date.today())
        self.client.force_authenticate(user=self.author)

        res = self.client.post(get_list_url(), data, format='json')

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)


    def test_post_comment_authenticated_not_projectmember_right_input(self):
        data = sample_comment_json(self.normal,self.text,"asdasdasdasdasdasdasdasd", date.today())
        self.client.force_authenticate(user=self.normal)

        res = self.client.post(get_list_url(), data, format='json')

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_post_comment_authenticated_too_long_input(self):
        body_too_long = "shit"
        for _ in range(100):
             body_too_long += "1234567890"
        data = sample_comment_json(self.author,self.text,body_too_long, date.today())
        self.client.force_authenticate(user=self.author)

        res = self.client.post(get_list_url(), data, format='json')

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)




class CommentDetailTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.editor = sample_user("xxxxxxxxxx","e@wp.pl", True)
        self.author = sample_user("yyyyyyyyyy", "n@wp.pl")
        self.normal = sample_user("wwwwwwwww", "w@wp.pl")
        self.project_manager = sample_user("zzzzzzzzz", "z@wp.pl")
        self.project = sample_project(sample_project_json("asd",self.project_manager,[self.project_manager, self.author, self.normal], date.today()))
        self.text = sample_text(sample_text_json(self.author,self.project,"asdasdasdasdasdasdasdasd"))

        self.editor.save()
        self.normal.save()
        self.author.save()
        self.project_manager()

        self.project.save()
        self.text.save()
        
    def tearDown(self):
        self.editor.delete()
        self.normal.delete()
        self.author.delete()
        self.project_manager.delete()

        self.project.delete()
        self.text.delete()

    
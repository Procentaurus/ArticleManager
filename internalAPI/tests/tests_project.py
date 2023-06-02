from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from datetime import date

from .samples import *


def get_list_url():
	return reverse('text_list')

def get_detail_url(id):
	return reverse('text_detail', args=[id])


class CommentListTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.editor = sample_user("xxxxxxxxxx","e@wp.pl", True)
        self.author = sample_user("yyyyyyyyyy", "n@wp.pl")
        self.normal = sample_user("wwwwwwwww", "w@wp.pl")
        self.project = sample_project("asd",self.author,[self.author], date.today())
        self.text = sample_text(self.project, "asdasdasdasdasdasdasdasd", self.author)

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
        data = sample_comment_json(self.text,"asdasdasdasdasdasdasdasd", self.author)

        res = self.client.post(get_list_url(), data, format='json')

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_post_comment_authenticated_editor_right_input(self):
        data = sample_comment_json(self.text,"asdasdasdasdasdasdasdasd", self.author)
        self.client.force_authenticate(user=self.editor)

        res = self.client.post(get_list_url(), data, format='json')

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_post_comment_authenticated_projectmember_right_input(self):
        data = sample_comment_json(self.text,"asdasdasdasdasdasdasdasd", self.author)
        self.client.force_authenticate(user=self.author)

        res = self.client.post(get_list_url(), data, format='json')

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)


    def test_post_comment_authenticated_not_projectmember_right_input(self):
        data = sample_comment_json(self.text,"asdasdasdasdasdasdasdasd", self.author)
        self.client.force_authenticate(user=self.normal)

        res = self.client.post(get_list_url(), data, format='json')

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_post_comment_authenticated_too_long_input(self):
        body_too_long = "shit"
        for _ in range(100):
             body_too_long += "1234567890"
        data = sample_comment_json(self.text,body_too_long, self.author)
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
        self.project = sample_project("asd",self.project_manager,[self.project_manager, self.author], date.today())
        self.text = sample_text(self.project,"asdasdasdasdasdasdasdasd", self.author)
        self.comment = sample_comment(self.text, "ajshdfbasmhdgfvbasmdjghfvbzsdjhcvbasd", self.author)

        self.editor.save()
        self.normal.save()
        self.author.save()
        self.project_manager.save()

        self.project.save()
        self.text.save()
        self.comment.save()
        
    def tearDown(self):
        self.editor.delete()
        self.normal.delete()
        self.author.delete()
        self.project_manager.delete()

        self.comment.delete()
        self.text.delete()
        self.project.delete()


    # checking delete method
    def test_delete_comment_unauthenticated(self):
        res = self.client.delete(get_detail_url(self.comment.id))

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_publication_editor(self):
        self.client.force_authenticate(user=self.editor)

        res = self.client.delete(get_detail_url(self.comment.id))

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_publication_author(self):
        self.client.force_authenticate(user=self.author)

        res = self.client.delete(get_detail_url(self.comment.id))

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_publication_projectmanager(self):
        self.client.force_authenticate(user=self.project_manager)

        res = self.client.delete(get_detail_url(self.comment.id))

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

    # checking get method
    def test_get_comment_unauthenticated(self):
        res = self.client.get(get_detail_url(self.comment.id))

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_comment_author(self):
        self.client.force_authenticate(user=self.author)

        res = self.client.get(get_detail_url(self.comment.id))

        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_get_comment_not_projectmember(self):
        self.client.force_authenticate(user=self.normal)

        res = self.client.get(get_detail_url(self.comment.id))

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_comment_editor(self):
        self.client.force_authenticate(user=self.editor)

        res = self.client.get(get_detail_url(self.comment.id))

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


    # checking patch method
    def test_patch_comment_unauthenticated(self):
        sample = sample_comment_json(self.text, "ajshdfbasmhdgfvbasmdjghfvbzsdjhcvbasd", self.author)

        res = self.client.patch(get_detail_url(self.comment.id), sample, format='json')

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_patch_comment_editor(self):
        self.client.force_authenticate(user=self.editor)
        sample = sample_comment_json(self.text, "asd", self.author)

        res = self.client.patch(get_detail_url(self.comment.id), sample, format='json')

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_patch_comment_author_right_input(self):
        self.client.force_authenticate(user=self.author)
        sample = sample_comment_json(self.text, "asd", self.author)

        res = self.client.patch(get_detail_url(self.comment.id), sample, format='json')

        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_patch_comment_author_input_too_long(self):
        self.client.force_authenticate(user=self.author)
        body_too_long = "shit"
        for _ in range(100):
             body_too_long += "1234567890"
        sample = sample_comment_json(self.text, body_too_long, self.author)

        res = self.client.patch(get_detail_url(self.comment.id), sample, format='json')

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_patch_comment_not_project_member(self):
        self.client.force_authenticate(user=self.normal)
        sample = sample_comment_json(self.text, "asdsdasdasd", self.author)

        res = self.client.patch(get_detail_url(self.comment.id), sample, format='json')

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
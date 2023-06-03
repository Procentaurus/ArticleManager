from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from datetime import date, timedelta

from .samples import *


def get_list_url():
	return reverse('project_list')

def get_detail_url(name):
	return reverse('project_detail', args=[name])


class ProjectListTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.editor = sample_user("xxxxxxxxxx","e@wp.pl", True)
        self.normal = sample_user("wwwwwwwww", "wasas@wp.pl")

        self.editor.save()
        self.normal.save()

    def tearDown(self):
        self.editor.delete()
        self.normal.delete()


    # check get method
    def test_get_all_projects_authenticated_not_editor(self):
        self.client.force_authenticate(user=self.normal)

        res = self.client.get(get_list_url())

        self.assertEqual(res.status_code, status.HTTP_200_OK)


    def test_get_all_projects_authenticated_editor(self):
        self.client.force_authenticate(user=self.editor)

        res = self.client.get(get_list_url())

        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_get_all_projects_unauthenticated(self):
        res = self.client.get(get_list_url())

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


    # ckeck post method
    def test_post_project_unauthenticated(self):
        data = sample_project_json("ajhhdgf", self.normal, [self.normal], date.today())

        res = self.client.post(get_list_url(), data, format='json')

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_post_project_editor_right_input(self):
        data = sample_project_json("ajhhdgsadf", self.normal, [self.normal], date.today())
        self.client.force_authenticate(user=self.editor)

        res = self.client.post(get_list_url(), data, format='json')

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_post_project_not_editor(self):
        data = sample_project_json("ajhhdgf", self.normal, [self.normal], date.today())
        self.client.force_authenticate(user=self.normal)

        res = self.client.post(get_list_url(), data, format='json')

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


    def test_post_project_editor_too_long_input(self):
        name_too_long = "shit"
        for _ in range(100):
             name_too_long += "1234567890"
        data = sample_project_json(name_too_long, self.normal, [self.normal], date.today())
        self.client.force_authenticate(user=self.editor)

        res = self.client.post(get_list_url(), data, format='json')

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)



class ProjectDetailTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.editor = sample_user("xxxxxxxxxx","e@wp.pl", True)
        self.normal = sample_user("wwwwwwwww", "wasas@wp.pl")
        self.project_manager = sample_user("zzzzzzzzz", "sas@wp.pl")
        self.project_member = sample_user("aaaaaaaaa", "saqews@wp.pl")
        self.project = sample_project("dadsdasdasd",self.project_manager,[self.project_member], date.today())

        self.editor.save()
        self.normal.save()
        self.project_member.save()
        self.project_manager.save()

        self.project.save()

    def tearDown(self):
        self.editor.delete()
        self.normal.delete()
        self.project_manager.delete()
        self.project_member.delete()

        self.project.delete()


    # checking delete method
    def test_delete_project_unauthenticated(self):
        res = self.client.delete(get_detail_url(self.project.name))

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_project_editor(self):
        self.client.force_authenticate(user=self.editor)

        res = self.client.delete(get_detail_url(self.project.name))

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_project_normal(self):
        self.client.force_authenticate(user=self.normal)

        res = self.client.delete(get_detail_url(self.project.name))

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_project_projectmanager(self):
        self.client.force_authenticate(user=self.project_manager)

        res = self.client.delete(get_detail_url(self.project.name))

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_project_project_member(self):
        self.client.force_authenticate(user=self.project_member)

        res = self.client.delete(get_detail_url(self.project.name))

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


    # checking get method
    def test_get_project_unauthenticated(self):
        res = self.client.get(get_detail_url(self.project.name))

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_project_editor(self):
        self.client.force_authenticate(user=self.editor)

        res = self.client.get(get_detail_url(self.project.name))

        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_get_project_projectmanager(self):
        self.client.force_authenticate(user=self.project_manager)

        res = self.client.get(get_detail_url(self.project.name))

        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_get_project_projectmember(self):
        self.client.force_authenticate(user=self.project_member)

        res = self.client.get(get_detail_url(self.project.name))

        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_get_project_normal(self):
        self.client.force_authenticate(user=self.normal)

        res = self.client.get(get_detail_url(self.project.name))

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


    # checking patch method
    def test_patch_project_unauthenticated(self):
        sample = sample_project_json("self......project", self.project_manager,[self.project_manager], date.today()-timedelta(weeks=4))

        res = self.client.patch(get_detail_url(self.project.name), sample, format='json')

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_patch_project_editor(self):
        self.client.force_authenticate(user=self.editor)
        sample = sample_project_json("self......project", self.project_manager,[self.project_manager], date.today()-timedelta(weeks=4))

        res = self.client.patch(get_detail_url(self.project.name), sample, format='json')

        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_patch_project_projectmanager(self):
        self.client.force_authenticate(user=self.project_manager)
        sample = sample_project_json("self......project", self.project_manager,[self.project_manager], date.today()-timedelta(weeks=4))

        res = self.client.patch(get_detail_url(self.project.name), sample, format='json')

        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_patch_project_editor_name_too_long(self):
        self.client.force_authenticate(user=self.editor)
        name_too_long = "shit"
        for _ in range(50):
            name_too_long += "1234567890"
        sample = sample_project_json(name_too_long, self.project_manager,[self.project_manager], date.today()-timedelta(weeks=4))

        res = self.client.patch(get_detail_url(self.project.name), sample, format='json')

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_patch_project_not_projectmember(self):
        self.client.force_authenticate(user=self.normal)
        sample = sample_project_json("self......project", self.project_manager,[self.project_manager], date.today()-timedelta(weeks=4))

        res = self.client.patch(get_detail_url(self.project.name), sample, format='json')

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


    def test_patch_project_projectmember(self):
        self.client.force_authenticate(user=self.project_member)
        sample = sample_project_json("self......project", self.project_manager,[self.project_manager], date.today()-timedelta(weeks=4))

        res = self.client.patch(get_detail_url(self.project.name), sample, format='json')

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
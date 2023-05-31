from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse

from externalAPI.models import Publication
from customUser.models import MyUser
from externalAPI.views import *

def get_list_url():
	return reverse('publication_list')

def get_detail_url(title):
	return reverse('publication_detail', args=[title])

def sample_user(username, email, isEditor=False):
	sample = {
		"username": username,
		"email": email,
		"password": "123456PIOTR",
		"isEditor": isEditor
    }
	return MyUser.objects.create(**sample)

def sample_publication(manager, title,body, isAvailable=True):
	sample = {
		"manager" : manager,
		"body" : body,
		"title" : title,
        "isAvailable" : isAvailable
	}
	return Publication.objects.create(**sample)

def sample_json(manager):
    data = {
        "manager": manager.username,
        "title": "Kotki i psy2",
        "body": "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
        "isAvailable": "False"
    }
    return data


class PublicationListTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.editor = sample_user("xxxxxxxxxx","e@wp.pl", True)
        self.normal = sample_user("yyyyyyyyyy", "n@wp.pl")

        self.editor.save()
        self.normal.save()
        
    def tearDown(self):
        self.editor.delete()
        self.normal.delete()


    # cheack get method
    def test_get_all_publications_unauthenticated(self):
        res = self.client.get(get_list_url())

        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_get_all_publications_authenticated(self):
        self.client.force_authenticate(user=self.normal)

        res = self.client.get(get_list_url())

        self.assertEqual(res.status_code, status.HTTP_200_OK)


    # ckeck post method
    def test_post_publication_unauthenticated(self):
        data = sample_json(self.normal)

        res = self.client.post(get_list_url(), data, format='json')

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_post_publication_authenticated(self):
        data = sample_json(self.normal)
        self.client.force_authenticate(user=self.normal)

        res = self.client.post(get_list_url(), data, format='json')

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_post_publication_editor(self):
        data = sample_json(self.normal)
        self.client.force_authenticate(user=self.editor)

        res = self.client.post(get_list_url(), data, format='json')

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)


class PublicationDetailTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.editor = sample_user("xxxxxxxxxx","e@wp.pl", True)
        self.normal = sample_user("yyyyyyyyyy", "n@wp.pl")
        self.publication = sample_publication(self.normal,"sssssssss", "dddddddddd")

        self.publication.save()
        self.editor.save()
        self.normal.save()
        
    def tearDown(self):
        self.editor.delete()
        self.normal.delete()
        self.publication.delete()


	# checking delete method
    def test_delete_publication_unauthenticated(self):
        res = self.client.delete(get_detail_url(self.publication.title))

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_publication_editor(self):
        self.client.force_authenticate(user=self.editor)

        res = self.client.delete(get_detail_url(self.publication.title))

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_publication_not_editor(self):
        self.client.force_authenticate(user=self.normal)

        res = self.client.delete(get_detail_url(self.publication.title))

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


    # checking get method
    def test_get_publication_unauthenticated(self):
        res = self.client.get(get_detail_url(self.publication.title))

        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_get_publication_authenticated(self):
        self.client.force_authenticate(user=self.normal)

        res = self.client.get(get_detail_url(self.publication.title))

        self.assertEqual(res.status_code, status.HTTP_200_OK)


    # checking patch method
    def test_patch_publication_unauthenticated(self):
        sample = sample_json(self.normal)

        res = self.client.patch(get_detail_url(self.publication.title), sample, format='json')

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_patch_publication_editor(self):
        self.client.force_authenticate(user=self.editor)
        sample = sample_json(self.normal)

        res = self.client.patch(get_detail_url(self.publication.title), sample, format='json')

        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_patch_publication_not_editor(self):
        self.client.force_authenticate(user=self.normal)
        sample = sample_json(self.normal)

        res = self.client.patch(get_detail_url(self.publication.title), sample, format='json')

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)



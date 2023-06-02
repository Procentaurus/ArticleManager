from django.test import TestCase
from django.db import IntegrityError
from ..models import Publication
from customUser.models import MyUser

class PublicationModelTest(TestCase):
    def setUp(self):
        self.user = MyUser.objects.create(username='testuser', email="test@test.pl")

    def test_publication_creation(self):
        publication = Publication.objects.create(
            manager=self.user,
            body='Publication body',
            title='Valid Title',
            isAvailable=True,
            numberOfDownloads=0
        )
        self.assertEqual(publication.id, publication.pk)
        self.assertEqual(publication.manager, self.user)
        self.assertEqual(publication.body, 'Publication body')
        self.assertEqual(publication.title, 'Valid Title')
        self.assertTrue(publication.isAvailable)
        self.assertEqual(publication.numberOfDownloads, 0)

    def test_is_available_default_value(self):
        publication = Publication.objects.create(
            manager=self.user,
            body='Publication body',
            title='Valid Title',
            numberOfDownloads=0
        )
        self.assertTrue(publication.isAvailable)

    def test_number_of_downloads_default_value(self):
        publication = Publication.objects.create(
            manager=self.user,
            body='Publication body',
            title='Valid Title',
            isAvailable=True,
        )
        self.assertEqual(publication.numberOfDownloads, 0)

    def test_unique_title_validation(self):
        publication1 = Publication.objects.create(
            manager=self.user,
            body='Publication body',
            title='Unique Title',
            isAvailable=True,
            numberOfDownloads=0
        )
        with self.assertRaises(IntegrityError):
            Publication.objects.create(
                manager=self.user,
                body='Another publication body',
                title='Unique Title',
                isAvailable=True,
                numberOfDownloads=0
            )

    def test_adding_date_auto_now_add(self):
        publication = Publication.objects.create(
            manager=self.user,
            body='Publication body',
            title='Valid Title',
            isAvailable=True,
            numberOfDownloads=0
        )
        self.assertIsNotNone(publication.addingDate)
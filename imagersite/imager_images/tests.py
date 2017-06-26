"""Tests for Imager Profile app."""

from django.conf import settings
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from imager_images.models import Photo, Album
import faker
import datetime
import factory
import os


fake = faker.Faker()


HERE = os.path.dirname(__file__)


class PhotoFactory(factory.django.DjangoModelFactory):
    """Factory for creating users."""

    class Meta:
        """."""

        model = Photo

    title = factory.Sequence(
        lambda n: 'Photo{}'.format(n)
    )
    description = fake.text(254)
    date_modified = datetime.datetime.now()
    photo = SimpleUploadedFile(
        name='example.jpg',
        content=open(os.path.join(
            HERE,
            'static',
            'jerry-kiesewetter-192478.jpg'), 'rb').read(),
        content_type='image/jpeg')


class AlbumFactory(factory.django.DjangoModelFactory):
    """Factory for creating users."""

    class Meta:
        """."""

        model = Album

    title = factory.Sequence(
        lambda n: 'Album{}'.format(n)
    )
    description = fake.text(254)
    date_modified = datetime.datetime.now()


class PhotoTestCases(TestCase):
    """."""

    def setUp(self):
        """."""
        user = User(
            username='morgan',
            email='morgan@morgan.com'
        )
        user.set_password('morgaaaaan')
        user.save()
        self.user = user
        photo = PhotoFactory.build()
        photo.user = self.user
        photo.save()
        self.photo = photo

    def test_upload_image_adds_new_photo_instance(self):
        """."""
        self.assertEqual(Photo.objects.count(), 1)

    def test_new_photo_is_private_by_default(self):
        """."""
        self.assertEqual(self.photo.published, 'PV')

    def test_delete_user_with_photos_photos_die(self):
        """."""
        self.user.delete()
        self.assertEqual(Photo.objects.count(), 0)

    def test_uploaded_photo_lives_in_media_user_photos(self):
        """."""
        upload_dir = os.path.join(settings.MEDIA_ROOT, 'user_images')
        directory_contents = os.listdir(upload_dir)
        name = self.photo.photo.name.split('/')[1]
        self.assertTrue(name in directory_contents)

    def test_can_change_uploaded_photo_privacy_setting(self):
        """."""
        self.photo.published = 'PB'
        self.assertEqual(self.photo.published, 'PB')

    def test_upload_with_different_privacy_setting(self):
        """."""
        photo = PhotoFactory.build()
        photo.user = self.user
        photo.published = 'PB'
        photo.save()
        self.photo1 = photo
        self.assertEqual(self.photo1.published, 'PB')

    def test_upload_with_shared_privacy_setting(self):
        """."""
        photo = PhotoFactory.build()
        photo.user = self.user
        photo.published = 'SH'
        photo.save()
        self.photo1 = photo
        self.assertEqual(self.photo1.published, 'SH')


class AlbumsTestCase(TestCase):
    """."""

    def setUp(self):
        """."""
        user = User(
            username='morgan',
            email='morgan@morgan.com'
        )
        user.set_password('morgaaaaan')
        user.save()
        self.user = user

        photos = [PhotoFactory.build() for i in range(20)]
        for photo in photos:
            photo.user = user
            photo.save()

        albums = [AlbumFactory.build() for i in range(5)]
        for idx, album in enumerate(albums):
            album.user = user
            album.save()
            album.photo.add(photos[idx])
            album.cover = photos[idx]
        self.albums = albums

    def test_delete_user_with_albums_albums_delete(self):
        """."""
        self.assertTrue(Album.objects.count() == 5)
        self.user.delete()
        self.assertEqual(Album.objects.count(), 0)

    def test_update_album_pv_choice(self):
        """."""
        self.albums[0].published = 'SH'
        self.assertEqual(self.albums[0].published, 'SH')

    def test_upload_with_different_privacy_setting(self):
        """."""
        album = AlbumFactory.build()
        album.user = self.user
        album.published = 'PB'
        album.save()
        self.assertEqual(album.published, 'PB')

    def test_upload_with_shared_privacy_setting(self):
        """."""
        album = AlbumFactory.build()
        album.user = self.user
        album.published = 'SH'
        album.save()
        self.assertEqual(album.published, 'SH')
"""Tests for Imager Profile app."""

from django.conf import settings
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, Client, RequestFactory
from imager_images.models import Photo, Album
from bs4 import BeautifulSoup
from imager_images.views import (
    library,
    photos_view,
    single_photo_view,
    single_album_view,
    albums_view)
import faker
import datetime
import factory
import os

fake = faker.Faker()


HERE = os.path.dirname(__file__)


class PhotoFactory(factory.django.DjangoModelFactory):
    """Factory for creating photos."""

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
    """Factory for creating albums."""

    class Meta:
        """."""

        model = Album

    title = factory.Sequence(
        lambda n: 'Album{}'.format(n)
    )
    description = fake.text(254)
    date_modified = datetime.datetime.now()


class PhotoTestModels(TestCase):
    """Test class for photo models."""

    def setUp(self):
        """Create a user and a photo."""
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
        """New photo has been created."""
        self.assertEqual(Photo.objects.count(), 1)

    def test_new_photo_is_private_by_default(self):
        """New photo has default published setting."""
        self.assertEqual(self.photo.published, 'PV')

    def test_delete_user_with_photos_photos_die(self):
        """Deleted user's photos are deleted."""
        self.user.delete()
        self.assertEqual(Photo.objects.count(), 0)

    def test_uploaded_photo_lives_in_media_user_photos(self):
        """New photo lives in the correct directory."""
        upload_dir = os.path.join(settings.MEDIA_ROOT, 'user_images')
        directory_contents = os.listdir(upload_dir)
        name = self.photo.photo.name.split('/')[1]
        self.assertTrue(name in directory_contents)

    def test_can_change_uploaded_photo_privacy_setting(self):
        """Upated published setting works."""
        self.photo.published = 'PB'
        self.assertEqual(self.photo.published, 'PB')

    def test_upload_with_different_privacy_setting(self):
        """Upload a new photo with non-default setting."""
        photo = PhotoFactory.build()
        photo.user = self.user
        photo.published = 'PB'
        photo.save()
        self.photo1 = photo
        self.assertEqual(self.photo1.published, 'PB')

    def test_upload_with_shared_privacy_setting(self):
        """Upload a new photo with non-default setting."""
        photo = PhotoFactory.build()
        photo.user = self.user
        photo.published = 'SH'
        photo.save()
        self.photo1 = photo
        self.assertEqual(self.photo1.published, 'SH')


class PhotoView(TestCase):
    """Test photo views."""

    def setUp(self):
        """."""
        user_1 = User(
            username='morgan',
            email='morgan@morgan.com'
        )
        user_2 = User(
            username='kurt',
            email='kurt@kurt.com'
        )
        user_3 = User(
            username='mcgee',
            email='mcgee@mcgee.com'
        )
        user_1.save()
        user_2.save()
        user_3.save()
        self.user_1 = user_1
        self.user_2 = user_2
        self.user_3 = user_3

        photos_1 = [PhotoFactory.build() for i in range(10)]
        for photo in photos_1:
            photo.user = user_1
            photo.published = 'PB'
            photo.save()
        photos_1[0].published = 'PV'
        photos_1[0].save()

        photos_2 = [PhotoFactory.build() for i in range(10)]
        for photo in photos_2:
            photo.user = user_2
            photo.published = 'PB'
            photo.save()

        albums = [AlbumFactory.build() for i in range(3)]
        albums[0].user = user_1
        albums[0].published = 'PB'
        albums[0].cover = photos_1[1]
        albums[1].user = user_2
        albums[1].cover = photos_2[1]
        albums[2].user = user_3
        albums[2].published = 'PB'
        albums[0].save()
        albums[1].save()
        albums[2].save()

        for photo in photos_1:
            albums[0].photos.add(photo)
            albums[0].save()

        for photo in photos_2:
            albums[1].photos.add(photo)
            albums[0].save()

        self.photos_1 = photos_1
        self.photos_2 = photos_2
        self.albums = albums
        self.client = Client()

    def test_image_count_correct(self):
        """Test img element count is equal to public images."""
        response = self.client.get(reverse('photos'))
        html = BeautifulSoup(response.content, 'html.parser')
        photos = html.find_all('img')
        self.assertEqual(len(photos), Photo.objects.filter(published='PB').count())


class AlbumsTestModels(TestCase):
    """Test class for album models."""

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
            album.photos.add(photos[idx])
            album.cover = photos[idx]
        self.albums = albums

    def test_delete_user_with_albums_albums_deleted(self):
        """Delete user deletes albums."""
        self.assertTrue(Album.objects.count() == 5)
        self.user.delete()
        self.assertEqual(Album.objects.count(), 0)

    def test_update_album_pv_choice(self):
        """Updated album published status updates."""
        self.albums[0].published = 'SH'
        self.assertEqual(self.albums[0].published, 'SH')

    def test_upload_with_different_privacy_setting(self):
        """Non-default published setting on upload."""
        album = AlbumFactory.build()
        album.user = self.user
        album.published = 'PB'
        album.save()
        self.assertEqual(album.published, 'PB')

    def test_upload_with_shared_privacy_setting(self):
        """Non-default published setting on upload."""
        album = AlbumFactory.build()
        album.user = self.user
        album.published = 'SH'
        album.save()
        self.assertEqual(album.published, 'SH')


class LibraryView(TestCase):
    """Test library view."""

    def setUp(self):
        """."""
        user_1 = User(
            username='morgan',
            email='morgan@morgan.com'
        )
        user_2 = User(
            username='kurt',
            email='kurt@kurt.com'
        )
        user_3 = User(
            username='mcgee',
            email='mcgee@mcgee.com'
        )
        user_1.save()
        user_2.save()
        user_3.save()
        self.user_1 = user_1
        self.user_2 = user_2
        self.user_3 = user_3

        photos_1 = [PhotoFactory.build() for i in range(10)]
        for photo in photos_1:
            photo.user = user_1
            photo.published = 'PB'
            photo.save()
        photos_1[0].published = 'PV'
        photos_1[0].save()

        photos_2 = [PhotoFactory.build() for i in range(10)]
        for photo in photos_2:
            photo.user = user_2
            photo.published = 'PB'
            photo.save()

        albums = [AlbumFactory.build() for i in range(3)]
        albums[0].user = user_1
        albums[0].published = 'PB'
        albums[0].cover = photos_1[1]
        albums[1].user = user_2
        albums[1].cover = photos_2[1]
        albums[2].user = user_3
        albums[2].published = 'PB'
        albums[0].save()
        albums[1].save()
        albums[2].save()

        for photo in photos_1:
            albums[0].photos.add(photo)
            albums[0].save()

        for photo in photos_2:
            albums[1].photos.add(photo)
            albums[0].save()

        self.photos_1 = photos_1
        self.photos_2 = photos_2
        self.albums = albums
        self.client = Client()

    def test_logged_out_user_redirects(self):
        """Logged out user redirects to login."""
        response = self.client.get(reverse('library'))
        self.assertRedirects(response, '/accounts/login/?next=/images/library/')

    def test_logged_in_user_gets_200_status(self):
        """Logged in user gets 200 status on library get."""
        self.client.force_login(self.user_1)
        response = self.client.get(reverse('library'))
        self.assertTrue(response.status_code == 200)

    def test_logged_in_user_library_view_shows_correct_album_count(self):
        """Logged-in user sees correct album count."""
        self.client.force_login(self.user_1)
        response = self.client.get(reverse('library'))
        html = BeautifulSoup(response.content, 'html.parser')
        albums = html.find_all('li', 'album')
        self.assertEqual(1, len(albums))

    def test_logged_in_user_library_view_shows_correct_photo_count(self):
        """Logged-in user sees correct photo count."""
        self.client.force_login(self.user_1)
        response = self.client.get(reverse('library'))
        html = BeautifulSoup(response.content, 'html.parser')
        photos = html.find_all('li', 'photo')
        self.assertEqual(10, len(photos))


class AlbumView(TestCase):
    """Test album views."""

    def setUp(self):
        """."""
        user_1 = User(
            username='morgan',
            email='morgan@morgan.com'
        )
        user_2 = User(
            username='kurt',
            email='kurt@kurt.com'
        )
        user_3 = User(
            username='mcgee',
            email='mcgee@mcgee.com'
        )
        user_1.save()
        user_2.save()
        user_3.save()
        self.user_1 = user_1
        self.user_2 = user_2
        self.user_3 = user_3

        photos_1 = [PhotoFactory.build() for i in range(10)]
        for photo in photos_1:
            photo.user = user_1
            photo.published = 'PB'
            photo.save()
        photos_1[0].published = 'PV'
        photos_1[0].save()

        photos_2 = [PhotoFactory.build() for i in range(10)]
        for photo in photos_2:
            photo.user = user_2
            photo.published = 'PB'
            photo.save()

        albums = [AlbumFactory.build() for i in range(3)]
        albums[0].user = user_1
        albums[0].published = 'PB'
        albums[0].cover = photos_1[1]
        albums[1].user = user_2
        albums[1].cover = photos_2[1]
        albums[2].user = user_3
        albums[2].published = 'PB'
        albums[0].save()
        albums[1].save()
        albums[2].save()

        for photo in photos_1:
            albums[0].photos.add(photo)
            albums[0].save()

        for photo in photos_2:
            albums[1].photos.add(photo)
            albums[0].save()

        self.photos_1 = photos_1
        self.photos_2 = photos_2
        self.albums = albums
        self.client = Client()

    def test_albums_logged_in_logged_out_users_see_same_content(self):
        """View is the same regardless of auth."""
        logged_out_response = self.client.get(reverse('albums'))
        self.client.force_login(self.user_1)
        logged_in_response = self.client.get(reverse('albums'))
        self.assertEqual(logged_out_response.content, logged_in_response.content)

    def test_public_album_count(self):
        """Display albums match published album count."""
        response = self.client.get(reverse('albums'))
        html = BeautifulSoup(response.content, 'html5lib')
        albums = html.find_all('li', 'album')
        self.assertEqual(len(albums), Album.objects.filter(published='PB').count())

    def test_album_displays_correct_number_images(self):
        """Album view displays all published photos belonging to album."""
        response = self.client.get(reverse('single_album', kwargs={'album_id': self.albums[0].id}))
        html = BeautifulSoup(response.content, 'html5lib')
        photos = html.find_all('img')
        album_title = html.find('p', 'album-title').text
        self.assertEqual(len(photos), Album.objects.get(id=self.albums[0].id).photos.filter(published='PB').count())
        self.assertEqual(album_title, Album.objects.get(id=self.albums[0].id).title)

"""Tests for Imager Profile app."""

from django.test import TestCase
from django.contrib.auth.models import User
from imager_profile.models import ImagerProfile

import factory


# class PhotoFactory(factory.django.DjangoModelFactory):
#     """Factory for creating users."""

#     class Meta:
#         """."""

#         model = Photo
#     username = factory.Sequence(lambda n: 'user{}'.format(n))
#     email = factory.Sequence(lambda n: 'user{}@example.com'.format(n))


# class ImagerProfileTestCase(TestCase):
#     """ImagerProfile tests."""

#     def setUp(self):
#         """."""
#         users = [UserFactory.create() for i in range(20)]

#         for user in users:
#             user.set_password('cake')
#             user.save()

#         self.users = users


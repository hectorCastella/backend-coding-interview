from django.test import TestCase
from django.contrib.auth.models import User

from photos.models import Photographer, Photo, PhotoVariant
from photos.serializers import (
    PhotographerSerializer,
    PhotoVariantSerializer,
    PhotoSerializer,
)


class PhotographerSerializerTest(TestCase):

    def test_duplicate_external_id(self):
        """Prevenet photographer with same external id to exists"""

        # given
        odl_photographer = Photographer.objects.create(
            external_id=101, name="Old John", url="https://example.com/old-john"
        )
        # when
        new_photographer = Photographer.objects.create(
            external_id=101, name="John Doe", url="https://example.com/john"
        )
        serializers = PhotoSerializer(data=new_photographer)

        # then
        self.assertFalse(serializers.is_valid(raise_exception=False))


    def test_serialize_model_instance(self):
        """Ensure that the serializers are able to pass properly"""

        # given
        photographer = Photographer.objects.create(
            external_id=101, name="John Doe", url="https://example.com/john"
        )
        # when
        serializer = PhotographerSerializer(photographer)

        # then
        self.assertEqual(serializer.data["name"], "John Doe")
        self.assertEqual(serializer.data["external_id"], 101)
        self.assertEqual(serializer.data["url"], "https://example.com/john")


class PhotoVariantSerializerTest(TestCase):

    def test_valid_data(self):
        """Ensure that the serailizer is able to pass when all attributes is given"""
        # given
        data = {"variant_name": "large", "url": "https://example.com/photo_large.jpg"}
        serializer = PhotoVariantSerializer(data=data)

        # then
        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_missing_variant_name(self):
        """Ensure that all the variants have some kind of name attach to it"""
        # given
        data = {"url": "https://example.com/photo_large.jpg"}

        # when 
        serializer = PhotoVariantSerializer(data=data)

        # then
        self.assertFalse(serializer.is_valid())

    def test_missing_url(self):
        """Ensure that all the variants have the url attach to it"""
        
        # given
        data = {"variant_name": "large"}

        # when
        serializer = PhotoVariantSerializer(data=data)

        # then
        self.assertFalse(serializer.is_valid())

    def test_serialize_model_instance(self):
        """Assume a proper photo is created"""

        # when 
        photographer = Photographer.objects.create(
            external_id=1, name="Jane", url="https://example.com/jane"
        )
        photo = Photo.objects.create(
            photographer=photographer,
            external_id=500,
            width=1920,
            height=1080,
            url="https://example.com/photo.jpg",
            avg_color="#FFFFFF",
            alt="A photo",
        )
        variant = {
            "original_photo":photo,
            "variant_name": "small",
            "url":"https://example.com/photo_small.jpg",
        }

        # then
        serializer = PhotoVariantSerializer(data=variant)

        # given
        self.assertTrue(serializer.is_valid())

class PhotoSerializerTest(TestCase):

    def _build_photo_data(self, **overrides):
        data = {
            "photographer": {
                "external_id": 200,
                "name": "Alice",
                "url": "https://example.com/alice",
            },
            "photos_variants": [
                {"variant_name": "original", "url": "https://example.com/orig.jpg"},
                {"variant_name": "small", "url": "https://example.com/small.jpg"},
            ],
            "external_id": 1000,
            "width": 1920,
            "height": 1080,
            "url": "https://example.com/photo.jpg",
            "avg_color": "#AABBCC",
            "alt": "Test photo",
        }
        data.update(overrides)
        return data

    def test_valid_data(self):
        """Ensure that internal function is able to create proper photo"""

        # given
        data = self._build_photo_data()

        # when 
        serializer = PhotoSerializer(data=data)

        # then
        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_create_without_variants(self):
        """It is possible a photo can be create without variant"""

        # given 
        data = self._build_photo_data(photos_variants=[])

        # when
        serializer = PhotoSerializer(data=data)

        # Then
        self.assertTrue(serializer.is_valid())

    def test_missing_photographer_fails_validation(self):
        """A new photo is being created, but photographer is missing"""
        # given
        data = self._build_photo_data()
        data.pop("photographer")

        # when 
        serializer = PhotoSerializer(data=data)

        # then
        self.assertFalse(serializer.is_valid())

    def test_missing_external_id_fails(self):
        """A new photo is being created, but photographer is missing external id"""
        # given 
        data = self._build_photo_data()
        data.pop("external_id")

        # when 
        serializer = PhotoSerializer(data=data)

        # then
        self.assertFalse(serializer.is_valid())

    def test_duplicate_external_id_fails(self):
        """A new photo is being created, as well as photographer but exteranl id already exits"""

        # given
        data = self._build_photo_data()
        serializer = PhotoSerializer(data=data)
        serializer.is_valid()
        serializer.save()

        # when
        data2 = self._build_photo_data(
            url="https://example.com/photo2.jpg",
            photos_variants=[
                {"variant_name": "tiny", "url": "https://example.com/tiny2.jpg"},
            ],
        )
        serializer2 = PhotoSerializer(data=data2)

        # then 
        self.assertFalse(serializer2.is_valid())

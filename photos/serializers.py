from typing import Required
import datetime

import logging
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework import serializers
from rest_framework.authtoken.models import Token

from photos.models import Photographer, Photo, PhotoVariant

class PhotographerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photographer
        fields = "__all__"

class PhotoVariantSerializer(serializers.ModelSerializer):

    class Meta:
        model = PhotoVariant
        fields = ["id", "variant_name", "url"]

class PhotoSerializer(serializers.ModelSerializer):

    photographer = PhotographerSerializer(required=False)
    photos_variants = PhotoVariantSerializer(source="variants", required=False, many=True)

    class Meta:
        model = Photo 
        fields = "__all__"

    def validate(self, attrs):
        photographer = attrs.get("photographer", None)

        # logic run only for created a new instance of photo
        if not self.instance:
            if not photographer:
                raise serializers.ValidationError({"Missing photographer": "Missing field"})
            
            photographer_serializer = PhotographerSerializer(data=photographer)


            if not photographer_serializer.is_valid():
                raise serializers.ValidationError({"Invalid photographer": f"Please ensure that the photographer is valid: {photographer}"})


        # validate all the variants
        variants = attrs.get("variants", [])
        for variant_data in variants:
            variants_serializers = PhotoVariantSerializer(data=variant_data)
            if not variants_serializers.is_valid():
                raise serializers.ValidationError({"Invalid Variant": f"Invalid variant : {variant_data}"})

        return super().validate(attrs)

    def create(self, validate_attrs):
        photographer_data = validate_attrs.pop("photographer")
        variants_data = validate_attrs.pop("variants")

        photographer = Photographer.objects.create(**photographer_data)

        photo = Photo.objects.create(photographer=photographer, **validate_attrs)
        for variant in variants_data:
            PhotoVariant.objects.create(original_photo=photo, **variant)

        return photo

    def update(self, instance, validated_data):
        variants = validated_data.pop("variants",[])
        photographer = validated_data.pop("photographer", {})

        # Delete all the previous variants and create new ones being passed in this object
        if len(variants) > 0:
            PhotoVariant.objects.filter(original_photo=instance).delete()
            for variant in variants:
                PhotoVariant.objects.create(original_photo=instance, **variant)

        # If photographer is pass then determinate if needw to create a new or update using the external
        # id
        if photographer:
            # if it is a different photographer then update the value
            external_id = photographer.get("external_id", None)
            different_photographer = instance.photographer.external_id != external_id
            if external_id and different_photographer:
                # create a new photographer and attack to the current photo
                new_photographer_instance, created = Photographer.objects.get_or_create(**photographer)
                instance.photographer = new_photographer_instance
                instance.save()
        
        return super().update(instance, validated_data)

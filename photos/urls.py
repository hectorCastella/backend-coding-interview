from django.urls import path, include
from . import views

from rest_framework.routers import DefaultRouter

app_name = 'photos'

router =  DefaultRouter()
router.register(r"photos", views.PhotoReadOnlyViewSet, basename="photos")
router.register(r"photographer", views.PhotographerReadOnlyViewSet, basename="photosgraphers")
router.register(r"photos-variants", views.PhotoVariantReadOnlyViewSet, basename="photos-variants")

urlpatterns = [

    # Get Photo or update photo
    #path("photo/", views.PhotoView.as_view(), name="photo"),
    # Get Photographer or update Photographer
    #path("photographer/", views.PhotographerView.as_view(), name="photographer"),

    # Upload csv file
    path("upload-data/", views.UploadDataView.as_view(), name="upload-data"),
    path("", include(router.urls))
]
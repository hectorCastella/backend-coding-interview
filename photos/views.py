
import csv
import io
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status, viewsets

from photos.models import Photographer, Photo, PhotoVariant
from photos.serializers import PhotoSerializer, PhotographerSerializer, PhotoVariantSerializer

# Create your views here.
class UploadDataView(APIView):
    parser_classes = [MultiPartParser, FormParser] # Handles form data and file uploads

    def post(self, request, *args, **kwargs):
        # Access the uploaded file from the request data
        csv_file = request.FILES.get('file')

        if not csv_file:
            return Response(
                {"error": "No file uploaded"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Basic file validation
        if not csv_file.name.endswith('.csv'):
            return Response(
                {"error": "Filetype not supported. Must be a .csv file."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Process the CSV content
        try:
            decoded_file = csv_file.read().decode('utf-8')
            io_string = io.StringIO(decoded_file)
            reader = csv.DictReader(io_string)
            for row in reader:

                # create the photograhper
                photographer_data = {
                    "name": row["photographer"],
                    "url": row["photographer_url"],
                    "external_id": row["photographer_id"]
                }

                # Query the input and ensure that the data is there
                variants = []
                raw_keys = row.keys()
                for key in raw_keys:
                    if "src" not in key:
                        continue

                    parse_key = key[4:]
                    convert_key = PhotoVariant.VARIANTS_NAMES(parse_key)
                    variant_data = {
                        "url": row[key],
                        "variant_name": convert_key
                    }
                    variants.append(variant_data)

                # constructs the photo serializser
                photo_data = {
                    "photographer": photographer_data,
                    "photos_variants": variants,
                    "external_id": row["id"],
                    "width": row["width"],
                    "height": row["height"],
                    "url": row["url"],
                    "avg_color": row["avg_color"],
                    "alt": row["alt"]
                }
                photo_serializer = PhotoSerializer(data=photo_data) 
                if photo_serializer.is_valid():
                    photo_serializer.save()
                else:
                    return Response({
                        "general_message": f"Row {row} not valid errors",
                        "errors": photo_serializer.errors
                    }, status=status.HTTP_400_BAD_REQUEST)


            return Response(
                {"sucess": "Data upload"}
            )
        except Exception as e:
            return Response(
                {"error": f"An error occurred: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class PhotoReadOnlyViewSet(viewsets.ModelViewSet):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer

class PhotographerReadOnlyViewSet(viewsets.ModelViewSet):
    queryset = Photographer.objects.all()
    serializer_class = PhotographerSerializer

class PhotoVariantReadOnlyViewSet(viewsets.ModelViewSet):
    queryset = PhotoVariant.objects.all()
    serializer_class = PhotoVariantSerializer 

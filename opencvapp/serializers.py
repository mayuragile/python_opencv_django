from rest_framework.serializers import ModelSerializer
from .models import *


class ImageSerializer(ModelSerializer):

    class Meta:
        model = ImageDetails
        fields = ('id', 'img_name', 'img')

class TestImageSerializer(ModelSerializer):

    class Meta:
        model = TestUploadImage
        fields = ('id', 'testimg')


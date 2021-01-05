from .models import *
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import cv2
import numpy as np
import os
from numpy import asarray 


class ImageUploadView(APIView):
    def post(self, request, *args, **kwargs):
        
        img = request.data.get('img')
        img_name = request.data.get('img_name')
        
        if not request.data:
            return Response({"message": "Data is required", "status": status.HTTP_400_BAD_REQUEST}, status.HTTP_400_BAD_REQUEST)

        if not img:
            return Response({"message": "img is required", "status": status.HTTP_400_BAD_REQUEST}, status.HTTP_400_BAD_REQUEST)
    
        if not img_name:
            response = {
                'status_code' : status.HTTP_400_BAD_REQUEST,
                'message' : 'There is no images in Database, so this image will inserted, so img_name is required!',
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        data = {"img_name":img_name,"img":img}
        serializer = ImageSerializer(data=data, context={'request': request})
            
        if not serializer.is_valid(raise_exception=False):
            error_msg = serializer.errors

            if serializer.errors.get('img'):
                error_msg = ''.join(serializer.errors['img'])

            # Retrun error message with 400 status
            return Response({"message": error_msg,"status":status.HTTP_400_BAD_REQUEST}, status.HTTP_400_BAD_REQUEST)

        serializer.save()
        response = {
                'status_code' : status.HTTP_200_OK,
                'message' : 'Image upload successfully.!',
            }
        return Response(response, status=status.HTTP_201_CREATED)


        # data = {"testimg":img}
        # serializer = TestImageSerializer(data=data, context={'request': request})
            
        # if not serializer.is_valid(raise_exception=False):
        #     error_msg = serializer.errors

        #     if serializer.errors.get('testimg'):
        #         error_msg = ''.join(serializer.errors['testimg'])

        #     # Retrun error message with 400 status
        #     return Response({"message": error_msg,"status":status.HTTP_400_BAD_REQUEST}, status.HTTP_400_BAD_REQUEST)

        # serializer.save()


        # last_uploaded_img_obj = TestUploadImage.objects.filter().last()
        # last_uploaded = cv2.imread(last_uploaded_img_obj.testimg.path)
        
        # last_img = request.build_absolute_uri(last_uploaded_img_obj.testimg.url)
        
        # for i in ImageDetails.objects.all():
        #     img_path = cv2.imread(i.img.path)
            
        #     img = request.build_absolute_uri(i.img.url)
            
        #     if last_uploaded.shape == img_path.shape:
        #         difference = cv2.subtract(img_path, last_uploaded)
        #         # print(difference)
        #         b, g, r = cv2.split(difference)
        #         # print(cv2.countNonZero(b), cv2.countNonZero(g), cv2.countNonZero(r))
        #         if cv2.countNonZero(b) == 0 and cv2.countNonZero(g) == 0 and cv2.countNonZero(r) == 0:
        #             response = {
        #                 'status_code' : status.HTTP_200_OK,
        #                 'message' : 'Image is matched with one of the images in database.',
        #                 'database_image' : img,
        #                 'database_image_name' : i.img_name,
        #                 'entered_image' : last_img,
        #             }
        #             return Response(response, status=status.HTTP_200_OK)
        
        #         else:
        #             response = {
        #                 'status_code' : status.HTTP_400_BAD_REQUEST,
        #                 'message' : 'Image is not matched with any images in database.',
        #                 'entered_image' : last_img,
        #             }
        #             return Response(response, status=status.HTTP_400_BAD_REQUEST)


class ImageComaprisonView(APIView):
    def post(self, request, *args, **kwargs):
        
        img = request.data.get('img')
        img_name = request.data.get('img_name')
        
        if not request.data:
            return Response({"message": "Data is required", "status": status.HTTP_400_BAD_REQUEST}, status.HTTP_400_BAD_REQUEST)

        if not img:
            return Response({"message": "img is required", "status": status.HTTP_400_BAD_REQUEST}, status.HTTP_400_BAD_REQUEST)

        obj = ImageDetails.objects.filter().last()
        
        if not obj:
            
            if not img_name:
                response = {
                    'status_code' : status.HTTP_400_BAD_REQUEST,
                    'message' : 'There is no images in Database, so this image will inserted, so img_name is required!',
                }
                return Response(response, status=status.HTTP_400_BAD_REQUEST)

            data = {"img_name":img_name,"img":img}
            serializer = ImageSerializer(data=data, context={'request': request})
                
            if not serializer.is_valid(raise_exception=False):
                error_msg = serializer.errors

                if serializer.errors.get('img'):
                    error_msg = ''.join(serializer.errors['img'])

                # Retrun error message with 400 status
                return Response({"message": error_msg,"status":status.HTTP_400_BAD_REQUEST}, status.HTTP_400_BAD_REQUEST)

            serializer.save()
            response = {
                    'status_code' : status.HTTP_200_OK,
                    'message' : 'Image upload successfully.!',
                }
            return Response(response, status=status.HTTP_201_CREATED)


        data = {"testimg":img}
        serializer = TestImageSerializer(data=data, context={'request': request})
            
        if not serializer.is_valid(raise_exception=False):
            error_msg = serializer.errors

            if serializer.errors.get('testimg'):
                error_msg = ''.join(serializer.errors['testimg'])

            # Retrun error message with 400 status
            return Response({"message": error_msg,"status":status.HTTP_400_BAD_REQUEST}, status.HTTP_400_BAD_REQUEST)

        serializer.save()


        last_uploaded_img_obj = TestUploadImage.objects.filter().last()
        last_uploaded = cv2.imread(last_uploaded_img_obj.testimg.path)
        
        last_img = request.build_absolute_uri(last_uploaded_img_obj.testimg.url)
        
        del_obj = TestUploadImage.objects.filter().last()
        os.remove(del_obj.testimg.path)
        del_obj.delete()

        for i in ImageDetails.objects.all():
            img_path = cv2.imread(i.img.path)
            
            img = request.build_absolute_uri(i.img.url)
            
            if last_uploaded.shape == img_path.shape:
                print(last_uploaded.shape, img_path.shape)
                difference = cv2.subtract(img_path, last_uploaded)
                # print(difference)
                b, g, r = cv2.split(difference)
                print(cv2.countNonZero(b), cv2.countNonZero(g), cv2.countNonZero(r))
                if cv2.countNonZero(b) == 0 and cv2.countNonZero(g) == 0 and cv2.countNonZero(r) == 0:
                    response = {
                        'status_code' : status.HTTP_200_OK,
                        'message' : 'Image is matched with one of the images in database.',
                        'database_image' : img,
                        'database_image_name' : i.img_name,
                        'entered_image' : last_img,
                    }
                    return Response(response, status=status.HTTP_200_OK)
        
                else:
                    response = {
                        'status_code' : status.HTTP_400_BAD_REQUEST,
                        'message' : 'Image is not matched with any images in database.',
                        'entered_image' : last_img,
                    }
                    return Response(response, status=status.HTTP_400_BAD_REQUEST)
            
            else:
                print(True)
                response = {
                    'status_code' : status.HTTP_400_BAD_REQUEST,
                    'message' : 'Image is not matched with any images in database.',
                    'entered_image' : last_img,
                }
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
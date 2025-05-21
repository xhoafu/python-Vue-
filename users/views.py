from django.shortcuts import render
from rest_framework.generics import get_object_or_404
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import UserProfileSerializers,UserSerializers,RegisterSerializer
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from .models import UserProfile
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.permissions import BasePermission,IsAuthenticated,IsAdminUser
from django.views.decorators.cache import cache_page


# Create your views here.

class UserProfileView(GenericAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializers
    # permission_classes = [IsAuthenticated]

    def get(self,request):
        return Response(self.serializer_class(instance=self.get_queryset(),many=True).data)

    def post(self,request):

        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)



class UserDetaView(GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializers
    permission_classes = [IsAuthenticated]

    def get(self,request,pk):

        return Response(self.serializer_class(instance=self.get_object()).data)

    def put(self,request,pk):
        instance = self.get_object()
        serializer = self.serializer_class(instance=instance,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,status=status.HTTP_404_NOT_FOUND)

    def delete(self,request,pk):
        try:
            self.get_object().delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)


class Register(GenericAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    # permission_classes = [IsAuthenticated]

    def get(self,request):

        return Response(self.serializer_class(instance=self.get_queryset(),many=True).data)

    def post(self,request):

        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)



class Login(TokenObtainPairView):
    def post(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        result = serializer.validated_data
        result['email'] = serializer.user.email
        result['username'] = serializer.user.username
        result['user_id'] = serializer.user.id
        # result['token'] = result.pop('access')

        return Response(result, status=status.HTTP_200_OK)
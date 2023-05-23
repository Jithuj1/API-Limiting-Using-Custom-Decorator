from django.shortcuts import render
from .models import CustomUser
from .serializer import UserSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .decorators import rate_limit_calls
from rest_framework.pagination import PageNumberPagination




class TokenObtainPairViewExtend(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Adding custom climes 
        token['id'] = user.id
        token['name'] = user.f_name

        if token:
            return token
        else:
            return Response("False")
        

class MytokenObtainPairView(TokenObtainPairView):
    serializer_class = TokenObtainPairViewExtend



@api_view(['POST'])
@rate_limit_calls(rate_limit=5)
def UserDetails(request):
    if request.method == "POST":
        email = request.data.get('email')
        try:
            user = CustomUser.objects.get(email = email)
            if user:
                return Response({'message':"Email already taken "})
        except:
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(status=status.HTTP_202_ACCEPTED)
            else:
                return Response({'message':'wrong credentials'})
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

class CustomPagination(PageNumberPagination):
    page_size = 10


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
@rate_limit_calls(rate_limit=5)
def ListUser(request):
    paginator = CustomPagination()
    if request.method == "GET":
        users = CustomUser.objects.all()    
    else:
        date = request.data.get('date')
        desc = request.data.get('desc')
        if date is not None:
            users = CustomUser.objects.all(created_at = date)
        elif desc is not None :
            users = CustomUser.objects.order_by('-created_at')
        else:
            users= CustomUser.objects.all()
    paginated_users = paginator.paginate_queryset(users, request)
    serializer = UserSerializer(paginated_users, many = True)
    return paginator.get_paginated_response(serializer.data)

from django.shortcuts import redirect
from django.db.models import Count, Q

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated

from drf_spectacular.utils import extend_schema, OpenApiResponse

from api.v1.courses.serializers import CourseSerializer
from accounts.models import CustomUser
from .serializers import CustomUserSerializer
from .permissions import IsOwnerOfAccount


@extend_schema(tags=['Custom Users'], request=CustomUserSerializer, responses=CustomUserSerializer)  
class CustomUserDetailAPIView(APIView):
    permission_classes = [IsOwnerOfAccount, IsAuthenticated]
    
    def get_object(self, id):
        try:
            return CustomUser.objects.get(id=id)
        except CustomUser.DoesNotExist:
            raise redirect('dashboard')
    
    @extend_schema(operation_id='Get user details', description='Get user details by ID')
    def get(self, request, id):
        user = self.get_object(id)
        serializer = CustomUserSerializer(user)
        return Response(serializer.data)
    
    @extend_schema(operation_id='Update user details', description='Update user details by ID')
    def put(self, request, id):
        user = self.get_object(id)
        serializer = CustomUserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    
    @extend_schema(operation_id='Partial update user details', description='Partial update user details by ID')
    def patch(self, request, id):
        user = self.get_object(id)
        serializer = CustomUserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    
    @extend_schema(operation_id='Delete user', description='Delete user by ID')
    def delete(self, request, id):
        user = self.get_object(id)
        user.delete()
        return Response(status=204)


class CustomUserDataSerializer(serializers.Serializer):
    ''' Serializer for custom user data '''
    user = CustomUserSerializer()
    enrolled_courses_count = serializers.IntegerField()
    enrolled_courses_percentage = serializers.IntegerField()


@extend_schema(tags=['Custom Users'], request=None,
               responses={
                200: OpenApiResponse(
                    description='Custom user data',
                    response=CustomUserDataSerializer
                )
            })   
@api_view(['GET'])
def dashboard(request):
    user = request.user
    enrolled_courses = user.subscription.courses.all().annotate(
        completed_lessons_count=Count('lessons', filter=Q(subscriptioncourse__completed_percentage=100))
    )
    
    data = {
        'user': CustomUserSerializer(user, context={'request': request}).data,
        'enrolled_courses': CourseSerializer(enrolled_courses, many=True, context={'request': request}).data,
        'enrolled_courses_count': enrolled_courses.count(),
    }
    
    return Response(data=data)
    
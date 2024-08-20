from django.http import Http404
from django.utils import timezone
from django.shortcuts import get_object_or_404

from drf_spectacular.utils import extend_schema, OpenApiResponse

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from courses.models import Course, Group, Lesson
from .serializers import CourseSerializer, GroupSerializer, LessonSerializer
from .permissions import IsOwnerOfCourse, IsOwnerOfGroup, IsOwnerOfLesson


@extend_schema(tags=['Courses'], request=CourseSerializer, responses=CourseSerializer)   
class CourseAPIView(APIView):
    @extend_schema(operation_id='List courses', description='List all courses')
    def get(self, request):
        courses = Course.objects.all()
        serializer = CourseSerializer(courses, many=True, context={'request': request})
        return Response(serializer.data)
    
    @extend_schema(operation_id='Create course', description='Create a new course')
    def post(self, request):
        serializer = CourseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


@extend_schema(tags=['Course'], request=CourseSerializer, responses=CourseSerializer) 
class CourseDetailAPIView(APIView):
    permission_classes = [IsAuthenticated, IsOwnerOfCourse]
    
    def get_object(self, pk):
        return get_object_or_404(Course, pk=pk)
    
    @extend_schema(operation_id='Get course details', description='Get course details by ID')
    def get(self, request, pk):
        course = self.get_object(pk)
        serializer = CourseSerializer(course, context={'request': request})
        return Response(serializer.data)
    
    @extend_schema(operation_id='Update course details', description='Update course details by ID')
    def put(self, request, pk):
        course = self.get_object(pk)
        serializer = CourseSerializer(course, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    
    @extend_schema(operation_id='Partial update course details', description='Partial update course details by ID')
    def patch(self, request, pk):
        course = self.get_object(pk)
        serializer = CourseSerializer(course, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    
    @extend_schema(operation_id='Delete course', description='Delete course by ID')
    def delete(self, request, pk):
        course = self.get_object(pk)
        course.delete()
        return Response(status=204)


@extend_schema(tags=['Course'], request=None, responses={
        200: OpenApiResponse(description='Course enrolled successfully'),
        400: OpenApiResponse(description='You are already enrolled in this course'),
        402: OpenApiResponse(description='Poinsts not enough, Please buy more points'),
        404: OpenApiResponse(description='Course not found')
    })    
@api_view(['POST'])
def enroll_course(request, pk):
    course = get_object_or_404(Course, pk=pk)
    user = request.user
    balance = user.balance
    if course.price > balance.points:
        return Response({'detail': 'Poinsts not enough, Please buy more points'}, status=402)
    if user.subscription.courses.filter(id=course.id).exists():
        return Response({'detail': 'You are already enrolled in this course'}, status=400)
    
    user.subscription.courses.add(course)
    
    balance -= course.price
    balance.save()
    
    return Response({'detail': 'Course enrolled successfully'}, status=200)


@extend_schema(tags=['Groups'], request=GroupSerializer, responses=GroupSerializer)    
class GroupAPIView(APIView):
    @extend_schema(operation_id='List groups for a course', description='List all groups for a course')
    def get(self, request, pk):
        course = get_object_or_404(Course, pk=pk)
        groups = Group.objects.filter(course=course)
        seraializer = GroupSerializer(groups, many=True, context={'request': request} )
        return Response(seraializer.data)
    
    @extend_schema(operation_id='Create group for a course', description='Create a new group for a course ')
    def post(self, request, pk):
        course = get_object_or_404(Course, pk=pk)
        serializer = GroupSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(course=course)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


@extend_schema(tags=['Groups'], request=GroupSerializer, responses=GroupSerializer)  
class GroupDetailAPIView(APIView):
    permission_classes = [IsAuthenticated, IsOwnerOfGroup]
     
    def get_object(self, pk):
        return get_object_or_404(Group, pk=pk)
    
    @extend_schema(operation_id='Get group details', description='Get group details by ID')
    def get(self, request, pk):
        group = self.get_object(pk)
        serializer = GroupSerializer(group, context={'request': request})
        return Response(serializer.data)
    
    @extend_schema(operation_id='Update group details', description='Update group details by ID')
    def put(self, request, pk):
        group = self.get_object(pk)
        serializer = GroupSerializer(group, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    
    @extend_schema(operation_id='Partial update group details', description='Partial update group details by ID')
    def patch(self, request, pk):
        group = self.get_object(pk)
        serializer = GroupSerializer(group, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    
    @extend_schema(operation_id='Delete group', description='Delete group by ID')
    def delete(self, request, pk):
        group = self.get_object(pk)
        group.delete()
        return Response(status=204)


@extend_schema(tags=['Lessons'], request=LessonSerializer, responses=LessonSerializer)     
class LessonAPIView(APIView):
    def get_object(self, pk):
        return get_object_or_404(Course, pk=pk)
    
    @extend_schema(operation_id='List lessons for a course', description='List all lessons for a course')
    def get(self, request, pk):
        course = self.get_object(pk)
        lessons = Lesson.objects.filter(course=course)
        serializer = LessonSerializer(lessons, many=True, context={'request': request})
        return Response(serializer.data)
    
    @extend_schema(operation_id='Create lesson for a course', description='Create a new lesson for a course')
    def post(self, request, pk):
        course = self.get_object(pk)
        serializer = LessonSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(course=course)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    

@extend_schema(tags=['Lessons'], request=LessonSerializer, responses=LessonSerializer)   
class LessonDetailAPIView(APIView):
    permission_classes = [IsAuthenticated, IsOwnerOfLesson]
    
    def get_object(self, pk):
        return get_object_or_404(Lesson, pk=pk)
    
    @extend_schema(operation_id='Get lesson details', description='Get lesson details by ID')
    def get(self, request, pk):
        lesson = self.get_object(pk)
        serializer = LessonSerializer(lesson, context={'request': request})
        return Response(serializer.data)
    
    @extend_schema(operation_id='Update lesson details', description='Update lesson details by ID')
    def put(self, request, pk):
        lesson = self.get_object(pk)
        serializer = LessonSerializer(lesson, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    
    @extend_schema(operation_id='Partial update lesson details', description='Partial update lesson details by ID')
    def patch(self, request, pk):
        lesson = self.get_object(pk)
        serializer = LessonSerializer(lesson, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    
    @extend_schema(operation_id='Delete lesson', description='Delete lesson by ID')
    def delete(self, request, pk):
        lesson = self.get_object(pk)
        lesson.delete()
        return Response(status=204)
    

@extend_schema(tags=['Lessons'], request=None, responses={
    200: OpenApiResponse(description='Lesson completed successfully'),
    403: OpenApiResponse(description='You are not enrolled in this course'),
    404: OpenApiResponse(description='Lesson not found')
}) 
@api_view(['POST'])
def lesson_complete(request, pk, lesson_pk):
    lesson = get_object_or_404(pk=lesson_pk)
    course = lesson.course
    user = request.user
    if not user.subscription.courses.filter(id=course.id).exists():
        return Response({'detail': 'You are not enrolled in this course'}, status=403)
    
    progress = user.subscriptioncourse.filter(course=course)
    progress.completed_lessons.add(lesson)
    progress.completed_percentage = (progress.completed_lessons.count() / course.lessons.count()) * 100
    
    if progress.completed_percentage >= 100:
        progress.ended_at = timezone.now()
    
    progress.save()
    
    return Response({'detail': 'Lesson completed successfully'}, status=200)
    

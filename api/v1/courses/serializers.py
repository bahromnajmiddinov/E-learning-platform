from rest_framework import serializers

from drf_spectacular.utils import extend_schema_field

from api.v1.accounts.serializers import CustomUserSerializer
from courses.models import Course, Lesson, Group


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'
        

class CourseSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='course-detail', read_only=True, lookup_field='pk')
    author = CustomUserSerializer(read_only=True)
    lessons = LessonSerializer(many=True, read_only=True)
    students_count = serializers.SerializerMethodField()
    lessons_count = serializers.SerializerMethodField()
    
    completed_lessons_count = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = Course
        fields = '__all__'
        extra_fields =['url']
    
    @extend_schema_field(field=serializers.IntegerField, component_name='Number of students enrolled in the course')
    def get_students_count(self, obj):
        return obj.get_student_count
    
    @extend_schema_field(field=serializers.IntegerField, component_name='Number of lessons in the course')
    def get_lessons_count(self, obj):
        return obj.get_lessons_count


class GroupSerializer(serializers.ModelSerializer):
    course = CourseSerializer(read_only=True)
    members = CustomUserSerializer(many=True, read_only=True)
    
    class Meta:
        model = Group
        fields = '__all__'
    
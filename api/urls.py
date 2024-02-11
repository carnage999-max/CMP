from django.urls import path
from . import views


urlpatterns = [
    path('all-questions', views.getQuestions, name='questions'),
    path('<str:course_code>/questions', views.getQuestionsByCourseCode, name='course-questions'),
    path('courses-available', views.getAllCourses, name='course-available'),
]


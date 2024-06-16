"""
URL configuration for TimelyTeacher project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('',views.home, name='home'),
    path('home',views.home, name='home'),
    path('login',views.login, name='login'),
    path('logout',views.logout, name='logout'),
    path('admin',views.admin, name='admin'),
    path('teachers',views.manageteachers, name='teachers'),
    path('teacherdetails',views.teacherdetails, name='teacherdetails'),
    path('class',views.manageclass, name='class'),
    path('manage',views.manage, name='manage'),
    path('timetable',views.timetable, name='timetable'),
    path('subjects',views.subjects, name='subjects'),
    path('students',views.students, name='students'),
    path('studentdetails',views.studentdetails, name='studentdetails'),
    path('saveImportedStudent',views.saveImportedStudent, name='saveImportedStudent'),
    path('saveTimetable',views.saveTimetable, name='saveTimetable'),
    path('saveAttendence',views.saveAttendence, name='saveAttendence'),
    path('attendence',views.attendence, name='attendence'),
    path('viewattendence',views.viewattendence, name='viewattendence'),
    path('schedule',views.schedule, name='schedule'),
    path('attendencereport',views.attendencereport, name='attendencereport'),
]

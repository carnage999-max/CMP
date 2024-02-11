from .models import *
from .forms import *
from django.contrib import messages
from django.contrib.auth import (authenticate, login, logout,
                                 update_session_auth_hash)
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

import csv 
import ast


def add_questions(csv_path, course_code, course_title):
     with open(csv_path, "r") as file:
        reader = csv.DictReader(file)
        try:
            for row in reader:
                if len(ast.literal_eval(row['options'])) == 4:
                    QuizQuestion.objects.create(
                    course_code=course_code,
                    course_title=course_title,
                    question=row['Questions'],
                    optionA=ast.literal_eval(row['options'])[0],
                    optionB=ast.literal_eval(row['options'])[1],
                    optionC=ast.literal_eval(row['options'])[2],
                    optionD=ast.literal_eval(row['options'])[3],
                    answer=row['answer']
                )
                else:
                    QuizQuestion.objects.create(
                    course_code=course_code,
                    course_title=course_title,
                    question=row['Questions'],
                    optionA=ast.literal_eval(row['options'])[1],
                    optionB=ast.literal_eval(row['options'])[2],
                    answer=row['answer']
                )
        except:
            pass


def index(request):
    # csv_path = 'main\scripts\cmp214_3.csv'
    # course_code='CMP214'
    # course_title='Data Management I'
    # add_questions(csv_path, course_code, course_title)
    codes = set([i.course_code for i in QuizQuestion.objects.all()])
    titles = set([i.course_title for i in QuizQuestion.objects.all()])
    codes_titles = list(zip(codes, titles))
    print(codes_titles)
    return render(request, 'index.html')


def registerUser(request):
    if request.user.is_authenticated:
        return redirect('index')
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'Something is wrong')
    else:
        form = CreateUserForm()

    return render(request, 'signup.html', {'form': form})


def loginUser(request):
    if request.user.is_authenticated:
        return redirect('index')
    if request.method == "POST":
        form = SignInForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(email=email, password=password)
            if user:
                login(request, user)
                return redirect('index')
            else:
                messages.error(request, 'Email or Password is incorrect!')
    else:
        form = SignInForm()

    return render(request, 'signin.html', {'form': form})


# def addModel():
#     
            
# addModel()


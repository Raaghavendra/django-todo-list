from django.contrib.auth.models import Permission
from django.shortcuts import render
from rest_framework import generics, permissions
from .serializers import TodoSerializer, TodoCompleteSerializer
from todo.models import Todo
from datetime import datetime
from rest_framework.exceptions import ValidationError
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.db import IntegrityError
from rest_framework.authtoken.models import Token
# Create your views here.

@csrf_exempt
def signup(request):
    if request.method == 'POST':
        # Create new user
        try:
            data = JSONParser().parse(request)
            user = User.objects.create_user(username=data['username'],password=data['password'])
            user.save()
            token = Token.objects.create(user=user)
            return JsonResponse({'token':str(token)}, status=201)
        except IntegrityError:
            return JsonResponse({'error':'Username is already taken :-('}, status=400)

@csrf_exempt
def login(request):
    if request.method == 'POST':
        # Create new user
        data = JSONParser().parse(request)
        user = authenticate(request,username=data['username'],password=data['password'])
        if user:
            try:
                token = Token.objects.get(user=user)
            except:
                token = Token.objects.create(user=user)
            return JsonResponse({'token':str(token)}, status=201)
        else:
            return JsonResponse({'error':'User dosen\'t exist'}, status=400)

class TodoCompletedList(generics.ListAPIView):
    serializer_class = TodoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Todo.objects.filter(user=user,status=True).order_by('-datecompleted')

class TodoCreateList(generics.ListCreateAPIView):
    serializer_class = TodoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Todo.objects.filter(user=user,status=False)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class TodoRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TodoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Todo.objects.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class TodoComplete(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TodoCompleteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Todo.objects.filter(user=user)

    def perform_update(self, serializer):
        if Todo.objects.get(pk=self.kwargs['pk']).status:
            raise ValidationError("You have already marked it as complete")
        else:
            serializer.instance.datecompleted = datetime.now()
            serializer.save(status=True)
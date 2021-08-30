from django.urls import path
from django.urls.resolvers import URLPattern
from . import views

urlpatterns =[
    # Auth
    path('signup',views.signup),
    path('login',views.login), #provide new token if user exists
    path('todos', views.TodoCreateList.as_view()),
    path('todos/<int:pk>', views.TodoRetrieveUpdateDestroy.as_view()),
    path('todos/<int:pk>/complete', views.TodoComplete.as_view()),
    path('todos/completed', views.TodoCompletedList.as_view())
]
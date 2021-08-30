from django.db.models import fields
from rest_framework import serializers
from todo.models import Todo

class TodoSerializer(serializers.ModelSerializer):
    datecreated = serializers.ReadOnlyField()
    datecompleted = serializers.ReadOnlyField()
    class Meta:
        model = Todo
        fields = ['id','title','description','datecreated','datecompleted','important']

class TodoCompleteSerializer(serializers.ModelSerializer):
    #datecreated = serializers.ReadOnlyField()
    #datecompleted = serializers.ReadOnlyField()
    class Meta:
        model = Todo
        fields = ['id']
        read_only_fields = ['title','description','datecreated','datecompleted','important']
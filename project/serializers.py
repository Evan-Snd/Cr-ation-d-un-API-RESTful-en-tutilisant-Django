from rest_framework import serializers
from .models import Contributors, Projects, Issues, Comments
from authentication.serializers import UserSerializer


class ProjectSerializer(serializers.ModelSerializer):
    #   project_id = serializers.IntegerField()
    #   title = serializers.CharField()
    #   description = serializers.CharField()
    #   type = serializers.CharField()
    #   author_user_id = serializers.PrimaryKeyRelatedField(read_only=True)
    # author = UserSerializer()
    class Meta:
        model = Projects
        fields = ['id', 'title', 'description', 'type', 'author']
        extra_kwargs = {'author': {'read_only': True}}


class ContributorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contributors
        fields = ['id', 'user', 'project', 'permission', 'role']
        extra_kwargs = {'project': {'read_only': True}}



class IssueSerializer(serializers.ModelSerializer):
    # parent_lookup_kwargs = {
    #     'projetc_pk': 'project__pk',
    # }
    class Meta:
        model = Issues
        fields = ['id', 'title', 'description', 'tag', 'priority', 'status', 'author', 'assignee', 'created_time']
        extra_kwargs = {'author': {'read_only': True}}


class CommentSerializer(serializers.ModelSerializer):
    # parent_lookup_kwargs = {
    #     'issue_pk': 'issue__pk',
    #     'project_pk': 'issue__project__pk',
    # }
    class Meta:
        model = Comments
        fields = ['id', 'description', 'author', 'issue', 'created_time']
        extra_kwargs = {'author': {'read_only': True}, 'issue': {'read_only': True}}

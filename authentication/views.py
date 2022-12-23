from django.contrib.auth import get_user_model
from django.shortcuts import render
from rest_framework import status, viewsets
from django.conf import settings
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserSerializer
from .models import User
from project.models import Projects


class CreateUserAPIView(APIView):
    # Allow any user (authenticated or not) to access this url
    permission_classes = (AllowAny,)

    def post(self, request):
        user = request.data
        serializer = UserSerializer(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self, *args, **kwargs):
        project_id = self.kwargs.get("projects_pk")
        project = None
        try:
            project = Projects.objects.get(id=project_id)
        except Projects.DoesNotExist:
            raise NotFound("Un project avec cet identifiant n'existe pas")
        return self.queryset.filter(project=project)

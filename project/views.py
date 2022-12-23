from rest_framework.decorators import api_view
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework import status, generics, viewsets, request
from rest_framework import permissions

from .models import Projects, Contributors, Comments, Issues
from .serializers import ProjectSerializer, ContributorSerializer, CommentSerializer, IssueSerializer


class ProjectListView(generics.ListCreateAPIView):
    queryset = Projects.objects.all()
    serializer_class = ProjectSerializer


class ProjectViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Projects.objects.all()
    serializer_class = ProjectSerializer

    def get_queryset(self):
        return self.queryset.filter(author=self.request.user)

    def perform_create(self, serializer):
        return serializer.save(author=self.request.user)


@api_view(['GET', 'PUT', 'DELETE'])
def project_detail(request, pk):
    try:
        project = Projects.objects.get(pk=pk)
    except Projects.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ProjectSerializer(project)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        serializer = ProjectSerializer(project, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        project.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ContributorListView(generics.ListCreateAPIView):
    queryset = Contributors.objects.all()
    serializer_class = ContributorSerializer


class ContributorViewSet(viewsets.ModelViewSet):
    queryset = Contributors.objects.all()
    serializer_class = ContributorSerializer

    def get_queryset(self, *args, **kwargs):
        project_id = self.kwargs.get("projects_pk")
        try:
            self.project = Projects.objects.get(id=project_id)
        except Projects.DoesNotExist:
            raise NotFound("Un project avec cet identifiant n'existe pas")
        return self.queryset.filter(project=self.project)

    def perform_create(self, serializer):
        # print(self.project)
        return serializer.save(project_id=self.kwargs.get("projects_pk"))


@api_view(['GET'])
def contributor_detail(request, pk):
    try:
        contributor = Contributors.objects.get(pk=pk)
    except Contributors.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ContributorSerializer(contributor)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CommentListView(generics.ListCreateAPIView):
    queryset = Comments.objects.all()
    serializer_class = CommentSerializer


class CommentViewSet(viewsets.ModelViewSet):
    issue = None

    queryset = Comments.objects.all().select_related(
        'issue'
    )
    serializer_class = CommentSerializer

    def get_queryset(self, *args, **kwargs):
        issue_id = self.kwargs.get("issues_pk")
        try:
            self.issue = Issues.objects.get(id=issue_id)
        except Issues.DoesNotExist:
            raise NotFound("Un problème avec cet identifiant n'existe pas")
        return self.queryset.filter(issue=self.issue)

    def perform_create(self, serializer):
        return serializer.save(issue_id=self.kwargs.get("issues_pk"), author=self.request.user)


@api_view(['GET'])
def comment_detail(request, pk):
    try:
        comment = Comments.objects.get(pk=pk)
    except Comments.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = CommentSerializer(comment)
        return Response(serializer.data, status=status.HTTP_200_OK)


class IssueListView(generics.ListCreateAPIView):
    queryset = Issues.objects.all()
    serializer_class = IssueSerializer


class IssueViewSet(viewsets.ModelViewSet):
    project = None

    queryset = Issues.objects.all()
    serializer_class = IssueSerializer

    def get_queryset(self, *args, **kwargs):
        project_id = self.kwargs.get("projects_pk")
        try:
            self.project = Projects.objects.get(id=project_id)
        except Projects.DoesNotExist:
            raise NotFound("Un project avec cet identifiant n'existe pas")
        return self.queryset.filter(project=self.project)

    # def create(self, request, *args, **kwargs):
    #  serializer = self.serializer_class(data=request.data)
    #  serializer.is_valid(raise_exception=True)
    #  self.perform_create(serializer)
    #  print(self.project)
    #  serializer.project=self.project
    #  serializer.save()
    #  headers = self.get_success_headers(serializer.data)
    #  return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        # print(self.project)
        return serializer.save(project_id=self.kwargs.get("projects_pk"), author=self.request.user)


@api_view(['GET'])
def issue_detail(request, pk):
    try:
        issue = Issues.objects.get(pk=pk)
    except Issues.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = IssueSerializer(issue)
        return Response(serializer.data, status=status.HTTP_200_OK)

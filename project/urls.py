from django.urls import path, include
from rest_framework.routers import SimpleRouter
from rest_framework_nested import routers
from . import views


router_project = SimpleRouter()
router_project.register('projects', views.ProjectViewSet, basename='projects')

issue_router = routers.NestedSimpleRouter(
    router_project,
    r'projects',
    lookup='projects')

issue_router.register(
    r'issues',
    views.IssueViewSet,
    basename='issues'
)

user_router = routers.NestedSimpleRouter(
    router_project,
    r'projects',
    lookup='projects')

user_router.register(
    r'users',
    views.ContributorViewSet,
    basename='users'
)

comment_router = routers.NestedSimpleRouter(
    issue_router,
    r'issues',
    lookup='issues')

comment_router.register(
    r'comments',
    views.CommentViewSet,
    basename='comments'
)

app_name = 'projects'

urlpatterns = [
    # path('projects/', views.ProjectListView.as_view()),
    # path('projects/<int:pk>/', views.project_detail),
    # path('projects/<int:pk>/issues/', views.IssueViewSet, name='project-liste-issues'),
    # path('projects/<int:pk>/issues/<int:pk>', views.IssueViewSet, name='project-liste-issues'),
    path('', include(router_project.urls)),
    path('', include(issue_router.urls, )),
    path('', include(comment_router.urls, )),
    path('', include(user_router.urls))
    # path('', include(comment_router.urls)),
    # path('contributors/', views.ContributorListView.as_view()),
    # path('contributors/<int:pk>/', views.contributor_detail),
    # path('comments/', views.CommentListView.as_view()),
    # path('comments/<int:pk>/', views.comment_detail),
    # path('', include(router.urls)),
    # path('issues/', views.IssueListView.as_view()),
    # path('issues/<int:pk>/', views.issue_detail),
]

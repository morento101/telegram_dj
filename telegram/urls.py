from django.urls import path
from .views import HomeView, RegisterView, LogoutView, GroupsListView, GroupDetailView, JoinGroupView, \
    CreateGroupView, UpdateProfileView, DeleteGroupView, MyLoginView, BrowseGroupsListView, ChatView, \
    SendMessageView
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', MyLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    path('groups/', GroupsListView.as_view(), name='groups'),
    path('group/<int:pk>/', GroupDetailView.as_view(), name='group_detail'),
    path('join_group/<int:pk>/', JoinGroupView.as_view(), name='join'),
    path('delete_group/<int:pk>/', DeleteGroupView.as_view(), name='delete_group'),
    path('create_group/', CreateGroupView.as_view(), name='create_group'),
    path('browse_groups/', BrowseGroupsListView.as_view(), name='browse_groups'),

    path('group_chat/<int:pk>', ChatView.as_view(), name='group_chat'),
    path('group_chat/send/', SendMessageView.as_view(), name='send_message'),

    path('update_profile/<int:pk>/', UpdateProfileView.as_view(), name='update_profile'),
]

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

    path('groups/', login_required(GroupsListView.as_view(), login_url='login'), name='groups'),
    path('group/<int:pk>/', login_required(GroupDetailView.as_view(), login_url='login'), name='group_detail'),
    path('join_group/<int:pk>/', login_required(JoinGroupView.as_view(), login_url='login'), name='join'),
    path('delete_group/<int:pk>/', login_required(DeleteGroupView.as_view(), login_url='login'), name='delete_group'),
    path('create_group/', login_required(CreateGroupView.as_view(), login_url='login'), name='create_group'),
    path('browse_groups/', login_required(BrowseGroupsListView.as_view(), login_url='login'), name='browse_groups'),

    path('group_chat/<int:pk>', login_required(ChatView.as_view(), login_url='login'), name='group_chat'),
    path('group_chat/send/', login_required(SendMessageView.as_view(), login_url='login'), name='send_message'),

    path('update_profile/<int:pk>/', login_required(UpdateProfileView.as_view(),
                                                    login_url='login'), name='update_profile'),
]

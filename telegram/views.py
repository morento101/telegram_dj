from django.contrib.auth.views import LoginView
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, TemplateView, UpdateView, DeleteView
from telegram.forms import CreateUserForm, LoginForm
from django.contrib.auth import logout
from django.contrib.auth.models import User
from .models import TeleGroup, UserProfile, Message
from django.db.models import Q
from django.contrib import messages as flash_messages
from django.contrib.auth.mixins import LoginRequiredMixin


class RegisterView(View):
    """
    Class-based view for registration
    """
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('groups')
        form = CreateUserForm()
        context = {'form': form}
        return render(request, 'telegram/register.html', context)

    def post(self, request):
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        else:
            print(type(form.errors))
            flash_messages.error(self.request, form.errors[list(form.errors.keys())[0]].as_text()[1:])
        context = {'form': form}
        return render(request, 'telegram/register.html', context)


class MyLoginView(LoginView):
    """
    Django generic view for login page
    """
    template_name = 'telegram/login.html'
    redirect_authenticated_user = True
    form_class = LoginForm
    success_message = 'Successfully logged in'

    def form_invalid(self, form):
        form_invalid = super(MyLoginView, self).form_invalid(form)
        flash_messages.error(self.request, form.errors[list(form.errors.keys())[0]].as_text()[1:])
        return form_invalid

    def get_success_url(self):
        return reverse_lazy('groups')


class LogoutView(LoginRequiredMixin, View):
    """
    Logout view based on View class
    """
    def get(self, request):
        logout(request)
        return redirect('groups')


class GroupsListView(LoginRequiredMixin, ListView):
    """
    Generic ListView where list of all user's groups are displayed
    """
    model = TeleGroup
    context_object_name = 'groups'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset().filter(follower=self.request.user)

        search = self.request.GET.get('search-area') or ''
        if search:
            queryset = queryset.filter(title__icontains=search)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        search = self.request.GET.get('search-area') or ''
        context['search'] = search

        return context


class GroupDetailView(LoginRequiredMixin, DetailView):
    """
    Detail view for all groups, where displayed all info about certain group
    """
    model = TeleGroup

    def get_context_data(self, **kwargs):
        context = super(GroupDetailView, self).get_context_data()
        context['followers'] = self.object.follower.all()
        return context


class JoinGroupView(LoginRequiredMixin, TemplateView):
    """
    View for joining to the certain group
    """
    template_name = 'telegram/group_response.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        group = get_object_or_404(TeleGroup, pk=kwargs['pk'])
        flag = group.add_user(self.request)

        if flag:
            context['response'] = f"You've joined to the group {group}"
        else:
            context['response'] = f"You're already in the group {group}"

        return context


class CreateGroupView(LoginRequiredMixin, CreateView):
    """
    View for creating new TeleGroup instance with obligatory two fields.
    Automate adding user to group and connecting owner to group
    """
    model = TeleGroup
    fields = ('title', 'description')

    def get_success_url(self):
        return reverse('groups')

    def form_valid(self, form):
        response = super().form_valid(form)
        self.object.add_user(self.request)
        self.object.connect_owner(self.request)
        return response


class DeleteGroupView(LoginRequiredMixin, DeleteView):
    """
    Delete TeleGroup instance from database.
    There are confirmation template. If form is submitted, then group is deleted
    """
    model = TeleGroup
    template_name = 'telegram/telegroup_confirm_delete.html'
    success_url = reverse_lazy('groups')


class UpdateProfileView(LoginRequiredMixin, UpdateView):
    """
    View for updating info in user's profile
    """
    model = UserProfile
    fields = ('username', 'phone', 'email', 'photo')
    template_name = 'telegram/update_profile.html'

    def get_success_url(self):
        return reverse('update_profile', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['response'] = 'Successfully changed data!'
        return context


class BrowseGroupsListView(LoginRequiredMixin, ListView):
    """
    View inherited from Django generic ListView for displaying
    groups which user does not follow with pagination
    """
    model = TeleGroup
    context_object_name = 'groups'
    template_name = 'telegram/browse_groups.html'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(~Q(follower=self.request.user))
        return queryset


class ChatView(LoginRequiredMixin, View):
    """
    Displays group's chat with all history
    """
    def get(self, request, pk):
        group = get_object_or_404(TeleGroup, pk=pk)
        if group:
            context = {'group': group}
            return render(request, 'telegram/chat.html', context)


class SendMessageView(LoginRequiredMixin, View):
    """
    View for AJAX request which creates new Message instance.
    Data is received from ChatView form
    """
    def post(self, request):
        user_pk = request.POST.get('user_pk')
        group_pk = request.POST.get('group_pk')
        message = request.POST.get('message')

        if message:
            new_message = Message.objects.create(
                user=User.objects.get(pk=user_pk), group=TeleGroup.objects.get(pk=group_pk), value=message
            )
            new_message.save()

        return HttpResponse('ok')

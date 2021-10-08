from django.contrib.auth.views import LoginView
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, TemplateView, UpdateView, DeleteView
from forms import CreateUserForm, LoginForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import TeleGroup, UserProfile, Message
from django.db.models import Q
from django.contrib import messages as flash_messages
from django.contrib.auth.hashers import check_password


class HomeView(View):
    def get(self, request):
        return redirect('groups')


class RegisterView(View):
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
    template_name = 'telegram/login.html'
    redirect_authenticated_user = True
    form_class = LoginForm
    success_message = 'Successfully logged in'

    def form_invalid(self, form):
        form_invalid = super(MyLoginView, self).form_invalid(form)
        flash_messages.error(self.request, form.errors[list(form.errors.keys())[0]].as_text()[1:])
        return form_invalid

    # def form_valid(self, form):
    #     form_valid = super(MyLoginView, self).form_valid(form)
    #     username = form.cleaned_data['username']
    #     password = form.cleaned_data['password']
    #     user = User.objects.get(username=username)
    #     if user:
    #         hash_pass = user.password
    #         check = check_password(password, hash_pass)
    #         if check:
    #             return form_valid
    #         else:
    #             messages.error(self.request, 'Password is not correct')
    #
    #     else:
    #         messages.error(self.request, 'User with such username does not exist')

    def get_success_url(self):
        return reverse_lazy('groups')


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('home')


class GroupsListView(ListView):
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


class GroupDetailView(DetailView):
    model = TeleGroup

    def get_context_data(self, **kwargs):
        context = super(GroupDetailView, self).get_context_data()
        context['followers'] = self.object.follower.all()
        return context


class JoinGroupView(TemplateView):
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


class CreateGroupView(CreateView):
    model = TeleGroup
    fields = ('title', 'description')

    def get_success_url(self):
        return reverse('groups')

    def form_valid(self, form):
        response = super().form_valid(form)
        self.object.add_user(self.request)
        self.object.connect_owner(self.request)
        return response


class DeleteGroupView(DeleteView):
    model = TeleGroup
    template_name = 'telegram/telegroup_confirm_delete.html'
    success_url = reverse_lazy('groups')


class GetProfileView(TemplateView):
    template_name = 'telegram/get_profile.html'


class UpdateProfileView(UpdateView):
    model = UserProfile
    fields = ('username', 'phone', 'email', 'photo')
    template_name = 'telegram/update_profile.html'

    def get_success_url(self):
        return reverse('get_profile', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['response'] = 'Successfully changed data!'
        return context


class BrowseGroupsListView(ListView):
    model = TeleGroup
    context_object_name = 'groups'
    template_name = 'telegram/browse_groups.html'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(~Q(follower=self.request.user))
        return queryset


class ChatView(View):
    def get(self, request, pk):
        group = get_object_or_404(TeleGroup, pk=pk)
        if group:
            context = {'group': group}
            return render(request, 'telegram/chat.html', context)


class SendMessageView(View):
    def post(self, request):
        user_pk = request.POST.get('user_pk')
        group_pk = request.POST.get('group_pk')
        message = request.POST.get('message')

        if message:
            new_message = Message.objects.create(
                user=User.objects.get(pk=user_pk), group=TeleGroup.objects.get(pk=group_pk), value=message
            )
            new_message.save()

        context = {'user_pk': user_pk, 'group_pk': group_pk, 'message': message}
        return HttpResponse('ok', context)


class GetMessagesView(View):
    def get(self, request, pk):
        group = get_object_or_404(TeleGroup, pk=pk)
        messages = Message.objects.filter(group=group).all()

        lst = []
        for message in messages:
            user_id = message.user_id
            user = get_object_or_404(User, pk=user_id)
            if user:
                username = user.username
                lst.append(username)

        context = {'messages': list(messages.values()), 'username': lst, 'current_user': request.user.username}

        return JsonResponse(context)

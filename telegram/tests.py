from django.http import QueryDict
from django.test import TestCase, RequestFactory, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .views import GroupDetailView, GroupsListView, BrowseGroupsListView
from .models import TeleGroup, UserProfile, Message


class Authentication(TestCase):
    def setUp(self) -> None:
        pass
        # self.factory = RequestFactory()

    def test_authentication_for_views_without_args(self):
        list_of_urls = [
            'logout', 'groups', 'create_group',
            'browse_groups', 'send_message',
                        ]
        responses = map(lambda a: self.client.get(reverse(a)), list_of_urls)

        for response in responses:
            self.assertEqual(response.status_code, 302)

    # def test_authentication_for_groups_view(self):
    #     logout_request = self.client.get(reverse('groups'))
    #     self.assertEqual(logout_request.status_code, 302)


class TelegroupLogicTestCases(TestCase):
    def setUp(self) -> None:
        self.factory = RequestFactory()
        self.request = self.factory.get('')
        self.user = User.objects.create(
            username='test_case',
            email='test_case@gmail.com',
            password='test_case_password',
        )
        self.client.force_login(self.user)
        self.group = TeleGroup.objects.create(
            title='test_group',
            description='test_group_description',
        )
        self.message = Message.objects.create(
            user=self.user,
            group=self.group,
            value='test_case_message_value',
        )

    def test_auto_creation_userprofile_for_user(self):
        self.assertEqual(self.user.userprofile,
                         UserProfile.objects.get(user=self.user)
                         )

    def test_add_user_to_owner_and_follower(self):
        self.factory = RequestFactory()
        self.request.user = self.user

        self.group.add_user(self.request)
        self.assertIn(self.user, self.group.follower.all())
        self.assertEqual(self.group.number_followers, 1)

        self.group.connect_owner(self.request)
        self.assertEqual(self.user, self.group.owner)

    def test_group_list_view(self):
        self.request.user = self.user
        self.group.add_user(self.request)
        a = GroupsListView()
        a.request = self.request
        queryset = GroupsListView.get_queryset(a)
        self.assertQuerysetEqual(queryset, TeleGroup.objects.all())

        # self.client.force_login(self.user)
        response = self.client.get(reverse('groups'), follow=True)
        self.assertContains(response, f'{self.group}')

    def test_group_list_view_search_area(self):
        self.request.user = self.user
        a = GroupsListView()
        a.request = self.request
        a.request = self.request
        a.request.GET = QueryDict('search-area=lol_stupid_search', mutable=True)
        queryset = GroupsListView.get_queryset(a)
        self.assertQuerysetEqual(queryset, TeleGroup.objects.filter(title__contains=a.request.GET.get('search-area')))

    def test_group_detail_view(self):
        self.request.user = self.user
        response = GroupDetailView.as_view()(self.request, pk=self.group.pk)
        self.assertEqual(response.status_code, 200)

    def test_create_group_view(self):
        self.client.post(
            reverse('create_group'),
            data={
                'title': 'test_create_group_title',
                'description': 'test_create_group_description',
            }
        )
        # import pdb; pdb.set_trace()
        self.assertEqual(TeleGroup.objects.filter(title='test_create_group_title').exists(), True)

    def test_delete_group_view_get(self):
        response = self.client.get(reverse('delete_group', args=(self.group.pk,)), follow=True)
        self.assertContains(response, f'Are are you sure you want to delete {self.group.title}')

    def test_delete_group_view_post(self):
        response = self.client.post(reverse('delete_group', args=(self.group.pk,)), follow=True)
        self.assertRedirects(response, reverse('groups'), status_code=302)

    def test_browse_groups_view(self):
        self.request.user = self.user
        self.client.force_login(self.user)

        a = BrowseGroupsListView()
        a.request = self.request
        queryset = BrowseGroupsListView.get_queryset(a)
        self.assertQuerysetEqual(queryset, TeleGroup.objects.all())

        response = self.client.get(reverse('browse_groups'))
        self.assertContains(response, f'{self.group.title}')

# TODO: add test for messages and others views

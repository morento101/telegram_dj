from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User
from .models import TeleGroup, UserProfile, Message


class TelegroupLogicTestCases(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create(
            username='test_case',
            email='test_case@gmail.com',
            password='test_case_password',
        )
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
        factory = RequestFactory()
        request = factory.get('')
        request.user = self.user

        self.group.add_user(request)
        self.assertIn(self.user, self.group.follower.all())
        self.assertEqual(self.group.number_followers, 1)

        self.group.connect_owner(request)
        self.assertEqual(self.user, self.group.owner)

# TODO: add test for messages and others views
# make 



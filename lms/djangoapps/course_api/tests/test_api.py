"""
Test for course API
"""

from lettuce import world
from django.test import RequestFactory

from xmodule.modulestore.tests.django_utils import ModuleStoreTestCase
from xmodule.modulestore.tests.factories import ToyCourseFactory

from lms.djangoapps.course_api.api import list_courses


class TestGetCourseList(ModuleStoreTestCase):
    """
    Test the behavior of the course list api
    """

    expected_course_data = {
        'blocks_url': '/api/courses/v1/blocks/?course_id=edX%2Ftoy%2F2012_Fall',
        'course_image': u'/c4x/edX/toy/asset/just_a_test.jpg',
        'description': u'A course about toys.',
        'end': None,
        'enrollment_end': None,
        'enrollment_start': None,
        'id': u'edX/toy/2012_Fall',
        'name': u'Toy Course',
        'number': u'toy',
        'org': u'edX',
        'start': u'2015-07-17T12:00:00Z',
        'start_display': u'July 17, 2015',
        'start_type': 'timestamp',
    }

    @classmethod
    def setUpClass(cls):
        super(TestGetCourseList, cls).setUpClass()
        cls.request_factory = RequestFactory()

    def setUp(self):
        super(TestGetCourseList, self).setUp()
        self.create_course()

    def create_user(self, username, email, password, is_staff):
        """
        Create a user as identified by username, email, password and is_staff.
        """
        user = world.UserFactory(
            username=username,
            email=email,
            password=password,
            is_staff=is_staff)
        return user

    def create_course(self):
        """
        Create a course for use in test cases
        """
        return ToyCourseFactory.create()

    def _api_shim(self, request, api_callable, user, username):
        """
        Wrap the call to `list_courses` in a view-like callable that takes a
        request object as the first argument.

        This needs to be here to make the `course_description` field work.  It
        looks for a request object as a first argument somewhere on the stack.
        """
        request.user = user
        return api_callable(user, username)

    def test_user_course_list_as_staff(self):
        request = self.request_factory.get('/')
        user = self.create_user("staff", "staff@example.com", "edx", True)
        courses = self._api_shim(request, list_courses, user, "staff")
        self.assertEqual([dict(course) for course in courses.data], [self.expected_course_data])

    def test_honor_user_course_list_as_staff(self):
        request = self.request_factory.get('/')
        user = self.create_user("staff", "staff@example.com", "edx", True)
        honor_user = self.create_user("honor", "honor@example.com", "edx", False)
        courses = self._api_shim(request, list_courses, user, honor_user.username)
        self.assertEqual([dict(course) for course in courses.data], [self.expected_course_data])

    def test_user_course_list_as_honor(self):
        request = self.request_factory.get('/')
        user = self.create_user("honor", "honor@example.com", "edx", False)
        courses = self._api_shim(request, list_courses, user, "honor")
        self.assertEqual(courses.data, [self.expected_course_data])

    def test_staff_user_course_list_as(self):
        request = self.request_factory.get('/')
        user = self.create_user("honor", "honor@example.com", "edx", False)
        with self.assertRaises(ValueError):
            self._api_shim(request, list_courses, user, "staff")

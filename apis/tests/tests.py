from django.test import TestCase
from apis.serializers import OrganizationNameSerializer
from faker import Faker
from unittest import mock
from django.http.response import HttpResponse
from apis.utils import AttrDict
from apis.tests import data_test
from rest_framework.exceptions import NotFound


# Create your tests here.
class OrganizationSerializerTest(TestCase):
    def setUp(self):
        fake = Faker()

        self.data = {
            "name": fake.name()
        }

    def test_required_fields(self):
        serializer = OrganizationNameSerializer(data={})
        is_valid = serializer.is_valid()

        expected_error = {
            "name": ["This field is required."]
        }

        self.assertFalse(is_valid)
        self.assertEqual(serializer.errors, expected_error)

    def test_blank_field(self):
        data = {
            "name": ""
        }
        serializer = OrganizationNameSerializer(data=data)
        is_valid = serializer.is_valid()

        expected_error = {
            "name": ["This field may not be blank."]
        }

        self.assertFalse(is_valid)
        self.assertEqual(serializer.errors, expected_error)

    @mock.patch("apis.serializers.requests.get",
                return_value=AttrDict(data_test.error_data))
    def test_org_not_found(self, *args):
        data = {
            "name": "abcdefgs"
        }
        serializer = OrganizationNameSerializer(data=data)

        with self.assertRaisesMessage(NotFound, ""):
            is_valid = serializer.is_valid()
            self.assertFalse(is_valid)

    @mock.patch("apis.serializers.requests.get",
                return_value=AttrDict(data_test.exist_data))
    def test_org_exist(self, *args):
        serializer = OrganizationNameSerializer(data=self.data)

        is_valid = serializer.is_valid()

        expected_data = self.data

        self.assertTrue(is_valid)
        self.assertEqual(serializer.data, expected_data)

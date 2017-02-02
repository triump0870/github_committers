from django.test import TestCase
from apis.serializers import OrganizationNameSerializer
from faker import Faker
from unittest import mock
from django.http.response import HttpResponse


# Create your tests here.
class OrganizationSerializerTest(TestCase):
    error_data = {
        "detail": "{'documentation_url': 'https://developer.github.com/v3', 'message': 'Not Found'}",
        "status_code": 404
    }

    def setUp(self):
        fake = Faker()

        self.data = {
            "name": fake.name
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
                return_value=error_data)
    def test_org_not_found(self, *args):
        data = {
            "name": "abcdefgs"
        }
        serializer = OrganizationNameSerializer(data=data)
        is_valid = serializer.is_valid()

        print("valid: ", is_valid)
        print("error: ", serializer.errors)

from logging import getLogger

import requests
from rest_framework import serializers
from rest_framework.exceptions import NotFound

from apis.utils import get_auth

logger = getLogger("apis")


class OrganizationNameSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=50, allow_blank=False, allow_null=False)

    def validate_name(self, name):
        github_org_api = "https://api.github.com/orgs/{org}".format(org=name)
        try:
            req = requests.get(github_org_api, auth=get_auth())
        except:
            logger.error("Errors occurred while fetching data from Github for [{}] API".format(github_org_api))

        if 400 <= req.status_code < 500:
            logger.error("Error found: \n[{}]".format(req.json()))
            raise NotFound(req.json())
        return name

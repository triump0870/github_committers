from logging import getLogger

from django.conf import settings
from django.core.cache import cache
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from rest_framework import status
from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response

from apis.serializers import OrganizationNameSerializer
from apis.utils import get_repos, get_contributors

logger = getLogger("apis")
CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


class Committers(ListCreateAPIView):
    """
    Calls the Github APIs for a particular organization and presents the top 5
    repositories based on the forks_count and lists top 3 committees based on
    the total commits.
    """
    serializer_class = OrganizationNameSerializer

    def get(self, request):
        return Response(status=status.HTTP_200_OK)

    def post(self, request):
        serializer = OrganizationNameSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            organization = serializer.data["name"]
            results = cache.get(organization, None)
            if not results:
                repos = get_repos(organization)
                results = []
                for repo in repos:
                    committees = get_contributors(repo["contributors_url"])
                    repo["committees"] = committees
                    results.append(repo)
                cache.set(organization, results)
            return Response(data=results, status=status.HTTP_200_OK)

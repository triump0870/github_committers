from logging import getLogger

import requests
from django.conf import settings
from django.core.cache import cache
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from requests.auth import HTTPBasicAuth
from rest_framework import status
from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response
from django.utils.decorators import method_decorator

from apis.serializers import OrganizationNameSerializer
from django.views.decorators.cache import cache_page

logger = getLogger("apis")
CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


class ListCommittee(ListCreateAPIView):
    """
    Calls the Github APIs for a particular organization and presents the top 5
    repositories based on the forks_count and lists top 3 committees based on
    the total commits.
    """
    serializer_class = OrganizationNameSerializer

    @method_decorator(cache_page(CACHE_TTL))
    def get(self, request):
        return Response(status=status.HTTP_200_OK)

    @method_decorator(cache_page(CACHE_TTL))
    def post(self, request):
        print("request: ", request.data)
        serializer = OrganizationNameSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            organization = serializer.data["name"]
            results = cache.get(organization, None)
            if not results:
                repos = self.get_repos(organization)
                results = []
                for repo in repos:
                    toppers = self.get_contributors(repo["contributors_url"])
                    repo["toppers"] = toppers
                    results.append(repo)
                cache.set(organization, results)
            return Response(data=results, status=status.HTTP_200_OK)

    def get_repos(self, org):
        forks = {}
        repos = {}
        results = []
        GITHUB_REPO_API = "https://api.github.com/orgs/{org}/repos?page=1&per_page=100".format(org=org)

        try:
            req = requests.get(GITHUB_REPO_API, auth=self.get_auth())
        except:
            logger.error("Error occurred while fetching data from [{}]".format(GITHUB_REPO_API))

        while True:
            for i in req.json():
                forks[i["id"]] = i["forks_count"]
                details = {
                    "id": i["id"],
                    "full_name": i["full_name"],
                    "url": i["html_url"],
                    "contributors_url": i["contributors_url"],
                    "forks_count": i["forks_count"]
                }
                repos[i["id"]] = details
            if "next" in req.links:
                # Traverse through pages to get all the repositories
                req = self.get_repos_for_link(req.links["next"]["url"])
            else:
                break

        _q = sorted(forks, key=forks.get, reverse=True)[:5]
        for i in _q:
            results.append(repos[i])
        return results

    @staticmethod
    def get_auth():
        """Attaches HTTP Basic Authentication to the given Request object."""

        return HTTPBasicAuth(settings.USERNAME, settings.PASSWORD)

    def get_repos_for_link(self, url):
        """Returns the repositories for the requested URL"""
        try:
            req = requests.get(url, auth=self.get_auth())
        except:
            logger.error("Error occurred while fetching data from [{}]".format(url))
        return req

    def get_contributors(self, url):
        """
        Returns a list of top 3 committees for the repo.

        :param url:
        :return:
        """
        committee = {}
        results = []
        res = {}
        api_link = "{url}/stats/contributors?page=1&per_page=100".format(url=url.rsplit('/', 1)[0])

        try:
            req = requests.get(api_link, auth=self.get_auth())
        except:
            logger.error("Error occurred while fetching data from [{}]".format(api_link))
            return results

        for i in req.json():
            try:
                res[i["author"]["id"]] = i["total"]
                details = {
                    "id": i["author"]["id"],
                    "name": i["author"]["login"],
                    "html_url": i["author"]["html_url"],
                    "commits": i["total"],
                }
                committee[i["author"]["id"]] = details

            except:
                pass

        _q = sorted(res.items(), key=lambda t: t[1], reverse=True)[:3]
        for i in _q:
            results.append(committee[i[0]])

        return results

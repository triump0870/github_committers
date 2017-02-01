from logging import getLogger

import requests
from django.conf import settings
from requests.auth import HTTPBasicAuth
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

logger = getLogger("apis")


class ListToppers(APIView):
    def get(self, request):
        organization = "github"
        repos = self.get_repos(organization)
        results = []
        for repo in repos:
            toppers = self.get_contributors(repo["contributors_url"])
            repo["toppers"] = toppers
            results.append(repo)
        return Response(data=results, status=status.HTTP_200_OK)

    def get_repos(self, org):
        repo_dict = {}
        repo_list_dict = {}
        results = []

        GITHUB_REPO_API = "https://api.github.com/orgs/{org}/repos?page=1&per_page=100".format(org=org)

        try:
            req = requests.get(GITHUB_REPO_API, auth=self.get_auth())
        except:
            logger.error("Error occurred while fetching data from [{}]".format(GITHUB_REPO_API))

        while True:
            for i in req.json():
                repo_dict[i["id"]] = i["forks_count"]
                details = {
                    "id": i["id"],
                    "full_name": i["full_name"],
                    "url": i["html_url"],
                    "contributors_url": i["contributors_url"],
                    "forks_count": i["forks_count"]
                }
                repo_list_dict[i["id"]] = details
            if "next" in req.links:
                req = self.get_repos_for_link(req.links["next"]["url"])
            else:
                break

        sorted_repo_list = sorted(repo_dict, key=repo_dict.get, reverse=True)[:5]
        for i in sorted_repo_list:
            results.append(repo_list_dict[i])
        return results

    @staticmethod
    def get_auth():
        return HTTPBasicAuth(settings.USERNAME, settings.PASSWORD)

    def get_repos_for_link(self, url):
        try:
            req = requests.get(url, auth=self.get_auth())
        except:
            logger.error("Error occurred while fetching data from [{}]".format(url))
        return req

    def get_contributors(self, url):
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

        toppers = sorted(res.items(), key=lambda t: t[1], reverse=True)[:3]
        for i in toppers:
            results.append(committee[i[0]])

        return results

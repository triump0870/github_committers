from logging import getLogger

import requests
from django.conf import settings
from requests.auth import HTTPBasicAuth

logger = getLogger("apis")


def get_repos(org):
    forks = {}
    repos = {}
    results = []
    github_repo_api = "https://api.github.com/orgs/{org}/repos?page=1&per_page=100".format(org=org)
    try:
        req = requests.get(github_repo_api, auth=get_auth())
    except:
        logger.error("Error occurred while fetching data from [{}]".format(github_repo_api))

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
            req = get_repos_for_link(req.links["next"]["url"])
        else:
            break

    _q = sorted(forks, key=forks.get, reverse=True)[:5]
    for i in _q:
        results.append(repos[i])
    return results


def get_auth():
    """Attaches HTTP Basic Authentication to the given Request object."""
    return HTTPBasicAuth(settings.USERNAME, settings.PASSWORD)


def get_repos_for_link(url):
    """Returns the repositories for the requested URL"""
    try:
        req = requests.get(url, auth=get_auth())
    except:
        logger.error("Error occurred while fetching data from [{}]".format(url))
    return req


def get_contributors(url):
    """
    Returns a list of top 3 committees for the repo.
    """
    committee = {}
    results = []
    res = {}
    api_link = "{url}/stats/contributors?page=1&per_page=100".format(url=url.rsplit('/', 1)[0])

    try:
        req = requests.get(api_link, auth=get_auth())
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


class AttrDict(dict):
    def __init__(self, *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self

    def json(self):
        return self.__dict__

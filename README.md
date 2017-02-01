## Description
Uses the Github APIs to get the top 3 committee for the top 5 repositories of a particular organization

## Request
    curl -H "Content-Type: application/json" -X POST http://localhost:8000/apis/list/ -d '{"name": "google"}'
    
## Response
    [
        {
            "url": "https://github.com/google/material-design-icons",
            "contributors_url": "https://api.github.com/repos/google/material-design-icons/contributors",
            "forks_count": 5304,
            "toppers": [
                {
                    "commits": 36,
                    "id": 3145577,
                    "name": "jestelle",
                    "html_url": "https://github.com/jestelle"
                },
                {
                    "commits": 25,
                    "id": 42326,
                    "name": "shyndman",
                    "html_url": "https://github.com/shyndman"
                },
                {
                    "commits": 9,
                    "id": 72062,
                    "name": "liquidx",
                    "html_url": "https://github.com/liquidx"
                }
            ],
            "full_name": "google/material-design-icons",
            "id": 24953448
        },
        {
            "url": "https://github.com/google/iosched",
            "contributors_url": "https://api.github.com/repos/google/iosched/contributors",
            "forks_count": 4829,
            "toppers": [
                {
                    "commits": 93,
                    "id": 4062052,
                    "name": "freewheelnat",
                    "html_url": "https://github.com/freewheelnat"
                },
                {
                    "commits": 79,
                    "id": 437242,
                    "name": "PaulRashidi",
                    "html_url": "https://github.com/PaulRashidi"
                },
                {
                    "commits": 37,
                    "id": 170296,
                    "name": "shailen",
                    "html_url": "https://github.com/shailen"
                }
            ],
            "full_name": "google/iosched",
            "id": 18347476
        },
        {
            "url": "https://github.com/google/protobuf",
            "contributors_url": "https://api.github.com/repos/google/protobuf/contributors",
            "forks_count": 4455,
            "toppers": [
                {
                    "commits": 477,
                    "id": 17011,
                    "name": "jskeet",
                    "html_url": "https://github.com/jskeet"
                },
                {
                    "commits": 227,
                    "id": 385366,
                    "name": "csharptest",
                    "html_url": "https://github.com/csharptest"
                },
                {
                    "commits": 213,
                    "id": 8551050,
                    "name": "xfxyjwf",
                    "html_url": "https://github.com/xfxyjwf"
                }
            ],
            "full_name": "google/protobuf",
            "id": 23357588
        },
        {
            "url": "https://github.com/google/material-design-lite",
            "contributors_url": "https://api.github.com/repos/google/material-design-lite/contributors",
            "forks_count": 4365,
            "toppers": [
                {
                    "commits": 457,
                    "id": 110953,
                    "name": "addyosmani",
                    "html_url": "https://github.com/addyosmani"
                },
                {
                    "commits": 430,
                    "id": 234957,
                    "name": "surma",
                    "html_url": "https://github.com/surma"
                },
                {
                    "commits": 332,
                    "id": 409615,
                    "name": "sgomes",
                    "html_url": "https://github.com/sgomes"
                }
            ],
            "full_name": "google/material-design-lite",
            "id": 29268051
        },
        {
            "url": "https://github.com/google/guava",
            "contributors_url": "https://api.github.com/repos/google/guava/contributors",
            "forks_count": 3399,
            "toppers": [
                {
                    "commits": 1139,
                    "id": 1703908,
                    "name": "cpovirk",
                    "html_url": "https://github.com/cpovirk"
                },
                {
                    "commits": 494,
                    "id": 2036304,
                    "name": "kluever",
                    "html_url": "https://github.com/kluever"
                },
                {
                    "commits": 418,
                    "id": 101568,
                    "name": "cgdecker",
                    "html_url": "https://github.com/cgdecker"
                }
            ],
            "full_name": "google/guava",
            "id": 20300177
        }
    ]
    
## Github APIs Used
* https://api.github.com/orgs/:org/repos
> Lists the repositories for the requested organization(:org)

* https://api.github.com/repos/:org/:repo/stats/contributors
> Lists the contributors
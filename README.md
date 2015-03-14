# Jason
Jason is a thin object mapper for REST services

[![Build Status](https://travis-ci.org/sourcelair/jason.svg)](https://travis-ci.org/sourcelair/jason)

## Getting started

```python
from datetime import datetime, timedelta
from jason import fields, Service

service = Service('localhost:11235', 'api/internal')

class User(service.Resource):
    username = fields.StringField()
    email = fields.EmailField()
    created = fields.DateTimeField()


two_days_ago = datetime.now() - timedelta(days=2)

recent_users = User.objects.filter(created__gte=two_days_ago)
```

## Examples

### Quering the GitHub API

```python
from github.models import GitHubUser


user = GitHubUser.objects.all()[0]


for repo in user.get_repos():
    print repo.name
```


## Testing
In order to run the jason tests, you have to
  1. install the dependencies from `requirements-dev.txt` (`pip install -r requirements-dev.txt`)
  2. run `nosetests --all-modules tests` in your terminal

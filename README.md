# Jason
Jason is a thin object mapper for REST services

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

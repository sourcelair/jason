from .service import github
import jason
import os


class GitHubUser(github.Resource):
    _root = 'users'
    
    login = jason.fields.StringField()
    
    def get_endpoint(self):
        endpoint = os.path.join(
            self.service.base_url,
            GitHubUser.get_root(),
            self.login
        )
        return endpoint


class GitHubRepo(github.Resource):
    _root = 'repos'
    
    def get_endpoint(self):
        endpoint = os.path.join(self.owner.get_endpoint())
        return endpoint
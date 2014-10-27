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
    
    def get_repos(self):
        user_repos_root = os.path.join(self.get_endpoint(), 'repos')
        return GitHubRepo.objects.query_at(user_repos_root)


class GitHubRepo(github.Resource):
    _root = 'repos'
    
    def get_endpoint(self):
        endpoint = os.path.join(
            'repos',
            self.owner.login,
            self.name
            
        )
        return endpoint
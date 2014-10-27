from .service import github


class GitHubUser(github.Resource):
    _root = 'users'


class GitHubRepo(github.Resource):
    pass
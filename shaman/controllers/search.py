from pecan import expose, abort
from shaman.models import Repo, Project
from sqlalchemy import desc


class SearchController(object):

    def __init__(self):
        self.filters = {
                'distro': Repo.distro,
                'distro_version': Repo.distro_version,
                # TODO: figure out archs
                #'arch': Repo.arch,
                'ref': Repo.ref,
                'sha1': Repo.sha1,
                'flavor': Repo.flavor,
                'status': Repo.status,
        }

    @expose('json')
    def index(self, **kw):
        """
        Supported query args:
        distros: distro/distro_version or distro/distro_codename
        sha1: actual sha1 or "latest"
        ref: limit by ref
        flavor: limit by flavor
        status: limit by status
        """
        query = self.apply_filters(kw)
        if not query:
            return []
        return query.order_by(desc(Repo.modified)).all()

    def apply_filters(self, filters):
        # TODO: allow operators
        try:
            project = Project.filter_by(name=filters.pop('project')).first()
            query = Repo.filter_by(project=project)
        except KeyError:
            query = Repo.query
        for k, v in filters.items():
            if k not in self.filters:
                # TODO: improve error reporting
                # 'invalid query params: %s' % k
                abort(400)
            if k in self.filters:
                query = self.filter_repo(k, v, query)
        return query

    def filter_repo(self, key, value, query=None):
        filter_obj = self.filters[key]

        if key == 'sha1' and value == 'latest':
            # TODO:
            # recurse with the latest 50 (?) known built sha1s to find a common
            # one that exists for all.
            # return query.filter()
            # stub:
            pass
        # query will exist if multiple filters are being applied, e.g. by name
        # and by distro but otherwise it will be None
        if query:
            return query.filter(filter_obj == value)
        return Repo.query.filter(filter_obj == value)

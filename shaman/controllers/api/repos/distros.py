from pecan import request, expose, abort
from shaman.models import Project, Repo
from sqlalchemy import desc
from shaman.controllers.api.repos import flavors as _flavors


class DistroVersionController(object):

    def __init__(self, distro_version_name):
        self.distro_version_name = distro_version_name
        request.context['distro_version'] = distro_version_name
        self.project = Project.query.get(request.context['project_id'])
        self.repos = Repo.query.filter_by(
            project=self.project,
            ref=request.context['ref'],
            sha1=request.context['sha1'],
            distro=request.context['distro'],
            distro_version=distro_version_name,
            flavor='default').order_by(desc(Repo.modified)).all()

    @expose(generic=True, template='json')
    def index(self):
        abort(405)

    @index.when(method='GET', template='json')
    def index_get(self):
        return [r for r in self.repos]

    flavors = _flavors.FlavorsController()


class DistroController(object):

    def __init__(self, distro_name):
        self.distro_name = distro_name
        request.context['distro'] = distro_name
        self.project = Project.query.get(request.context['project_id'])
        self.repos = Repo.query.filter_by(
            project=self.project,
            ref=request.context['ref'],
            distro=distro_name).all()

    @expose(generic=True, template='json')
    def index(self):
        abort(405)

    @index.when(method='GET', template='json')
    def index_get(self):
        return list(
            set([r.distro_version for r in self.repos])
        )

    @expose()
    def _lookup(self, distro_version_name, *remainder):
        return DistroVersionController(distro_version_name), remainder

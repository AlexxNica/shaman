import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship, backref, deferred
from sqlalchemy.event import listen
from sqlalchemy.orm.exc import DetachedInstanceError
from shaman.models import Base, update_timestamp
from shaman.models.types import JSONType


class Build(Base):

    __tablename__ = 'builds'
    id = Column(Integer, primary_key=True)
    url = Column(String(256))
    log_url = Column(String(256))
    build_id = Column(String(64), index=True)
    ref = Column(String(256), index=True)
    sha1 = Column(String(256), index=True)
    flavor = Column(String(256), nullable=False, index=True, default="default")
    started = Column(DateTime, index=True)
    completed = Column(DateTime, index=True)
    modified = Column(DateTime, index=True)
    status = Column(String(256), index=True)
    extra = deferred(Column(JSONType()))

    project_id = Column(Integer, ForeignKey('projects.id'))
    project = relationship('Project', backref=backref('builds', lazy='dynamic'))

    allowed_keys = [
        'url',
        'log_url',
        'build_id',
        'ref',
        'sha1',
        'flavor',
        'status',
        'extra',
    ]

    def __init__(self, project, **kwargs):
        self.project = project
        self.modified = datetime.datetime.utcnow()
        self.update_from_json(kwargs)
        self.started = datetime.datetime.utcnow()

    def __repr__(self):
        try:
            return "<Build {}/{}/{}>".format(
                self.project.name,
                self.ref,
                self.sha1,
            )
        except DetachedInstanceError:
            return '<Build detached>'

    def __json__(self):
        return dict(
            url=self.url,
            log_url=self.log_url,
            build_id=self.build_id,
            ref=self.ref,
            sha1=self.sha1,
            flavor=self.flavor,
            status=self.status,
            extra=self.extra,
            modified=self.modified,
            project=self.project.name,
        )

    def get_url(self):
        """
        This model object is mainly consumed by the UI. Since the template will
        not always have a full concept of what a url part means, this helper
        method will construct what the (full) relative URL to this object is.
        """
        url = "/builds/{project}/{ref}/{sha1}/{flavor}/{build_id}/"
        return url.format(
            project=self.project.name,
            ref=self.ref,
            sha1=self.sha1,
            flavor=self.flavor or 'default',
            build_id=self.build_id
        )


# listen for timestamp modifications
listen(Build, 'before_insert', update_timestamp)
listen(Build, 'before_update', update_timestamp)

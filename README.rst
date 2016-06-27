shaman
======
A REST API that serves as the source of truth for the state of
repositories on chacra nodes. It can be queried to get information
on what branches and sha1's are built and available for ceph.

It also acts as an orchestration service for a pool of chacra nodes,
allowing for horizontal scalability.


Configuration
=============


API Endpoints
=============

The parent endpoint for any API interaction is ``/api/``.

Shaman has three top level endpoints:

- ``repos``
  This endpoint is used to view and add/update repositories.

- ``search``
  This endpoint is used to perform searches against repositories.

- ``nodes``
  This endpoint is used to list the available chacra nodes as well
  as retrieve the next chacra node in the rotation.

GET /api/repos/
---------------

Returns a list of projects that shaman has repo
information about.

POST /api/repos/(project)/
----------------------

Used to add / update repos for a given project. You must
POST a json object with the following data::

    {
        "distro": "Ubuntu",
        "distro_version": "Trusty",
        "ref": "jewel",
        "sha1": "45107e21c568dd033c2f0a3107dec8f0b0e58374",
        "url": "https://chacra.ceph.com/r/ceph/jewel/ubuntu/trusty/",
        "arch": "x86_64",
        "created": "2016-06-14 14:04:54.671504",
        "modified" "2016-06-15 14:04:54.671504",
        "is_queued": False,
        "is_updating": True,
        "ready": False
    }

GET /api/search/(project)/(ref|sha1)/
--------------------------------

This endpoint is used to query for repos by ref or sha1. It will return metadata about
the latest built repository or repositories that matches your search criteria. 

A GET to ``/repos/ceph/master/`` would return the a list of all repos
for the ``master`` ref::

   [
     {
       "ref": "master",
       "sha1": "8d48f5413564b418a8016b6a344b517282a0f0fa",
       "distro": "ubuntu",
       "distro_version": "trusty",
       "url": "https://chacra.ceph.com/r/ceph/master/8d48f5413564b418a8016b6a344b517282a0f0fa/ubuntu/trusty/",
       "arch": "x86_64",
       "created": "2016-06-14 14:04:54.671504",
       "modified" "2016-06-15 14:04:54.671504",
       "is_queued": True,
       "is_updating": False,
       "ready": False,
     },
     {
       "ref": "master",
       "sha1": "8d48f5413564b418a8016b6a344b517282a0f0fa",
       "distro": "ubuntu",
       "distro_version": "xenial",
       "url": "https://chacra.ceph.com/r/ceph/jewel/8d48f5413564b418a8016b6a344b517282a0f0fa/ubuntu/xenial/",
       "arch": "x86_64",
       "created": "2016-06-14 14:04:54.671504",
       "modified" "2016-06-15 14:04:54.671504",
       "is_queued": False,
       "is_updating": False,
       "ready": True,
     },
     ...
   ]

The following querystring parameters are supported.

- ``distros``
  A list of distros in ``distro.distro_version`` or ``distro`` format.
  i.e. ``?distros=ubuntu, centos.7``

- ``arch``
  Filter by architecture. i.e. ``?arch=x86_64``

- ``common_sha1``
  Requires that the repos return be built for a common sha1
  across all given distros. If a common built sha1 is not found
  for distros then no results are returned.
  i.e. ``?common_sha1=True&distros=centos.7,ubuntu.xenial``

If you choose to use ``sha1`` instead of ``ref`` at this endoint, the ``common_sha1``
parameter would not be effective.

GET /api/nodes/
-----------

Returns a list of the chacra nodes available in the pool::

    ["https://chacra01.ceph.com", "https://chacra02.ceph.com"]

POST /api/nodes/
-----------

This endpoint is used to add a new chacra node to the pool.

You must POST a json object representing the new chacra node::

    {"url": "http://chacra03.ceph.com"}


GET /api/nodes/next/
----------------

Returns the url for the next chacra node in the rotation,
in plain text::

    "https://chacra02.ceph.com"

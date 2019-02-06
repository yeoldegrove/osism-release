# OSISM release repository

[![Build Status](https://travis-ci.org/osism/release.svg?branch=master)](https://travis-ci.org/osism/release)

**NOTE**: The release with the highest number is always the latest/master release and can/will be changed in the future. It is recommended not to use the latest/master release in productive environments.

## How to add a new Ansible role

**NOTE**: New roles can only be added in the last release.

Add an entry to the ``etc/roles.yml`` file.

In the release directory ``latest`` add an entry to the ``ansible_roles`` parameter in the ``base.yml`` file.

## How to add a new Docker image

**NOTE**: New images can only be added in the last release.

Add an entry to the ``etc/images.yml`` file.

In the ``latest`` release directory add an entry to the ``docker_images`` parameter in the ``base.yml`` file.

Push a snapshot of the new image with ``IMAGES=name_of_the_new_image OSISM_VERSION=YYYY.X.0 python src/images.py``.

## How to prepare the next release

**NOTE**: The name of a new release follows the scheme ``YYYY.X.0``.

* Copy the release directory ``latest`` to the new release directory (e.g. ``2019.1.0``)
* Set the ``repository_version`` parameter in the ``base.yml`` file to the appropriate value.
* Commit the prepared release with the message ``New release: YYYY.X.0``. Make further changes in subsequent commits.
* Push snapshots of all required images with ``OSISM_VERSION=2019.1.0 python src/images.py``. The ``src/images.py`` script is part of the ``release`` repository.

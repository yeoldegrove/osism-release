#!/usr/bin/env python

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import sys

import docker
import json
import yaml

OSISM_VERSION = os.environ.get("OSISM_VERSION", "latest")

with open("%s.yml" % OSISM_VERSION, "rb") as fp:
    versions = yaml.load(fp)

with open("images.yml", "rb") as fp:
    images = yaml.load(fp)

docker_images = versions['docker_images']
docker_client = docker.APIClient(base_url='unix://var/run/docker.sock')

for image in versions['docker_images']:
    if image in ['rally', 'helper']:
        continue

    if not images[image][:5] == 'osism':
        if image == 'ceph':
            target = 'osism/ceph-daemon'
        else:
            target = "osism/" + images[image][images[image].find('/') + 1:]
    else:
        target = images[image]

    target_tag = versions['repository_version']
    if image in ['cephclient', 'openstackclient', 'ceph']:
        target_tag = versions['docker_images'][image] + '-' + target_tag

    source_tag = versions['docker_images'][image]
    if image == 'ceph':
        source_tag = "tag-build-master-%s-ubuntu-16.04" % source_tag

    print("pulling - %s:%s" % (images[image], source_tag))
    docker_client.pull(images[image], source_tag)

    print("tagging - %s:%s" % (target, target_tag))
    docker_client.tag("%s:%s" % (images[image], source_tag), target, target_tag)

    print("pushing - %s:%s" % (target, target_tag))
    docker_client.push(target, target_tag)

    print("removing - %s:%s" % (images[image], source_tag))
    docker_client.remove_image("%s:%s" % (images[image], source_tag))

    print("removing - %s:%s" % (target, target_tag))
    docker_client.remove_image("%s:%s" % (target, target_tag))
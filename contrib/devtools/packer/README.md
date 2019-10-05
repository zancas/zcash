What
====

It's possible to simply install packer using your package manager.  The approach outlined below
provides a shareable snapshot of the tool, along with code as documentation detailing its build.

This PR provides developers with the ability to produce Virtual Machine Images with minimal effort.

Included features:

* minimal prerequisites:
     - a development environment that includes Docker
     - sufficient authority for resource allocation (e.g. AWS key and key ID)
* maximal auditability; where possible content-based hashes are included in the code
     - TODO: Find and verify the signature
          The base image is the "Official" golang image as described here:
https://hub.docker.com/layers/golang/library/golang/latest/images/sha256-a50a9364e9170ab5f5b03389ed33b9271b4a7b6bbb0ab41c4035adb3078927bc
     - The "source_ami" is from this list: https://wiki.debian.org/Cloud/AmazonEC2Image/Buster
* portability:
     - Produced Docker images are small enough to transfer conveniently
* optionality:
     - Build it yourself, or use a standard image
* composeability:
    - The tool is intended to be a component of a more complete CI solution
    - The included AWS config, is only one example of use

This utility produces computer Machine Images with minimal configuration by the User.

How
===

Running (Run this only if you trust me!  You can check my GPG signature on the commits.)
----------
1. Setup a development environment with docker.
2. Edit the contents of "packer_build.sh" in the hopefully self-explanatory way.
3. `chmod +x ./packer_build.sh`
4. `./packer_build.sh aws/gitlabrunner.json`

Building
--------
1. build the runner:
```BASH
cd ./contrib/devtools/packer && chmod +x publish_new_image.sh && ./publish_new_image.sh
```

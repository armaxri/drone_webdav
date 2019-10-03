#!/usr/bin/env bash

docker build -t arnemaxr/drone-webdav .
docker run --env-file .env -v ${PWD}:/work --workdir /work -it arnemaxr/drone-webdav

# To publish the tested result:
#docker push arnemaxr/drone-webdav
# Build and publish:
#docker build -t arnemaxr/drone-webdav:stable . & docker push arnemaxr/drone-webdav:stable

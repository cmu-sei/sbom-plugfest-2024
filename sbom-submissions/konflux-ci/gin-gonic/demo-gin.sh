#!/bin/bash
# Generate build-time sbom with cachi2
#
# The focus is on accuracy: perform the build with no network to be sure that
# no components get pulled in that aren't explicitly handled by cachi2
# pre-fetch.
#
# Steps:
#  (0) Get the target repository
#  (1) Pre-process: nothing to do.
#  (2) Run cachi2 to pre-fetch dependencies.
#  (3) Run the build with no network, providing cachi2 output.
#  (4) Post-process: declare base/builder images used and the build itself.
#  (5) Bonus! Upload to OCI registry so consumers of build can discover the SBOM.
#
# Author: Ralph Bean <rbean@redhat.com>
#
# * Inspired by cachi2 bundler demo by Michal Šoltis @slimreaper35
# * Post-processing borrowed from the https://konflux-ci.dev/ hermetic build pipeline

set -e

## (0) Get the target repository
DESTINATION=quay.io/rbean/sbom/plugfest/gin-gonic:latest
ORIGIN=git@github.com:gin-gonic/gin
COMMIT=f05f966a0824b1d302ee556183e2579c91954266
git clone $ORIGIN || echo "Repo already exists?"
# Copy in some build instructions
cp Containerfile.gin gin/Containerfile
pushd gin
git checkout $COMMIT

## (1) Pre-process: nothing to do

## (2) Run cachi2 to pre-fetch dependencies.
cachi2 fetch-deps gomod
cachi2 inject-files --for-output-dir /tmp/cachi2-output cachi2-output
cachi2 generate-env --for-output-dir /tmp/cachi2-output --output cachi2.env cachi2-output

# Make a copy of the sbom. If the build in (3) succeeds, we know this sbom is valid.
cp cachi2-output/bom.json sbom.cyclonedx.json

## (3) Run the build with no network, providing cachi2 output.
buildah build \
    --volume "$(realpath ./cachi2-output)":/tmp/cachi2-output:Z \
    --volume "$(realpath ./cachi2.env)":/tmp/cachi2.env:Z \
    --network none \
    --tag $DESTINATION \
    .

# Push to the registry and capture the digest
buildah push --digestfile image-digest "$DESTINATION" "docker://$DESTINATION"

## (4) Post-process: declare base/builder images used and the build itself.
# Extract list of base / builder images used
podman run -it \
    -v .:/src:Z \
    -u root \
    quay.io/konflux-ci/buildah-task:latest@sha256:b2d6c32d1e05e91920cd4475b2761d58bb7ee11ad5dff3ecb59831c7572b4d0c \
        dockerfile-json /src/Containerfile > parsed_dockerfile.json
BASE_IMAGES=$(
    jq -r '.Stages[] | select(.From | .Stage or .Scratch | not) | .BaseName | select(test("^oci-archive:") | not)' parsed_dockerfile.json
)
touch base_images_digests
for image in $BASE_IMAGES; do
  base_image_digest=$(buildah images --format '{{ .Name }}:{{ .Tag }}@{{ .Digest }}' --filter reference="$image")
  # In some cases, there might be BASE_IMAGES, but not any associated digest. This happens
  # if buildah did not use that particular image during build because it was skipped
  if [ -n "$base_image_digest" ]; then
    echo "$image $base_image_digest" >> base_images_digests
  fi
done

# Inject references to the base / builder images into the sbom
podman run -it \
    -v .:/src:Z \
    -u root \
    quay.io/redhat-appstudio/sbom-utility-scripts-image@sha256:e1347023ef1e83d52813c26384f551e3a03e482539d17a647955603e7ea6b579 \
        python3 /scripts/base_images_sbom_script.py \
          --sbom=/src/sbom.cyclonedx.json \
          --parsed-dockerfile=/src/parsed_dockerfile.json \
          --base-images-digests=/src/base_images_digests

# Inject a reference to the resultant image into the sbom
podman run -it \
    -v .:/src:Z \
    -u root \
    quay.io/redhat-appstudio/sbom-utility-scripts-image@sha256:e1347023ef1e83d52813c26384f551e3a03e482539d17a647955603e7ea6b579 \
        python3 /scripts/add_image_reference.py \
          --image-url "$DESTINATION" \
          --image-digest "$(cat image-digest)" \
          --input-file /src/sbom.cyclonedx.json \
          --output-file /src/sbom.cyclonedx.tmp.json

mv sbom.cyclonedx.tmp.json sbom.cyclonedx.json

## (5) Bonus! Upload to OCI registry so consumers of build can discover the SBOM.
oras attach --artifact-type "application/vnd.cyclonedx+json" "$DESTINATION@$(cat image-digest)" "sbom.cyclonedx.json:application/vnd.cyclonedx+json"

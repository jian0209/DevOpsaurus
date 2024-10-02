#! /bin/bash

image_name=$1
tag=$2

if [ -z "$image_name" ]; then
    echo "Please provide an image name for the docker image."
    exit 1
fi

if [ -z "$tag" ]; then
    echo "Please provide a tag for the docker image."
    exit 1
fi

echo "Logging in to Docker Hub..."
docker login -u jian0209 --password-stdin < docker_example_file/docker_password.txt

echo "Building the docker image..."
docker buildx build \
  --platform linux/amd64,linux/arm64 \
  --push \
  -t jian0209/$image_name:$tag \
  -t jian0209/$image_name:latest \
  .

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

echo "Building the docker image..."
docker buildx build --platform linux/amd64 -t $image_name-amd64:latest .
docker buildx build --platform linux/arm64 -t $image_name-arm64:latest .

echo "Tagging the docker image..."
docker tag $image_name-amd64:latest jian0209/$image_name:$tag-amd64
docker tag $image_name-arm64:latest jian0209/$image_name:$tag-arm64
docker tag $image_name-amd64:latest jian0209/$image_name:latest-amd64
docker tag $image_name-arm64:latest jian0209/$image_name:latest-arm64

echo "Logging in to Docker Hub..."
docker login -u jian0209 --password-stdin < docker_example_file/docker_password.txt

echo "Pushing the docker image..."
docker push jian0209/$image_name:$tag-amd64
docker push jian0209/$image_name:$tag-arm64
docker push jian0209/$image_name:latest-amd64
docker push jian0209/$image_name:latest-arm64

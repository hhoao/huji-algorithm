#!/usr/bin/env bash
set -euo pipefail

repository_root=$(git rev-parse --show-toplevel)
build_env="${repository_root}/docker/build.env"
if [ -f "$build_env" ]; then
  # shellcheck disable=SC1090
  source "$build_env"
fi

docker_registry="${DOCKER_REGISTRY:-}"
branch=$(git symbolic-ref --short HEAD)
image_name='autoclip-algorithm'

docker_file_dir=$repository_root/docker/autoclip-algorithm/internal

cd "$repository_root" || exit
git archive "$branch" --format=tar.gz --output="${docker_file_dir}"/"${image_name}".tar.gz

cd "${docker_file_dir}" || exit
tar -xzf "${image_name}".tar.gz -C ./ requirements.txt

docker build --progress=plain . -t "${image_name}":latest

docker tag "${image_name}":latest "${image_name}":1.0

if [ -n "$docker_registry" ]; then
  docker tag "${image_name}":latest "${docker_registry}/${image_name}:1.0"
  docker tag "${image_name}":latest "${docker_registry}/${image_name}:latest"
  docker push "${docker_registry}/${image_name}:1.0"
  docker push "${docker_registry}/${image_name}:latest"
  echo "Pushed to ${docker_registry}/${image_name}"
else
  echo "DOCKER_REGISTRY not set — built locally only (no push). See docker/build.env.example"
fi

rm -rf "${image_name}".tar.gz requirements.txt

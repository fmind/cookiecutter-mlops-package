# run docker tasks
[group('docker')]
docker: docker-build docker-run

# build docker image
[group('docker')]
docker-build tag="latest": package-build
    {% raw %}docker build --tag={{REPOSITORY}}:{{tag}} .{% endraw %}

# start docker compose
[group('docker')]
docker-compose:
    docker compose up

# run latest docker image
[group('docker')]
docker-run tag="latest":
    {% raw %}docker run --rm {{REPOSITORY}}:{{tag}}{% endraw %}

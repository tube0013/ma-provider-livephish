# the base of the official server image: Python, ffmpeg and the system libraries the server needs
FROM ghcr.io/music-assistant/base:1.7.1

# git for the server installed from its source; the compilers for a server requirement that is
# built from source
RUN apt-get update \
    && apt-get install -y --no-install-recommends git gcc g++ \
    && rm -rf /var/lib/apt/lists/*

COPY --from=ghcr.io/astral-sh/uv:0.13.8 /uv /uvx /bin/

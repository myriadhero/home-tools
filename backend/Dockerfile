# container user for the initial build
FROM python:3.9-alpine AS builder

ARG CODE_DIR

WORKDIR ${CODE_DIR}
RUN pip install pipenv

COPY ./Pipfile ./Pipfile.lock ${CODE_DIR}/

# set environment variables
ENV PIPENV_VENV_IN_PROJECT=1
ENV PIPENV_CACHE_DIR=${CODE_DIR}/pipenv_cache/

RUN pipenv sync

# Runtime container from this line
FROM python:3.9-alpine AS runtime
ARG CODE_DIR
ARG USER=djangouser
ARG UGROUP=djangogroup

WORKDIR ${CODE_DIR}
COPY --from=builder ${CODE_DIR}/.venv/ ./.venv/

# Finalise the image here
ARG DOCKER_WORLD_PORT
ENV VIRTUAL_ENV=${CODE_DIR}/.venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
ENV OUTER_WORLD_PORT=${DOCKER_WORLD_PORT}
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV STATICFILES_DIR=${CODE_DIR}/staticfiles

COPY ./backend ./app
RUN mkdir staticfiles

RUN addgroup -S ${UGROUP} && adduser -S ${USER} -G ${UGROUP} && chown -R ${USER}:${UGROUP} ${CODE_DIR}/app
WORKDIR ${CODE_DIR}/app

USER ${USER}

# entry point used for DB and other services to boot up
# ENTRYPOINT [ "executable" ]
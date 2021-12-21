FROM python:3.10.1-slim-bullseye as base

# Setup env
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONFAULTHANDLER 1

RUN apt-get update && apt-get install -y --no-install-recommends mariadb-client poppler-utils antiword libmagic-dev

FROM base AS python-deps

# Install pipenv and compilation dependencies
RUN apt-get update && apt-get install -y --no-install-recommends gcc libmariadbclient-dev-compat

RUN pip install pipenv

# Create and switch to a new user
RUN useradd --create-home appuser
WORKDIR /home/appuser
USER appuser

# Install python dependencies in /.venv
COPY Pipfile .
COPY Pipfile.lock .
RUN PIPENV_VENV_IN_PROJECT=1 pipenv install --deploy

FROM base AS runtime

# Create and switch to a new user
RUN useradd --create-home appuser --uid 1010
WORKDIR /home/appuser

ENV PATH="/home/appuser/.venv/bin:$PATH"

# Run the application
ENTRYPOINT ["/home/appuser/entrypoint.sh"]
CMD ["gunicorn", "app.wsgi:application", "--bind", "0.0.0.0:8000", "--access-logfile", "-"]

# Copy virtual env from python-deps stage
COPY --from=python-deps /home/appuser/.venv /home/appuser/.venv

# Install application into container
COPY . .

EXPOSE 8000/tcp
VOLUME /home/appuser/media

RUN ["python", "/home/appuser/manage.py", "collectstatic", "--noinput"]

USER appuser

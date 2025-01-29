FROM mcr.microsoft.com/devcontainers/python:0-3.10

ENV PYTHONUNBUFFERED 1

WORKDIR /app

# [Optional] Uncomment this section to install additional OS packages.
# RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
#     && apt-get -y install --no-install-recommends <your-package-list-here>
RUN sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'

# Import the repository signing key:
RUN wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -

# Update the package lists:
RUN apt-get update

# Install the latest version of PostgreSQL.
# If you want a specific version, use 'postgresql-12' or similar instead of 'postgresql':
RUN apt-get -y install postgresql-12

# [Optional] If your requirements rarely change, uncomment this section to add them to the image.
RUN pip install --upgrade pip

COPY requirements.txt /tmp/pip-tmp/
RUN pip --disable-pip-version-check --no-cache-dir install -r /tmp/pip-tmp/requirements.txt \
    && rm -rf /tmp/pip-tmp

# Production
COPY app.py .
COPY src ./src

CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:8000", "app:app"]
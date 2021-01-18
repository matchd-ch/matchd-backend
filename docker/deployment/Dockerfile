FROM docker.gitlab.liip.ch/matchd/docker-images/python-38-centos7:latest
ENV DJANGO_ENV dev

USER root

COPY ./docker/deployment/docker-entrypoint.sh /usr/local/bin/docker-entrypoint
RUN chmod +x /usr/local/bin/docker-entrypoint

USER 1001

WORKDIR '/opt/app-root/src'

COPY requirements.txt '/opt/app-root/src'

RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . '/opt/app-root/src'
COPY app/wsgi.py .

EXPOSE 8080

ENTRYPOINT ["docker-entrypoint"]
CMD ["/usr/libexec/s2i/run"]


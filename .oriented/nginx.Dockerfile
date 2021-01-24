FROM centos/nginx-112-centos7:latest

ARG PROXY_URL

USER 0

COPY ./.oriented/nginx nginx

RUN yum install -y --setopt=tsflags=nodocs httpd-tools && \
  rpm -V httpd-tools && \
  yum clean all -y && \
  mv nginx/mime.types /opt/app-root/etc/ && \
  sed "s|\$PROXY_URL|${PROXY_URL}|g;" nginx/nginx.conf.template > /opt/app-root/etc/nginx.conf && \
  rm -rf nginx && \
  yum remove -y httpd-tools && \
  yum clean all -y

USER 1001

EXPOSE 8080

CMD ["nginx", "-c", "/opt/app-root/etc/nginx.conf"]

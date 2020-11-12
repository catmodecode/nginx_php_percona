FROM docker:19

RUN \
  rm -rf /var/spool/cron/crontabs \
  && rm -rf /var/log/cron.log \
  && mkdir -m 0644 -p /var/spool/cron/crontabs \
  && mkfifo -m 666 /var/log/cron.log \
  && mkfifo -m 666 /var/log/crond.log

COPY /docker-start.sh /

CMD ["/docker-start.sh"]

FROM alpine:3.20
RUN apk add --no-cache socat coreutils
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
CMD ["/entrypoint.sh"]

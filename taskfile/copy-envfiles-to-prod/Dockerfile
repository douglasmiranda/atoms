FROM alpine:3
RUN apk add --no-cache openssh rsync && ssh-keygen -A

RUN mkdir -p /username/project-name/envfiles/prod

ENV USERNAME="root"
ENV PASSWORD="root"

ENTRYPOINT ["sh", "-c"]
CMD ["echo ${USERNAME}:${PASSWORD} | chpasswd && /usr/sbin/sshd -D -o PermitRootLogin=yes -o AddressFamily=inet -o GatewayPorts=yes -o AllowAgentForwarding=yes -o AllowTcpForwarding=yes -o KexAlgorithms=+diffie-hellman-group1-sha1 -o HostkeyAlgorithms=+ssh-rsa"]
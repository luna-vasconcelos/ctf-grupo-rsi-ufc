FROM debian:bookworm-slim

RUN apt-get update && apt-get install -y --no-install-recommends openssh-server pwgen \
 && rm -rf /var/lib/apt/lists/* \
 && mkdir -p /var/run/sshd

RUN useradd -m -s /bin/bash ctf \
 && echo "ctf:ctf" | chpasswd

# hint
RUN echo "welcome to the ssh side." > /home/ctf/README.txt \
 && chown ctf:ctf /home/ctf/README.txt

RUN sed -ri 's/^#?PasswordAuthentication .*/PasswordAuthentication yes/' /etc/ssh/sshd_config \
 && sed -ri 's/^#?PermitRootLogin .*/PermitRootLogin no/' /etc/ssh/sshd_config

EXPOSE 22
CMD ["/usr/sbin/sshd","-D","-e"]

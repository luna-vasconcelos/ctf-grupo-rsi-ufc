FROM debian:bookworm-slim

WORKDIR /rev

RUN apt-get update && apt-get install -y --no-install-recommends openssh-server pwgen \
&& rm -rf /var/lib/apt/lists/* \
&& mkdir -p /var/run/sshd 

RUN useradd -m -s /bin/bash ctf \
&& echo "ctf:ctf" | chpasswd

RUN mkdir -p /home/ctf/Documents 
RUN mkdir -p /home/ctf/Downloads 
RUN mkdir -p /home/ctf/Music 
RUN mkdir -p /home/ctf/Pictures  
RUN mkdir -p /home/ctf/Videos 
# Copiando arquivos
COPY --chown=ctf:ctf home_template_ctf/Documents/normal_file.elf /home/ctf/Documents/
COPY --chown=ctf:ctf home_template_ctf/Downloads/formula_hamburguer_de_siri.zip /home/ctf/Downloads/
COPY --chown=ctf:ctf home_template_ctf/Music/best_music_ever.mp3 /home/ctf/Music/
COPY --chown=ctf:ctf home_template_ctf/Pictures/crush_secreto.jpg /home/ctf/Pictures/
COPY --chown=ctf:ctf home_template_ctf/Pictures/the_mage.jpeg /home/ctf/Pictures
# hint
RUN echo "welcome to the ssh side. " > /home/ctf/README.txt \
&& chown ctf:ctf /home/ctf/README.txt 

RUN echo "I love Compressed files and Bootloaders. UPXXXXXXXXXX <333333333 " > /home/ctf/Documents/me.txt 

RUN sed -ri 's/^#?PasswordAuthentication .*/PasswordAuthentication yes/' /etc/ssh/sshd_config \
&& sed -ri 's/^#?PermitRootLogin .*/PermitRootLogin no/' /etc/ssh/sshd_config

EXPOSE 22
CMD ["/usr/sbin/sshd","-D","-e"]

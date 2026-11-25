FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update \
    && apt-get install -y --no-install-recommends openssh-server sudo python3 \
    && rm -rf /var/lib/apt/lists/* \
    && useradd --create-home --shell /bin/bash ansible \
    && echo 'ansible:ansible' | chpasswd \
    && usermod -aG sudo ansible \
    && printf 'ansible ALL=(ALL) NOPASSWD:ALL\n' > /etc/sudoers.d/ansible \
    && chmod 0440 /etc/sudoers.d/ansible \
    && printf 'PasswordAuthentication yes\nPermitRootLogin no\n' > /etc/ssh/sshd_config.d/ansible.conf \
    && mkdir -p /run/sshd

EXPOSE 22

CMD ["sh", "-c", "ssh-keygen -A && exec /usr/sbin/sshd -D -e"]

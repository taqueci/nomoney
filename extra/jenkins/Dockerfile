FROM jenkins/jenkins:lts

USER root

RUN apt-get update && \
  apt-get install -y --no-install-recommends python3 && \
  curl -fsSL https://get.docker.com | sh && \
  apt-get clean && rm -rf /var/lib/apt/lists/*

USER jenkins

COPY --chown=jenkins:jenkins ref /usr/share/jenkins/ref

# For copying the latest files to JENKINS_HOME.
RUN find /usr/share/jenkins/ref -type f -exec cp -p {} {}.override \;

RUN jenkins-plugin-cli -f /usr/share/jenkins/ref/plugins.txt

COPY --chown=jenkins:jenkins Jenkinsfile /usr/share/jenkins/ref/

LABEL \
  org.opencontainers.image.authors="Takeshi Nakamura" \
  org.opencontainers.image.url="https://github.com/taqueci/nomoney" \
  org.opencontainers.image.title="NoMoney" \
  org.opencontainers.image.description="Jenkins for NoMoney" \
  org.opencontainers.image.version="0.0.0" \
  org.opencontainers.image.source="https://github.com/taqueci/nomoney.git"

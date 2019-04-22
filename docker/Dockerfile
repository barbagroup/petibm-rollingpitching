# Dockerfile for 3D rolling and pitching plate with PetIBM.

FROM barbagroup/petibm:0.4-GPU-OpenMPI-ubuntu
MAINTAINER Olivier Mesnard <mesnardo@gwu.edu>

# Install basic requirements.
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        git \
        wget && \
    rm -rf /var/lib/apt/lists/*

# Install PetIBM app: petibm-rollingpitching.
RUN srcdir="/opt/petibm-rollingpitching" && \
    url=https://github.com/mesnardo/petibm-rollingpitching.git && \
    git clone --recursive ${url} ${srcdir} && \
    builddir="${srcdir}/build" && \
    mkdir -p ${builddir} && \
    cd ${builddir} && \
    cmake ${srcdir} && \
    make all && \
    make install

RUN useradd -ms /bin/bash petibm-user
USER petibm-user
WORKDIR /home/petibm-user
RUN mkdir /home/petibm-user/data

EXPOSE 23
CMD ["/usr/sbin/sshd", "-D", "-p", "23"]
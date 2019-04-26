# Dockerfile for 3D rolling and pitching plate with PetIBM.

FROM barbagroup/petibm:0.4-GPU-OpenMPI-ubuntu
MAINTAINER Olivier Mesnard <mesnardo@gwu.edu>

# Install basic requirements.
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        vim \
        git \
        wget && \
    rm -rf /var/lib/apt/lists/*

# Install PetIBM app: petibm-rollingpitching.
RUN SRCDIR=/opt/petibm-rollingpitching && \
    URL=https://github.com/mesnardo/petibm-rollingpitching.git && \
    git clone --recursive ${URL} ${SRCDIR} && \
    BUILDDIR=${SRCDIR}/build && \
    mkdir -p ${BUILDDIR} && \
    cd ${BUILDDIR} && \
    cmake ${SRCDIR} && \
    make all && \
    make install

# Install Miniconda3-4.5.12.
RUN VERSION=4.5.12 && \
    FILENAME=Miniconda3-${VERSION}-Linux-x86_64.sh && \
    URL=https://repo.anaconda.com/miniconda/${FILENAME} && \
    wget ${URL} -P /tmp && \
    bash /tmp/${FILENAME} -b -p /opt/miniconda3 && \
    echo "source /opt/miniconda3/etc/profile.d/conda.sh" >> /root/.bashrc && \
    echo "conda activate py36-cloud" >> /root/.bashrc && \
    rm -f /tmp/${FILENAME}

# Install petibmpy
ARG PETIBMPY_SHA=0f921da
RUN . /opt/miniconda3/bin/activate && \
    SRCDIR=/opt/petibmpy && \
    URL=https://github.com/mesnardo/petibmpy && \
    git clone ${URL} ${SRCDIR} && \
    cd ${SRCDIR} && \
    conda env create --name=py36 --file=environment.yaml && \
    conda activate py36 && \
    python setup.py install && \
    conda deactivate

RUN useradd -ms /bin/bash petibm-user
USER petibm-user
WORKDIR /home/petibm-user
RUN mkdir /home/petibm-user/data

EXPOSE 23
CMD ["/usr/sbin/sshd", "-D", "-p", "23"]
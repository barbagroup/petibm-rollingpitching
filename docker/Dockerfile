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
ADD https://api.github.com/repos/mesnardo/petibmpy/git/refs/heads/master version.json
RUN . /opt/miniconda3/bin/activate && \
    SRCDIR=/opt/petibmpy && \
    URL=https://github.com/mesnardo/petibmpy && \
    git clone ${URL} ${SRCDIR} && \
    cd ${SRCDIR} && \
    conda env create --name=py36 --file=environment.yaml && \
    conda activate py36 && \
    python setup.py install && \
    conda deactivate

# Install PetIBM app: petibm-rollingpitching.
ADD https://api.github.com/repos/mesnardo/petibm-rollingpitching/git/refs/heads/master version.json
RUN SRCDIR=/opt/petibm-rollingpitching && \
    URL=https://github.com/mesnardo/petibm-rollingpitching.git && \
    git clone --recursive ${URL} ${SRCDIR} && \
    BUILDDIR=${SRCDIR}/build && \
    mkdir -p ${BUILDDIR} && \
    cd ${BUILDDIR} && \
    cmake ${SRCDIR} \
        -DCMAKE_INSTALL_PREFIX=/usr/local \
        -DCMAKE_C_COMPILER=mpicc \
        -DCMAKE_CXX_COMPILER=mpicxx \
        -DPETSC_DIR=${PETSC_DIR} \
        -DPETSC_ARCH=${PETSC_ARCH} \
        -DCMAKE_INSTALL_RPATH_USE_LINK_PATH=ON \
        -DCMAKE_BUILD_TYPE=RELEASE && \
    make all && \
    make install

RUN useradd -ms /bin/bash petibm-user
USER petibm-user
WORKDIR /home/petibm-user
RUN mkdir /home/petibm-user/data

EXPOSE 23
CMD ["/usr/sbin/sshd", "-D", "-p", "23"]

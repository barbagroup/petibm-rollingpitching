# Running simulations on AWS

1. Sign-in to your AWS account
2. Go to EC2, switch to your preferred Region, and click "Launch instance"
3. Choose one the Ubuntu 18.04 AMI
4. Choose the `p2.8xlarge` instance type (8 NVIDIA K80 GPUs, 32 vCPUs, 488 GiB Mem, 96 GiB GPU Mem). (`p2.xlarge` does not have enough memory for the base case simulation.)
5. Use a Bootstrap script to install and start Docker on the instance:

   ```bash
   #!/bin/bash
   sudo snap install docker
   sudo addgroup --system docker
   sudo adduser ubuntu docker
   newgrp docker
   sudo snap disable docker
   sudo snap enable docker
   ```

6. Request 100 GB for the Root volume (gp2 volume type is fine)
7. Use a Security Group with SSH to your IP address
8. Review, set your Permission Key-Pair, and Launch
9. Once the instance is provisioned, connect to it

   ```shell
   ssh -i <pem-path> ubuntu@<public-ipv4-dns-or-address>
   ```

10. On the EC2 instance, install dependencies for Singularity

    ```shell
    sudo apt update
    sudo apt install -y build-essential libssl-dev uuid-dev libgpgme11-dev libseccomp-dev wget pkg-config git
    ```

11. Install CUDA Toolkit 10.1

    ```shell
    wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu1804/x86_64/cuda-ubuntu1804.pin
    sudo mv cuda-ubuntu1804.pin /etc/apt/preferences.d/cuda-repository-pin-600
    sudo apt-key adv --fetch-keys https://developer.download.nvidia.com/compute/cuda/repos/ubuntu1804/x86_64/7fa2af80.pub
    sudo add-apt-repository "deb https://developer.download.nvidia.com/compute/cuda/repos/ubuntu1804/x86_64/ /"
    sudo apt update
    sudo apt -y install cuda-10-1
    ```

12. Install GO (required for Singularity)

    ```shell
    export VERSION=1.14.12 OS=linux ARCH=amd64
    wget https://dl.google.com/go/go$VERSION.$OS-$ARCH.tar.gz
    sudo tar -C /usr/local -xzvf go$VERSION.$OS-$ARCH.tar.gz
    rm -f go$VERSION.$OS-$ARCH.tar.gz
    export PATH=/usr/local/go/bin:$PATH
    ```

13. Install Singularity

    ```shell
    export VERSION=3.8.0
    wget https://github.com/hpcng/singularity/releases/download/v${VERSION}/singularity-${VERSION}.tar.gz
    tar -xzf singularity-${VERSION}.tar.gz
    rm -f singularity-${VERSION}.tar.gz
    cd singularity-${VERSION}
    ./mconfig -V ${VERSION}
    make -C builddir
    sudo make -C builddir install
    ```

14. Install nvidia-container-cli

    ```shell
    DIST=$(. /etc/os-release; echo $ID$VERSION_ID)
    curl -s -L https://nvidia.github.io/libnvidia-container/gpgkey | sudo apt-key add -
    curl -s -L https://nvidia.github.io/libnvidia-container/${DIST}/libnvidia-container.list | sudo tee /etc/apt/sources.list.d/libnvidia-container.list
    sudo apt update
    sudo apt install libnvidia-container-tools
    ```

15. Download the Zenodo archive with container images

    ```shell
    ARCHIVE=petibm-rollingpitching-images.zip
    curl --output $ARCHIVE https://zenodo.org/record/5090342/files/$ARCHIVE
    unzip $ARCHIVE
    rm -f $ARCHIVE
    ```

16. Load the pre-processing Docker image

    ```shell
    docker load -i petibm-rollingpitching-images/petibm-rollingpitching_prepost.tar
    ```

17. Download the Zenodo archive with the application input data

    ```shell
    ARCHIVE=petibm-rollingpitching-2021.05.02.zip
    curl --output $ARCHIVE https://zenodo.org/record/4733323/files/$ARCHIVE
    unzip $ARCHIVE
    rm -f $ARCHIVE
    ```

18. Run the base case simulation

    ```shell
    cd petibm-rollingpitching-2021.05.02/runs/Re200_St0.6_AR1.27_psi90
    docker run --rm -v $(pwd):/volume mesnardo/petibm-rollingpitching:prepost python /volume/scripts/create_body.py
    SINGULARITY_CUDA_VISIBLE_DEVICES=0,1,2,3 singularity exec --nv ~/petibm-rollingpitching-images/petibm-rollingpitching_petibm0.5.1-xenial.sif mpirun --use-hwthread-cpus petibm-rollingpitching -probes probes.yaml -options_left -log_view ascii:view.log
    ```

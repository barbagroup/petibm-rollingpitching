# Repro-Packs on AWS

1. Sign-in to your AWS account
2. Go to EC2, switch to your preferred Region, and click "Launch instance"
3. Choose one of the Ubuntu AMIs (e.g., "Ubuntu Server 20.04 LTS (HVM), SSD Volume Type")
4. Choose the `t3.2xlarge` instance type (or a similar one with 32 GB of memory)
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

6. Request 60 GB for the Root volume (gp2 volume type is fine)
7. Use a Security Group with SSH to your IP address
8. Review, set your Permission Key-Pair, and Launch
9. Once the instance is provisioned, connect to it

   ```shell
   ssh -i <pem-path> ubuntu@<public-ipv4-dns-or-address>
   ```

10. Install `unzip`

    ```shell
    sudo apt install unzip
    ```

11. Download the repro-packs from Zenodo and unzip the archive

    ```shell
    ARCHIVE=petibm-rollingpitching_repro-packs.zip
    curl --output $ARCHIVE https://zenodo.org/record/4732946/files/$ARCHIVE
    unzip $ARCHIVE
    rm -f $ARCHIVE
    ```

12. Download the container images from Zenodo and unzip the archive

    ```shell
    ARCHIVE=petibm-rollingpitching-images.zip
    curl --output $ARCHIVE https://zenodo.org/record/5090342/files/$ARCHIVE
    unzip $ARCHIVE
    rm -f $ARCHIVE
    ```

13. Load the Docker image for post-processing the data

    ```shell
    docker load -i petibm-rollingpitching-images/petibm-rollingpitching_prepost.tar
    ```

14. Run a Docker container to generate the secondary data and figures

    ```shell
    cd repro-packs
    docker run --rm -it -v $(pwd):/postprocessing mesnardo/petibm-rollingpitching:prepost /bin/bash /postprocessing/scripts/generate_all_figures.sh > repro-packs.log 2>&1
    ```

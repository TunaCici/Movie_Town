Author: Tuna Cici
Email: tunacici7@gmail.com

Welcome to my Web Applicaton using Flask, Redis, MongoDB, RabbitMQ and ElasticSearch.

This text document will guide you through the installation process.

Requirements
-------------------------------------------------------
OS: Ubuntu 20.04 or Kali-Linux. (or any linux distros)
Python: 3.9.7
Virtual Enviroment: Anaconda3 or Miniconda3
Docker: 20.10.8
--------------------------------------------------------

Quick notes before starting this tutorial
--------------------------------------------------------------------------------
1. I am going to assume you are already installed Ubuntu 20.04 onto your system.
2. You will need at least a decent modern CPU and 4GBs of RAM.
3. The program might be unstable because it depends on many different services.
4. Because of the architecture you need two apps running.
5. First app is the main flask app and the other is the worker.
6. You can open up as many worker as you want.
7. If an apps fails just restart it.
8. Feel free to contact me if anything goes wrong.
--------------------------------------------------------------------------------

Prerequisites
---------------------------------------------------------------------------
STEP 1 - Installing conda to your system.
    i. Go to Anaconda3's official website and download Miniconda 3 for Linux 64 bit
        Website: https://conda.io/miniconda.html
    ii. Open the downloadad file with bash
        sudo bash ./Miniconda3-latest-Linux-x86_64.sh
    iii. Follow the instructions to install Miniconda3.
        Once asked for the installation path, type /home/miniconda3
    iv. Add conda to your path.
        Type export PATH=/home/miniconda3/bin:$PATH onto your terminal
        Type conda init onto your terminal
    v. Restart your terminal and done. Conda is now installed.
STEP 2 - Installing docker to your system.
    i. Type these commands to add docker-se to your apt repository.
        sudo apt update
        sudo apt install apt-transport-https ca-certificates curl software-properties-common
        curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
        sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu focal stable"
        apt-cache policy docker-ce
    ii. Install the Docker.
        sudo apt install docker-ce
    iii. Test the installation.
        docker --version
    iv. Docker is now installed.
STEP 3 - Installing docker-compose to your system.
    i. Type these commands to install docker-compose
        sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
        sudo chmod +x /usr/local/bin/docker-compose
    ii. Test the installion.
        docker-compose --version
    iii. Docker-compose is now installed.
STEP 4 - Retrieve the project files from either the github or the DVD.
    i. Type the following command to retrieve the project files.
        git clone https://github.com/TunaCici/movie_town
STEP 5 - Download the necessary python libraries.
    i. Navigate to the project folder and type the following.
        pip install -r requirements.txt
    ii. Wait for the operation to end.
    iii. Required python libraries are now installed.
STEP 6 - Initialize the docker containers
    i. Navigate to the project folder and type the following.
        docker-compose up -d
    ii. Wait for the operation to end.
    iii. Docker containers for the MongoDB, ElasticSearch, Redis and Rabbitmq is installed.
STEP 7 - Initialize the databases.
    i. Navigate to the project folder and type the following.
        python init_db.py
    ii. This step might take a while depending on your system.
    iii. Now all of the movies are now loaded into your database.
STEP 8 - (Optional) Download the movie posters.
    i. This step is not necessary but will make the website a whole lot better.
    ii. Run the following command to download all the posters from the TMDB.
        python utils/imdb_helper.py
    iii. This step might take hours depending on your network and the TMDB API.
    iv. Move the folder "posters" from "data/posters" to "static/data/posters"
    v. Now all the movies will have it's own poster.
---------------------------------------------------------------------------

Usage
-------------------------------------------------------------
STEP 1 - Start the main Flask app.
    i. Navigate to the projet folder and type the following.
        python main.py
    ii. Now the webserver is running.
        localhost:5000
STEP 2 - Start the worker(s) for website to function.
    i. Navigate to the project folder and type the following.
        python worker.py
    ii. Now the worker is running and waiting for requests.
STEP 3 - Now just enjoy the Movie Town.
    i. Everything is ready, you can now sign-up, login or search through amazing movies.
        <3
-------------------------------------------------------------
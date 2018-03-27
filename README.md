# SG Travel Planner
Social Analytics Project

# Requirements

Requires Python 3.x

# Installation

Run `pip install -r requirements.txt` to install all necessary dependencies.

# Crawler

* Create a file called `.env` in the project root directory based on the `sample.env` provided
* Run the following commands:
    1. `$ set -a`
    2. `$ source .env`
    3. `$ python -m crawler.runner`

# Web UI

To run the UI, you will need to first install [Docker](https://docs.docker.com/install/) and [Docker Compose](https://docs.docker.com/compose/install/). Choose the appropriate installation for your OS.

Once you have done that and have verified the installations, follow these steps in your Terminal/Command Prompt:

* Ensure docker is up by running `docker -v`
* `cd travel_planner`
* `docker-compose up --build` and wait for everything to load, the first time will take some time to load up
* Once everything is up and running, open up your browser and visit [http://locahost/](http://locahost/)

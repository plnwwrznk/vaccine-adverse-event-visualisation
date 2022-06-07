# Vaccine adverse event visualisation

## General info
This is a dash app written as a project for the classes at the Adam Mickiewicz University.

It is using data from: https://vaers.hhs.gov/ to visualize adverse evens after vaccination


## Setup
How to run the app? Run in terminal:

    python ./index.py
and visit http://127.0.0.1:8050/ in your web browser.


#### Building and running basic app with docker:
Run in terminal:

    docker build -t uam-dash .
    docker run --rm -p 8000:8000 --name szczepionki uam-dash

To see the app open:
- on linux:  http://0.0.0.0:8000 
- on windows:   http://127.0.0.1:8000 

## Autors
* Paulina Wawrzyniak
* Anna Przybułek
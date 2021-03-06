# Influenza Estimator Web Tool

## Running directly from docker container

To run this file directly from the docker container do the following steps:

### Install Docker engine

You will find instructions to install docker engine on your system [here.](https://docs.docker.com/engine/install/ubuntu/#install-using-the-repository)

### Pulling and running the docker image

```commandline
docker pull tejsukhatme/influenza_estimator:random_forest
docker run -it -p 5000:5000 tejsukhatme/influenza_estimator:random_forest
```


## To compile manually and run, open a terminal and follow the following commands:

cd into the folder of choice and enter:
```commandline
git pull https://github.com/Hephaestus12/applications.git
cd applications/gsoc_application_projects/2020/influenza/web/
```

### Prepare the Environment

Make sure your have a python environment with Python 3.5
You will have to manually compile and install Shogun from source into that environment. Only then will you be able to run the webapp.

You can find the instructions for doing that [here](http://blog.detoni.me/2018/10/08/Compile-Shogun-with-Conda/).

### Installing packages

You have to install the following packages into your python environment.
```commandline
pip install -r requirements.txt
```

### Running the application
```commandline
export FLASK_APP=influenza_estimator
export FLASK_ENV=development
flask run
```

Your flask application should be successfully running once this is done.



# Influenza API Guide

#### GET the Live influenza ESTIMATE numbers as a JSON file for all countries.
Send a GET request to the following Endpoint:
```
/api/v1.0/all/current/
```


#### GET older influenza ESTIMATE numbers as a JSON file for all countries.
Send a GET request to the following Endpoint:
```
/api/v1.0/all/weekly/estimate/<int:year>/<int:week>/
```


#### GET older influenza INCIDENCE numbers as a JSON file for all countries.
Send a GET request to the following Endpoint:
```
/api/v1.0/all/weekly/incidence/<int:year>/<int:week>/
```


#### GET the Live influenza ESTIMATE number as a JSON file for one country.
Send a GET request to the following Endpoint:
```
/api/v1.0/specific/current/<string:country>
```


#### GET the older influenza ESTIMATE number as a JSON file for one country..
Send a GET request to the following Endpoint:
```
/api/v1.0/specific/weekly/estimate/<int:year>/<int:week>/<string:country>
```


#### GET the older influenza INCIDENCE number as a JSON file for one country.
Send a GET request to the following Endpoint:
```
/api/v1.0/specific/weekly/incidence/<int:year>/<int:week>/<string:country>
```

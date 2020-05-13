# AWS ECR Releases

## Getting started
Run the application with python command.
```bash
python3 main.py
```

## Pré-requis
Prerequisites packages for application runtime:
* python >= 3.5
* pip == 3
* gettext

Instll system dependencies (based the reference ime in the Dockerfile):
```bash
yum install -y gettext python3 python3-pip
```

Install python dependencies:
```bash
pip3 install -r requirements.txt
```

## Environment variables
The application takes parameters set into the file `.env`. This file is filled at the container lunching.

Variables list:
* `FLASK_ENV`: Environnement de l'application Flask
* `AWS_ACCESS_KEY_ID`: Access Key ID of the AWS IAM account
* `AWS_SECRET_ACCESS_KEY`: Access Key Secret of the AWS IAM account
* `AWS_REGION_NAME`: AWS region where is the AWS ECR
* `RELEASES_MAX`: Maximum of retrieved elements
* `DEBUG_MODE`: Enable the falsk debug mode

## List of accessible routes:
* [GET] /
* [GET] /<namespaceName>
    * [GET] /germainlefebvre4
* [GET] /<namespaceName>/<imageName>
    * [GET] /germainlefebvre4/hello-world

## Reponse example
The following examples are served by localhost application.

* http://localhost:8080/
```json
{
  "msg": "Please select an authorized registry namespace.",
  "registries": [
    "germainlefebvre4"
  ]
}
```


* http://localhost:8080/germainlefebvre4
```json
{
  "images": [
    "hello-world"
  ], 
  "msg": "Please select a image name into the namespace name."
}
```

* http://localhost:8080/germainlefebvre4/hello-world
```json
{
  "name": "hello-world",
  "releases": [
    "1.0.0",
    "1.0.1"
  ]
}
```

* http://localhost:8080/germainlefebvre4/toto
```json
{
  "images": [
    "hello-world"
  ], 
  "msg": "Please provide a authorized image name."
}
```

## Development environment
### Install dependencies
System dependencies
```bash
ap update
apt install -y python3 python3-pip
pip3 install pipenv
```

Python dependencies
```bash
pipenv update
```

### Run the application
```bash
pipenv run python main.py
```
Application is reachable at the address `http://localhost:8080`


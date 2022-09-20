# Machine_Learning_Project
This repository is created for practice purpose to learn end to end Machine Learning Project 

## Accounts:

1. [Github](https://github.com/sagark721)
2. [Heroku](https://dashboard.heroku.com/account)

## Create Conda Environment:

```
conda create -p venv_test python==3.7 -y
```
> Note: -p is used so that the environment will be created in project folder. otherwise -n is used which would create folder in 'C' drive.




### Activate conda environment:
```
conda activate venv_test/
```


### Create requirements.txt file and install requirements using:
```
pip install -r requirements.txt
```

## Git Commands:
1. To add specific files into git:
```
    git add <file name 1> <file name 2>
```

2. To add all the file in the directory to git:
```
    git add .
```
> Note: if dont want to add some files, add their name in .gitignore file

3. If file is created and not added by git, following command will give the status /warning of files which were not added/tracked by git

```
    git status
```

4. To create a new version:
```
    git commit -m <"Message" (why are you creating this version)>
```

5. To check all versions maintained by git:
```
    git log
```

6. To send the version/changes to github:
```
git push origin main
```
> Note: here 'origin' is the variable,in which the remote url is stored (url which we copied during cloning)

7. To check the remote url:
```
git remote -v
```

8. To check branch:
```
git branch 
```

## Heroku Setup

- To setup CI/CD pipeline in heroku we need 3 informations from Heroku:

    1. HEROKU_EMAIL 
    = sagark14121@gmail.comx
    2. HEROKU_API_KEY 
    = (Heroku dashboard -> Profile -> Account Setting -> (Scroll down) -> API Key) [e.g : a9569e3c-7313-4e7f-af73-6967633b9e8b]
    3. HEROKU_APP_NAME
    = App name from Heroku Dashboard [eg: checkreviews]


## Docker File


Create new docker file in vs code, type `Dockerfile` and hit enter.
- Code written in docker file:
```
    FROM python:3.7
    COPY . /app
    WORKDIR /app
    RUN pip install -r requirements.txt 
    EXPOSE $PORT
    CMD gunicorn --workers=4 --bind 0.0.0.0:$PORT app:app
```
> Note: Create `.dockerignore` file and the file names in it, To ignore the file which are not supposed to be added when creating Dockerfile.

### DockerFile Code Description/Instructions:
- Use `python 3.7` based operating system
- Copy all the code inside `app` folder
- Set working directory to `app`
- Install `requirements.txt` file
- Expose the port number, that will be sent from the environment variable
- `CMD gunicorn --workers=4 --bind 0.0.0.0:$PORT app:app` , to run the application

    

    - #### With the help of `gunicorn` we will launch the application on ip address 0.0.0.0 which is local host ip address. gunicorn is built for linux based system, base image in Docker is Ubuntu based system so we need gunicorn there. gunicorn is webserver gateway interface, whenever user is trying to access url `gunicorn` will accept that user's request and map that request with the logic written in `app.py` file and return that response back to the client , inshort gunicorn helps to run our application.

    - #### `--workers=4` means if there are 1000 requests each worker will handle 250 request (in order to increase efficency). (with paid subscription number of workers can be increased)

    - #### `--bind 0.0.0.0` is the local ip address of machine

    - #### PORT is the environment variable, whose value will be provided by the HEROKU (Environment varibale is the variable whose values is set by operating system)

    
    - #### app:app means,  in `app.py` file (flask application),`app` object. i.e file_name(Module name):object_name


### BUILD DOCKER IMAGE
docker build -t <image_name>:<tag_name> <location of the docker file> . is used for location as the dockerfile is located in the present directory.
```
docker bulid -t <image_name>:<tag_name> .
```
> Note: image_name must be in lowercase only

To list Docker images:
```
docker images
```

To run Docker image:
```
docker run -p 5000:5000 -e PORT=5000 <image id>
```

To check running containers in docker:
```
docker ps
```

To stop docker container:
```
docker stop <container_id>
```

## Deployment on Heroku

1. create a folder `.github`
2. within .github folder create one more folder `workflows`
3. in workflows folder create a file `main.yaml` (in this file there will be the github actions)

## Setting Github Secrets:

1. Open `main.yaml` file on github.
2. duplicate the tab
3. on second (duplicated) tab  -> Settings -> Secrets (on left side) -> Actions -> New Repository Secrets
4. add values of  HEROKU_EMAIL, HEROKU_API_KEY & HEROKU_APP_NAME as a secrets


## Create a `setup.py` file

## Create a folder named, `housing`.
- create `__init__.py` file in housing folder. `__init__.py` file will tell that housing folder is the python module/package so that this `housing` folder can be imported from any other file.
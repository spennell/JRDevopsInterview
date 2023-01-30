# Instructions

This repo is intended to act as a technical interview. Please make sure you follow the instructions and meet the listed requirements. Do not hesitate to ask questions if you are having trouble. You are also free to use Google, or any other web resources you may have. The idea of this technical exercise is to determine the assignee's troubleshooting skills. 

## Requirements:

Please have access to the following requirements. Docker resources can be provided if you do not have the ability to run docker locally.

* A Python compatible IDE - VS Code or Pycharm will function and are free. You amy also use any other IDE you wish.

* Docker/Docker Desktop - A local instance of docker or a remote instance

* Docker Compose

**Links**

[Get Docker | Docker Documentation](https://docs.docker.com/get-docker/)

[Compose | Docker Documentation](https://docs.docker.com/compose/)

[Get Started Tutorial for Python in Visual Studio Code](https://code.visualstudio.com/docs/python/python-tutorial)

[Download Visual Studio Code ](https://code.visualstudio.com/Download)

[Download PyCharm](https://www.jetbrains.com/pycharm/download/)

## Problem

Take the following application and convert it to a dockerized application. The end result should be written in a compose file.



##### Local App Requirements

If you want to run the app locally for testing as part of troubleshooting as outlined below or would like to run the app locally make sure you have a local copy of redis running and update the **.env** accordingly.



Create a **.env** file in the **app** directory. You may copy **.env.docker** or use the following template.

```ini
REDIS_HOST = "redis"
REDIS_DB = 0
REDIS_PORT = 6379
REDIS_QUEUE = "QUEUE1"
```



### Containers

Create the following containers based on the provided source code. **Bonus if done using multi-stage builds**. Reference the bin/build.sh script for a hint.

**Recommendations:** A solution that has been tested uses the `python:3.10.9-slim-bullseye` docker image. 

1. Application container that runs the FastAPI app.
   
   1. Configure the container to listen on port 80
   
   2. App requirements are listed in requirements.txt
   
   3. Working directory should be **/app** and source should be included in **/app/api**
   
   4. ```ini
      CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
      ```

2. Worker Container
   
   1. Should contain the project code and requires access to **rq_worker.py**
   
   2. Does not require any ports to be open
   
   3. Working Directory should be **/app**
   
   4. ```ini
      CMD ["rq", "worker", "-c", "rq_worker"]
      ```

3. Scheduler Container
   
   1. Does not need project code, requires dependencies defined in the **requirements.txt** file
   
   2. Set the following ENV variables
      
      ```ini
      RQ_REDIS_HOST="127.0.0.1"
      RQ_REDIS_PORT=6379
      RQ_REDIS_DB=0
      ```
   
   3. ```ini
      CMD ["rqscheduler"]
      ```

4. Redis Container - this can be left as default.

### Compose

Create a docker compose file to manage the app. You can use the following template to expand upon.

```yaml
version: '3'

services:
  redis:
    image: redis

  app:
    image: app

  worker:
    image: worker

  scheduler:
    image: scheduler
```

The worker and scheduler containers depend on the redis container to function. Once completed, attempt to run the application with docker-compose

### Validation

To test the application is working you should be bale to browse to http://localhost/docs

If you get a response the app is working. You are free to attempt to run the workers/status api endpoint



### Bonus

Create an additional container to leverage nginx as a reverse proxy.




### Troubleshooting

The bin directory contains a **workers.py** utility  that you can pass --help to for command output. If you have a local running version of redis you can use this to fire up local version of required worker services to validate the locally running application works.

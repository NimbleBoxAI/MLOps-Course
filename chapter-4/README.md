# Packaging

## Why Packaging?

Application needs to be deployed in different machines (VM’s, other laptops etc) which don’t have the necessary dependencies and it might be running on different configuration(OS, CPU’s, etc). 
To run the applications in different machines, it has to have same environment as it was running on the host side. 
Installing dependencies, configuring things for each machine is difficult and not scalable. 
The way to tackle this problem is `packaging`, also commonly known as `containerisation`

## Machine Learning Model

Before going into the techincal part, let's take a look into machine learning model. 

Here we are exploring `Question-Answering` in NLP.

Question Answering models can retrieve the answer to a question from a given context.

![](../images/chapter-4/qa.png)

Here question is passed along with the context to the model. Model encodes the data and predicts the start and end index of the answer in the context. The data present in the start_idx and end_idx is taken from the context and is outputted as answer.

Refer to `model.py` file for related code.

## Setup

Create a virutal enviornment using conda as below
```
conda create --name mlops python=3.8
conda activate mlops
```

Install the requirements needed
```
pip install -r requirements.txt
```

## Running

```python
python model.py
```

# Docker

Docker is a container management tool, which packages the application code, configuration, and dependencies into a portable image that can be shared and run on any platform or system.

There are three main things in docker:

- `DockerFile`: contains the list of commands to run which are necessary for the application to run (like dependencies, codes, command to run etc.)

- `Docker Image`: is a lightweight, standalone, executable package of software (built using dockerfile) that includes everything needed to run an application: code, runtime, system tools, system libraries, and settings.

- `Docker Container`: is an instance of Docker Image which contains the running application.

![arch](../images/chapter-4/docker_arch.png)

Let's see how to create each one of them.

## DockerFile

A simple file that consists of instructions to build a Docker Image. Each instruction in a docker file is a command/operation, for example, what operating system to use, what dependencies to install or how to compile the code, and many such instructions which act as a layer.

Let's see how to create a docker file for our application.

Create a file called `Dockerfile` and copy/paste the below content.
```dockerfile
FROM python:3.8
COPY ./ /app
WORKDIR /app
RUN pip install -r requirements.txt
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
CMD ["python3", "model.py"]
```

- `FROM:` creates a layer from the base image, here we have used python:3.8 as base image. This is pulled from Docker Hub. 

- `COPY:` Here the current directory files are copied to the container’s app directory. This will be added as a separate layer while building the image and is cached.

- `WORKDIR:` specifies the working directory in the container.

- `RUN:` specifies what commands to run within the container, here running pip command to install dependencies from requirements.txt file which is needed to run the application.

- `ENV`: specifies what enviornment variables to set inside docker container. Here LC_ALL, LANG are set to UTF-8.

- `CMD:` specifies what command to run at the start of the container.

## Docker Image

Docker image is a file comprised of multiple layers which can execute applications in a single instance. It includes all dependencies, configuration, scripts, binaries, etc. necessary for running an application. The image also contains other configuration for the container, such as environment variables, a default command to run, and other metadata.

Here instructions are provided in dockerfile. Let's create docker image using dockerfile. Run the following command:

```
docker build -t qa:test .
```

The above command builds the docker image using Dockerfile and assigns a tag to the created image `qa:test`

Check the list of all available docker images using the command:

```
docker images
```

If the dockerfile name is created with different name, then the above command might not work. In that case, we have to explicitly provide the dockerfile name as well like below

```
docker build -t qa:test -f docker_other_file .
```

The `.` in the end, provides the build context for docker. In the dockerimage, there is a command `COPY ./ /app`, here `./` maps to `.` in the docker build command. So if you want to run the docker build command from a different place, then this build context path needs to be modified accordingly.


## Docker Container

Docker Container is a runnable instance of an image. 

- Can be run on local machines, virtual machines or deployed to the cloud.

- Is portable (can be run on any OS)

- Containers are isolated from each other and run their own software, binaries, and configurations.

Let's create a docker container using the docker image builded in the previous step.

```
docker run --name qa_container qa:test
```

Here `--name` indicates the name of the container and also need to provide what docker image to use to create the container.

List all the docker containers using the command

```
docker ps -a
```

The model is downloaded while running the container. We will explore how to load from a remote location in next chapter.

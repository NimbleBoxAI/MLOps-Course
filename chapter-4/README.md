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
python src/model.py
```

This will download the model `deepset/roberta-base-squad2` from huggingface.

![](../images/chapter-4/basic_flow.png)

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
CMD ["python3", "src/model.py"]
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
docker build -t qa:test -f dockerfiles/Dockerfile .
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

![](../images/chapter-4/docker_flow.png)

The model is downloaded while running the container. We will explore how to upload & download from a remote storage (s3) instead of downloading it in docker image.

# Remote Storage

Remote storage, also known as cloud storage, is a description of storage accessed over a network (remotely). It can help in deploying large amounts of data to other servers that are located in the same remote zone.

## S3

Amazon Simple Storage Service (S3) is a storage for the internet. It is designed for large-capacity, low-cost storage provision across multiple geographical regions.


We have the model in our cache dir `TRANSFORMERS_CACHE`. The default directory where the model is downloaded is `~/.cache/huggingface/transformers/`. One simple way is to package the model in dockerimage so that it won't be downloaded everytime. But this is not a standard approach. There could be multiple models and we cannot package each and every model. Also we should not download from huggingface repo everytime. Better solution to this is to maintain all the models in a remote storage and load the model from 
there as and when needed.

For this to happen, we need to first upload the models to remote storage (S3).

![](../images/chapter-4/remote_flow.png)

## Uploading model to S3

Let's save the models in a specific folder `models`.

```
python src/save_model.py
```

This will download the model from huggingface. If the model is already downloaded it will be present in cache directory `~/.cache/huggingface/transformers/`. Then it will save the model in `models` directory.

Now we need to save this model in S3.

Data in S3 is organized in the form of buckets.

- A Bucket is a logical unit of storage in S3.

- A Bucket contains objects which contain the data and metadata.

Before adding any data in S3 the user has to create a bucket which will be used to store objects.

#### Creating bucket

- Sign in to the AWS Management Console and open the Amazon S3 console at https://console.aws.amazon.com/s3/

- Click on `Create Bucket`

- Bucket name details

- Created bucket

#### Programmatic access

Credentials are required to access any aws service. There are different ways of configuring credentials. Let's look at a simple way.

- Go to My Security Credentials

- Navigate to `Access Keys` section and click on `Create New Access Key button`.

  - This will download a csv file containing the AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY

- Set the ACCESS key and id values in environment variables.

```
export AWS_ACCESS_KEY_ID=<ACCESS KEY ID>
export AWS_SECRET_ACCESS_KEY=<ACCESS SECRET>
```

**Do not share the secrets with others**

#### Accessing s3 using CLI

Download the AWS CLI package and [install it from here](https://aws.amazon.com/cli/)

aws cli comes with a lot of commands. [Check the documentation here](https://docs.aws.amazon.com/cli/latest/index.html)


#### Push the model to s3

Navigate to the models directory where the model is downloaded and then run the following script. 

```
aws cp deepset s3://mlops-course/models/ --recursive
```

Here `deepset` is the folder name, `--recursive` option for pushing all the files in a folder.

## Downloading model from S3

Now that the model is present in s3, we need to modify the code such that the model is downloaded from s3 instead of huggingface.



## Dockerfile Update

```
FROM python:3.8
COPY ./ /app
WORKDIR /app
RUN pip install -r requirements.txt
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
ARG MODEL_DIR=./models
RUN chmod -R 0777 $MODEL_DIR
RUN python3 src/improved_model.py
```

The change from prior dockerfile is:

- `ARG MODEL_DIR=./models`: This is for saying where the models will be stored

- `RUN chmod -R 0777 $MODEL_DIR`: This is for giving permissions to the models directory. So that at run time models can be downloaded and written to this directory.

- `RUN python3 src/improved_model.py`: This will check whether the model is downloading from s3 properly or not.


### Building DockerImage

```
docker build -t qa:test -f dockerfiles/improved.Dockerfile .
```

# Conainer Registry

A container registry is a place to store docker images. Docker image is a file comprised of multiple layers which can execute applications in a single instance. Hosting all the images in one stored location allows users to commit, identify and pull images when needed.

AWS version of container registry is ECR which stands for Elastic Container Registry.

![arch](../images/chapter-4/ecr.png)

## Uploading Docker Image to ECR

- Create a repository when prompted with name `mlops-course`

Commands required to push the image to ECR can be found in the ECR itself

- Authenticating docker client to ECR

```
aws ecr get-login-password --region us-west-2 | docker login --username AWS --password-stdin 246113150184.dkr.ecr.us-west-2.amazonaws.com
```

- Tagging the image

```
docker tag qa:test 246113150184.dkr.ecr.us-west-2.amazonaws.com/mlops-course:latest
```

- Pushing the image

```
docker push 246113150184.dkr.ecr.us-west-2.amazonaws.com/mlops-course:latest
```



Now that the docker image is updated with the code and pushed to ECR, we need to create container with that image. There are different ways of doing it. We will explore deploying methods like with Kubernetes (EKS), Serverless (Lambda) in the coming chapters. We will also look into how to configure CI/CD using GitHub Actions for automating the docker image building and pushing to ECR. 

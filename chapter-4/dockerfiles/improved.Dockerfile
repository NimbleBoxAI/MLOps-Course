FROM python:3.8
COPY ./ /app
WORKDIR /app
RUN pip install -r requirements.txt
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
ARG MODEL_DIR=./models
RUN chmod -R 0777 $MODEL_DIR
RUN python3 src/improved_model.py
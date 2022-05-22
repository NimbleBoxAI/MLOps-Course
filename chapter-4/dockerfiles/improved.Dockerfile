FROM python:3.8

ARG AWS_ACCESS_KEY_ID
ARG AWS_SECRET_ACCESS_KEY
ENV AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID \
    AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY

COPY ./ /app
WORKDIR /app
RUN pip install -r requirements.txt
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
RUN mkdir models
RUN chmod -R 0777 models
CMD ["python3", "src/improved_model.py"]
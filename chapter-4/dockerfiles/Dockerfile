FROM python:3.8
COPY ./ /app
WORKDIR /app
RUN pip install -r requirements.txt
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
CMD ["python3", "src/model.py"]
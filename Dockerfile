FROM python:3.11.9
RUN mkdir /app
WORKDIR /app
COPY requirements.txt /app
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY . /app
ENV PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python
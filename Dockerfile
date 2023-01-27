FROM ubuntu:20.04

RUN apt update && apt install -y python3.8 python3-pip

RUN mkdir -p /src
WORKDIR /src

RUN useradd --create-home appuser
RUN chown -R appuser:appuser /src

COPY app /src/app
COPY requirements.txt /src

RUN pip3 install -r requirements.txt

USER appuser

CMD ["python3", "-um", "app"]

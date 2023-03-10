FROM python:3.11-alpine

RUN mkdir -p /src
WORKDIR /src

RUN addgroup -S appgroup && adduser -S appuser -G appgroup
RUN chown -R appuser:appgroup /src
USER appuser

COPY app /src/app
COPY requirements.txt /src

RUN pip3 install -r requirements.txt

CMD ["python3", "-um", "app"]

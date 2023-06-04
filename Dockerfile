FROM python:3.11-alpine

RUN addgroup -S appgroup \
 && adduser -S appuser -G appgroup \
 && mkdir -p /src \
 && chown -R appuser:appgroup /src

WORKDIR /src
# USER appuser

COPY requirements.txt /src
RUN pip3 install -r requirements.txt

COPY app /src/app

CMD ["python3", "-um", "app"]

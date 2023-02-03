# dispatcher-service

Small service that streams reddit submissions and comments
to respective endpoints

![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/flam-flam/dispatcher-service/ci.yaml?label=CI&logo=Docker&style=for-the-badge)
![GitHub tag (latest SemVer)](https://img.shields.io/github/v/tag/flam-flam/dispatcher-service?logo=Github&sort=semver&style=for-the-badge)

## Reddit credentials

Create new integration credentials at https://www.reddit.com/prefs/apps

Set the credentials in `.env` file (DO NOT COMMIT IT PLEASE).
```env
REDDIT_CLIENT_ID=<value>
REDDIT_CLIENT_SECRET=<value>
```

## Local dev / docker

Build and run using the environment variables in `.env` file
and `config.json`:

```sh
docker build -t dispatcher . && docker run -it --env-file .env -v $(pwd)/config.json:/src/config.json dispatcher
```

>Note: if you're running the code outside the docker container,
>you need to set `CONFIG_PATH` environment variable to your `config.json` path.

## Data output

The code sends a POST request to endpoints in `config.json` with
JSON payload, same for both comments and posts, e.g.:

```json
{"id": "j643al2", "created_utc": 1674835189.0}
```

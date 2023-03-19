# dispatcher-service

![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/flam-flam/dispatcher-service/ci.yaml?label=CI&logo=Docker&style=for-the-badge)
![GitHub tag (latest SemVer)](https://img.shields.io/github/v/tag/flam-flam/dispatcher-service?logo=Github&sort=semver&style=for-the-badge)

Small service that streams reddit submissions and comments
to respective endpoints

## Reddit credentials

1. Create new integration credentials at https://www.reddit.com/prefs/apps
    - name: `whatever_you_like_but_perhaps_flam-flam`
    - web app: `select this option`
    - description: `whatever you like, or nothing, it's not mandatory`
    - about url: `https://flam-flam.github.io`
    - redirect uri: `https://flam-flam.github.io`
    - create app: `click this button`

2. Create a new file called `.env` in the root of the repo with the following contents. It's in the `.gitignore` so will not be committed:
    ```env
    REDDIT_CLIENT_ID=<the string underneath "web app">
    REDDIT_CLIENT_SECRET=<the string next to "secret">
    ```

## Local dev / docker

Build and run using the environment variables in `.env` file
and `config.json`:

```sh
make build
```

Run the image with

```sh
make run
```

>Note: if you're running the code outside the docker container,
>you need to set `CONFIG_PATH` environment variable to your `config.json` path.

### Tests

Run the tests with `make test`.

## Data output

The code sends a POST request to endpoints in `config.json` with
JSON payload, same for both comments and submissions, e.g.:

```json
{"id": "j643al2", "created_utc": "2023-03-10T13:12:18+00:00"}
```

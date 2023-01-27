# dispatcher-service

Small service that streams reddit submissions and comments
to respective endpoints

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

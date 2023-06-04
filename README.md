# Wav2Mp3Api

### Requirements

1. Git
2. Docker
3. Docker-compose >= 3.9

### How to run app

1. `git clone https://github.com/paydhi/QuestionsApi.git`
2. `cd Wav2Mp3Api`
3. `docker compose up -d`

Backend now runs on `localhost:8000`, postgres runs on `localhost:5432`.

User:password for DB is `postgres:postgres`, as stated in `settings.py` and
`docker-compose.yml`

To stop app just run `docker compose stop`.

To completely remove containers and networks, run `docker compose down`.

### How to use

There are 3 endpoints:
1. `/api/users/create_user/`
2. `/api/records/upload_record/`
3. `/api/records/download_record/`

**First step**: you will need to create user by sending json `{"username": str}` to 
`/api/users/create_user/` endpoint. In response, you will get json with access token
and user uuid, that looks like this: `{"access_token": UUID, "user_uuid": UUID"}`

**Second step**: now you can send `multipart/form-data` request to `/api/records/upload_record/`
endpoint with params:
* `access_token`: access token from first step's response
* `user_uuid`: user uuid from first step's response
* `file`: wav file, that you want to convert to mp3

In return, you will get a json with download url, that looks like this:

`{"download_url": "http://localhost:8000/api/records/download_record/?id=record_uuid6&user=user_uuid"}`

**Third step**: now you can download converted file through your 
favorite browser, 
by simply following this link

Alternatively, you can use Postman collection, located in root of this repository.
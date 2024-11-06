# Blog app with fastapi

Simple blog application with authorization system, featured with AI content moderation.

## Description

Demonstration project where you can register account, login, create post with topic and leave comments.
In addition you can turn on content moderation by providing google api key to your personal NLP project.
Additional information on:
* https://cloud.google.com/natural-language

## Getting Started

### Dependencies

* Python3.9+, Optional: Docker

### Installing

* Clone repository and create virtual environment
```
git clone git@github.com:MirageKoi/blog_fastapi.git
```
* Change directory to the cloned one
```
cd blog_fastapi
```
```
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
```
* You are ready either run tests or server
* To be able using AI moderation you should provide .env file with api key
* ```blog_fastapi/.env``` <--- ```api_key=your_key_here```

### Executing program

* To run tests:
```
python3 -m pytest tests/
```
* To run server:
```
uvicorn src.main:app --reload
```
* After server running you can find all information regarding endpoints, schemas and functionality at
```
http://127.0.0.1:8000/docs
```

## TODO:
pass


from datetime import datetime, date

import requests

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from playhouse.shortcuts import *

from api_requests.TokenAuthorizedHomeworkCreateRequest import TokenAuthorizedHomeworkCreateRequest
from api_requests.TokenAuthorizedNoteCreateRequest import TokenAuthorizedNoteCreateRequest
from api_requests.TokenAuthorizedSubjectCreateRequest import TokenAuthorizedSubjectCreateRequest
from api_requests.TokenAuthorizedWorkCreateRequest import TokenAuthorizedWorkCreateRequest
from models.Homework import Homework
from models.Subject import Subject
from models.Work import Work
from models.Note import Note

app = FastAPI()
HEIMDALL_URL = 'http://heimdall:8000'

origins = [
    "http://heimdall",
    "http://heimdall:8000",
    "http://heimdall:8001",
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:8081",
    "http://localhost:4200",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


async def get_user_uuid(token: str):
    response = requests.get(HEIMDALL_URL + '/auth/validate/', params={'token': token})
    try:
        response = response.json()
        return response['user']['for']
    except KeyError:
        return None


@app.get('/subject/')
async def list_subjects(token: str):
    user_uuid = await get_user_uuid(token)
    if user_uuid is None:
        return {'status': 404}

    try:
        query = Subject.select().where(Subject.user_reference == user_uuid)
        return {'status': 200, 'subjects': [model_to_dict(model) for model in query]}
    except DoesNotExist:
        return {'status': 404}


@app.get('/subject/{weekday}/')
async def list_subject_weekday(weekday: int, token: str):
    user_uuid = await get_user_uuid(token)
    if user_uuid is None:
        return {'status': 404}

    try:
        query = Subject.select().where((Subject.user_reference == user_uuid) & (Subject.weekday == weekday))
        return {'status': 200, 'subjects': [model_to_dict(model) for model in query]}
    except DoesNotExist:
        return {'status': 404}


@app.post('/subject/')
async def create_subject(request: TokenAuthorizedSubjectCreateRequest):
    user_uuid = await get_user_uuid(request.token)
    if user_uuid is None:
        return {'status': 404}

    try:
        subject = Subject.create(short=request.short, name=request.name, room=request.room,
                                 weekday=request.weekday, repeat_interval=request.repeat_interval,
                                 time_start=request.time_start, time_end=request.time_end,
                                 type=request.type, user_reference=user_uuid)

        return {'status': 201, 'subject': subject}
    except Exception as e:
        return {'status': 500, 'error': e}


@app.delete('/subject/{subject_id}/')
async def remove_subject(subject_id: str, token: str):
    user_uuid = await get_user_uuid(token)
    if user_uuid is None:
        return {'status': 404}

    try:
        subject = Subject.get((Subject.id == subject_id) & (Subject.user_reference == user_uuid))
        subject.delete_instance()
        return {'status': 200}
    except Exception as e:
        return {'status': 500, 'error': e}


@app.get('/homework/')
async def list_homework(token: str):
    user_uuid = await get_user_uuid(token)
    if user_uuid is None:
        return {'status': 404}

    try:
        query = Homework.select().where(Homework.user_reference == user_uuid)
        return {'status': 200, 'homeworks': [model_to_dict(model) for model in query]}
    except DoesNotExist:
        return {'status': 404}


@app.post('/homework/')
async def create_subject(request: TokenAuthorizedHomeworkCreateRequest):
    user_uuid = await get_user_uuid(request.token)
    if user_uuid is None:
        return {'status': 404}

    try:
        subject = Homework.create(header=request.header, description=request.description,
                                  deadline=request.deadline, user_reference=user_uuid)

        return {'status': 201, 'homework': subject}
    except Exception as e:
        return {'status': 500, 'error': e}


@app.delete('/homework/{homework_id}/')
async def remove_subject(homework_id: str, token: str):
    user_uuid = await get_user_uuid(token)
    if user_uuid is None:
        return {'status': 404}

    try:
        homework = Homework.get((Homework.id == homework_id) & (Homework.user_reference == user_uuid))
        homework.delete_instance()
        return {'status': 200}
    except Exception as e:
        return {'status': 500, 'error': e}


@app.get('/work/')
async def list_work(token: str):
    user_uuid = await get_user_uuid(token)
    if user_uuid is None:
        return {'status': 404}

    try:
        query = Work.select().where((Work.user_reference == user_uuid) & (Work.workday >= date.today()))
        return {'status': 200, 'workdays': [model_to_dict(model) for model in query]}
    except DoesNotExist:
        return {'status': 404}


@app.post('/work/')
async def create_subject(request: TokenAuthorizedWorkCreateRequest):
    user_uuid = await get_user_uuid(request.token)
    if user_uuid is None:
        return {'status': 404}

    try:
        subject = Work.create(topic=request.topic, workday=request.workday,
                              since=request.since, until=request.until,
                              user_reference=user_uuid)

        return {'status': 201, 'work': subject}
    except Exception as e:
        return {'status': 500, 'error': e}


@app.get('/note/')
async def list_notes(token: str):
    user_uuid = await get_user_uuid(token)
    if user_uuid is None:
        return {'status': 404}

    try:
        query = Note.select().where(Note.user_reference == user_uuid)
        return {'status': 200, 'notes': [model_to_dict(model) for model in query]}
    except DoesNotExist:
        return {'status': 404}


@app.post('/note/')
async def create_subject(request: TokenAuthorizedNoteCreateRequest):
    user_uuid = await get_user_uuid(request.token)
    if user_uuid is None:
        return {'status': 404}

    try:
        subject = Note.create(name=request.name,  content=request.content,
                              created=request.created, priority=request.priority,
                              notify=request.notify, user_reference=user_uuid)

        return {'status': 201, 'note': subject}
    except Exception as e:
        return {'status': 500, 'error': e}

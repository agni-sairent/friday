import requests

from fastapi import FastAPI
from peewee import DoesNotExist

from api_requests.TokenAuthorizedHomeworkCreateRequest import TokenAuthorizedHomeworkCreateRequest
from api_requests.TokenAuthorizedNoteCreateRequest import TokenAuthorizedNoteCreateRequest
from api_requests.TokenAuthorizedSubjectCreateRequest import TokenAuthorizedSubjectCreateRequest
from api_requests.TokenAuthorizedWorkCreateRequest import TokenAuthorizedWorkCreateRequest
from models.Homework import Homework
from models.Subject import Subject
from models.Work import Work
from models.Note import Note
from api_requests.GenericTokenRequest import GenericTokenRequest

app = FastAPI()
HEIMDALL_URL = 'http://localhost:8000'


async def get_user_uuid(token: str):
    response = requests.get(HEIMDALL_URL + '/auth/validate/', params={'token': token})
    try:
        response = response.json()
        return response['user']['for']
    except KeyError:
        return None


@app.get('/subjects/')
async def list_subjects(request: GenericTokenRequest):
    user_uuid = await get_user_uuid(request.token)
    if user_uuid is None:
        return {'status': 404}

    try:
        query = Subject.select().where(Subject.user_reference == user_uuid)
        return {'status': 200, 'subjects': list(query)}
    except DoesNotExist:
        return {'status': 404}


@app.post('/subjects/create/')
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


@app.get('/homework/')
async def list_homework(request: GenericTokenRequest):
    user_uuid = await get_user_uuid(request.token)
    if user_uuid is None:
        return {'status': 404}

    try:
        query = Homework.select().where(Homework.user_reference == user_uuid)
        return {'status': 200, 'subjects': list(query)}
    except DoesNotExist:
        return {'status': 404}


@app.post('/homework/create/')
async def create_subject(request: TokenAuthorizedHomeworkCreateRequest):
    user_uuid = await get_user_uuid(request.token)
    if user_uuid is None:
        return {'status': 404}

    try:
        subject = Homework.create(header=request.header, description=request.description,
                                  deadline=request.deadline, user_reference=user_uuid)

        return {'status': 201, 'subject': subject}
    except Exception as e:
        return {'status': 500, 'error': e}


@app.get('/work/')
async def list_work(request: GenericTokenRequest):
    user_uuid = await get_user_uuid(request.token)
    if user_uuid is None:
        return {'status': 404}

    try:
        query = Work.select().where(Work.user_reference == user_uuid)
        return {'status': 200, 'subjects': list(query)}
    except DoesNotExist:
        return {'status': 404}


@app.post('/work/create/')
async def create_subject(request: TokenAuthorizedWorkCreateRequest):
    user_uuid = await get_user_uuid(request.token)
    if user_uuid is None:
        return {'status': 404}

    try:
        subject = Work.create(topic=request.topic, workday=request.workday,
                              since=request.since, until=request.until,
                              user_reference=user_uuid)

        return {'status': 201, 'subject': subject}
    except Exception as e:
        return {'status': 500, 'error': e}


@app.post('/notes/')
async def list_notes(request: GenericTokenRequest):
    user_uuid = await get_user_uuid(request.token)
    if user_uuid is None:
        return {'status': 404}

    try:
        query = Note.select().where(Note.user_reference == user_uuid)
        return {'status': 200, 'subjects': list(query)}
    except DoesNotExist:
        return {'status': 404}


@app.post('/notes/create/')
async def create_subject(request: TokenAuthorizedNoteCreateRequest):
    user_uuid = await get_user_uuid(request.token)
    if user_uuid is None:
        return {'status': 404}

    try:
        subject = Note.create(name=request.name,  content=request.content,
                              created=request.created, priority=request.priority,
                              notify=request.notify, user_reference=user_uuid)

        return {'status': 201, 'subject': subject}
    except Exception as e:
        return {'status': 500, 'error': e}

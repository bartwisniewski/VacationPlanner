import os

import requests
from places.forms import PlaceScrapForm
from places.scrapper import celery_states
from places.scrapper.schemas import Query
from places.scrapper.serializers import QuerySerializer


def url():
    host = os.environ.get("SCRAPPER_HOST", "127.0.0.1")
    port = os.environ.get("SCRAPPER_PORT", "8001")
    return f"http://{host}:{port}"


def new_scrap(form: PlaceScrapForm) -> str:
    endpoint = "/scrapper/scrap/"
    query = Query.from_form(form)
    serializer = QuerySerializer(query)
    response = requests.post(url() + endpoint, json=serializer.data)
    if response.status_code != 200:
        return ""
    return response.json().get("task_id", None)


def get_result(task_id: str):
    endpoint = f"/scrapper/result/{task_id}/"
    done, ok = check_if_done(task_id)
    result = []
    if done and ok:
        response = requests.get(url() + endpoint)
        data = response.json()
        result = data.get("result", [])
    return {"done": done, "ok": ok, "result": result}


def check_if_done(task_id: str):
    endpoint = f"/scrapper/check/{task_id}/"
    response = requests.get(url() + endpoint)
    data = response.json()
    status = data.get("status", "")
    if status in celery_states.READY_STATES:
        ok = status == celery_states.SUCCESS
        return True, ok  # done, ok
    return False, False

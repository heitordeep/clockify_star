import json
from datetime import date as dt
from datetime import datetime, timedelta
from os import path

import pendulum
from rich.console import Console

from clockify_app.response_request import HandleRequests

console = Console()

local_tz = pendulum.timezone('America/Sao_Paulo')

request = HandleRequests()


class Clockify:
    def __init__(self):
        self.hour = datetime.now(tz=local_tz) + timedelta(hours=3)

    @staticmethod
    def read_file(file_name: str) -> dict:
        with open(path.join('job/', f'{file_name}.json'), 'r') as f:
            data = json.loads(f.read())

        return data

    def start(self, job: dict):

        job.update(
            {'start': f'{dt.today()}T{self.hour.strftime("%H:%M:%S")}Z'}
        )
        request.post(job)

    def end(self):

        request.patch(
            {"end": f'{dt.today()}T{self.hour.strftime("%H:%M:%S.%f")}Z'}
        )

    def build_tags(self, tags: dict, job: dict) -> dict:
        payload = []

        for tag_job in job['tagIds']:
            if tag_job in tags.keys():
                payload.append(tags[tag_job])

        job['tagIds'] = payload

        return job

    def build_job(self):

        data = [
            self.read_file(file_name) for file_name in ['tags', 'start_job']
        ]

        # files[0] - tags api
        # files[1] - Tags of start_job
        job = self.build_tags(*data)

        validate_size = lambda x, v: len(x) == len(v)

        if validate_size(job['tagIds'], data[1]['tagIds']):
            self.start(job)
        else:
            console.print(
                f'[bold red]Ops, tags inválidas ou nula.\n'
                'Verifique o arquivo start_job.json [/bold cyan] :smiley:'
            )

import json
from datetime import date as dt
from datetime import datetime, timedelta
from os import path

from rich.console import Console

import pendulum
from clockify_app.update_requests import HandleRequests

console = Console()

local_tz = pendulum.timezone('America/Sao_Paulo')

request = HandleRequests()


class Clockify:
    def __init__(self):
        self.hour = datetime.now(tz=local_tz) + timedelta(hours=3)

    def start(self, job: dict):

        job.update(
            {'start': f'{dt.today()}T{self.hour.strftime("%H:%M:%S")}Z'}
        )
        request.post(job)

    def end(self):

        data = {"end": f'{dt.today()}T{self.hour.strftime("%H:%M:%S.%f")}Z'}
        request.patch(data)

    def create_job(self, job: list, tags: list) -> dict:
        payload = {}

        if job['taskId'] == 0:
            del job['taskId']

        for tag_job in job['tagIds']:
            if tag_job in tags.keys():
                payload[tag_job] = tags[tag_job]

        job['tagIds'] = list(payload.values())

        return payload

    def read_file(self, file_name: str) -> dict:

        with open(path.join('job/', f'{file_name}.json'), 'r') as f:
            data = json.loads(f.read())

        return data

    def get_job(self):

        files_names = ['tags', 'start_job']

        files = [self.read_file(x) for x in files_names]

        # files[0] - tags api and files[1] - Tags of start_job
        content = self.create_job(files[1], files[0])

        validation_count = lambda x, v: len(x) == len(v)

        if validation_count(content, files[1]['tagIds']):
            self.start(files[1])
        else:
            console.print(
                f'\n[bold red]Ops, tags invalidas ou vázias\nTags que foram passadas: '
                f'{" | ".join(tag for tag in tag_job["tagIds"])}\n[/bold red]'
                '[bold red]Recomendo você olhar o seu arquivo[/bold red] '
                '[bold cyan]start_job.json[/bold cyan] :smiley:'
            )

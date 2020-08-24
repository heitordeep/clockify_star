import json
from datetime import date as dt
from datetime import datetime, timedelta
from os import path

import requests
from decouple import config
from requests.exceptions import HTTPError
from rich.console import Console

console = Console()


class Clockify:
    def __init__(self):
        self.headers = {
            'X-Api-Key': config('key'),
            'content-type': 'application/json',
        }
        self.endpoint = f'workspaces/{config("workspaces")}/user/{config("user")}/time-entries'
        self.allowed_url = f'https://api.clockify.me/api/v1/{self.endpoint}'
        self.hour = datetime.now() + timedelta(hours=3)

    def start(self, job, payload):
        job['tagIds'] = payload
        data = {
            "start": f'{dt.today()}T{self.hour.strftime("%H:%M:%S")}Z',
        }

        if len(payload) != 0 and job['taskId'] != 0:
            for key, value in job.items():
                data.update({key: value})

        else:
            del job['taskId']

            for key, value in job.items():
                data.update({key: value})

        self.post(data)

    def end(self):

        data = {"end": f'{dt.today()}T{self.hour.strftime("%H:%M:%S.%f")}Z'}

        self.patch(data)

    def post(self, data):

        try:

            response = requests.post(
                f'{self.allowed_url}',
                headers=self.headers,
                data=json.dumps(data),
            )

            response.raise_for_status()

            console.print(
                f'\n[bold yellow]Logado com sucesso![/bold yellow] :smiley:'
            )

        except HTTPError as error:
            console.print(
                f'POST:\n[bold red]Ops, algo deu errado ao finalizar!\n'
                f'Error:\n{error}[/bold red]'
            )

    def patch(self, data):

        try:

            response = requests.patch(
                f'{self.allowed_url}',
                headers=self.headers,
                data=json.dumps(data),
            )

            response.raise_for_status()

            console.print(
                f'\n[bold yellow]Deslogado com sucesso![/bold yellow] :smiley:'
            )

        except HTTPError as error:
            console.print(
                f'Patch:\n[bold red]Ops, algo deu errado ao finalizar!\n'
                f'Error:\n{error}[/bold red]'
            )

    def get_job(self):

        payload = []
        files_names = ['tags', 'start_job']
        files = {}

        for file_name in files_names:
            with open(path.join('job/', f'{file_name}.json'), 'r') as f:
                files[file_name] = json.loads(f.read())

        tag = files['tags']
        tag_job = files['start_job']['tagIds']

        for name in tag.keys():
            if name in tag_job:
                payload.append(tag[name])

        if len(tag_job) == len(payload):
            self.start(files['start_job'], payload)
        else:
            console.print(
                f'\n[bold red]Ops, tags invalidas, verifique se está correto: '
                f'{" | ".join(tag for tag in tags)}\n[/bold red]'
                '[bold red]Recomendo você olhar o seu arquivo[/bold red] '
                '[bold cyan]start_job.json[/bold cyan] :smiley:'
            )

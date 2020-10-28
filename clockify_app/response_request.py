import json
from datetime import date as dt
from datetime import datetime, timedelta

import pendulum
import requests
from decouple import config
from requests.exceptions import HTTPError
from rich.console import Console

console = Console()
local_tz = pendulum.timezone('America/Sao_Paulo')


class HandleRequests:
    def __init__(self):
        self.allowed_url = (
            f'https://api.clockify.me/api/v1/workspaces/{config("workspaces")}'
        )
        self.headers = {
            'X-Api-Key': config('key'),
            'content-type': 'application/json',
        }
        self.hour = datetime.now(tz=local_tz) + timedelta(hours=3)

    def get(self, url):

        try:
            response = requests.get(
                f'{self.allowed_url}/{url}', headers=self.headers,
            )
            response.raise_for_status()

            return response

        except HTTPError as error:
            console.print(
                f'POST:\n[bold red]Ops, algo deu errado ao finalizar!\n'
                f'Error:\n{error}[/bold red]'
            )

    def post(self, data):

        try:

            response = requests.post(
                f'{self.allowed_url}/user/{config("user")}/time-entries',
                headers=self.headers,
                data=json.dumps(data),
            )

            response.raise_for_status()

            console.print(
                f'[bold yellow]Logado com sucesso! - '
                f'Hora: {dt.today()} - {self.hour.strftime("%H:%M:%S")}'
                '[/bold yellow] :smiley:'
            )

        except HTTPError as error:
            console.print(
                f'POST:\n[bold red]Ops, algo deu errado ao finalizar!\n'
                f'Error:\n{error}[/bold red]'
            )

    def patch(self, data):

        try:

            response = requests.patch(
                f'{self.allowed_url}/user/{config("user")}/time-entries',
                headers=self.headers,
                data=json.dumps(data),
            )

            response.raise_for_status()

            console.print(
                f'[bold yellow]Deslogado com sucesso! - '
                f'Hora: {dt.today()} - {self.hour.strftime("%H:%M:%S")}'
                '[/bold yellow] :smiley:'
            )

        except HTTPError as error:
            console.print(
                f'Patch:\n[bold red]Ops, algo deu errado ao finalizar!\n'
                f'Error:\n{error}[/bold red]'
            )

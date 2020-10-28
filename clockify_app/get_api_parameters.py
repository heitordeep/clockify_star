import json
from datetime import date as dt
from os import path
from sys import argv

from rich.console import Console

from response_request import HandleRequests

console = Console()

request = HandleRequests()


def build_json(parameter: str, url: str):

    response = request.get(url)

    data_json = {data['name']: data['id'] for data in response.json()}

    if data_json:
        save_file(parameter, data_json)
    else:
        console.print(f'[bold red]Nenhum dado encontrado![/bold red]')


def save_file(file_name: str, data: str):

    with open(path.join('job', f'{file_name}.json'), 'w') as f:
        f.write(json.dumps(data, ensure_ascii=False))

    console.print(
        f'[bold green]Arquivo {file_name}.json está pronto para uso! - '
        f'create_at: {dt.today()}[/bold green]'
    )


def validation_parameter(parameter: list):

    # parameter[0] - Name of the function to be called.
    # parameter[1] - Project Id.
    key = parameter[0]

    allowed_url = {'project_id': '/projects', 'tags': '/tags?page-size=1000'}

    # In method task it's necessary to pass two parameter: task and project id.
    if 'task' in key:
        allowed_url[key] = f'/projects/{parameter[1]}/tasks?page-size=1000'

    try:
        url = allowed_url[key]
        build_json(key, url)
    except KeyError:
        console.print(
            '[bold red]Você só possui permissões das seguintes pesquisas:'
            '[/bold red]\n[bold cyan]task | project_id | tags[/bold cyan]'
        )


if __name__ == "__main__":
    validation_parameter(argv[1:])

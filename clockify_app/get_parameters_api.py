import json
from os import path
from sys import argv

import requests
from decouple import config
from rich.console import Console

console = Console()

headers = {
    'X-Api-Key': config('key'),
    'content-type': 'application/json',
}

allowed_url = 'https://api.clockify.me/api/v1/'


def get_projects():

    response = requests.get(
        f'{allowed_url}workspaces/{config("workspaces")}/projects',
        headers=headers,
    )

    data_project = {
        project['name']: project['id'] for project in response.json()
    }

    save_files('projects_id', data_project)


def get_task():
    response = requests.get(
        f'{allowed_url}workspaces/{config("workspaces")}/projects/{argv[2]}/tasks?page-size=1000',
        headers=headers,
    )

    data_task = {project['name']: project['id'] for project in response.json()}

    if data_task:
        save_files('task', data_task)
    else:
        console.print(
            f'\n[bold red]Não possui tasks no projeto pesquisado.[/bold red]'
        )


def get_tags():
    response = requests.get(
        f'{allowed_url}workspaces/{config("workspaces")}/tags?page-size=1000',
        headers=headers,
    )

    data_tags = {tags['name']: tags['id'] for tags in response.json()}

    save_files('tags', data_tags)


def save_files(file_name, data):

    with open(path.join('job', f'{file_name}.json'), 'w') as f:
        f.write(json.dumps(data, ensure_ascii=False))

    console.print(
        f'\n[bold green]Arquivo {file_name}.json está pronto para uso![/bold green]'
    )


def read_projects():
    with open(path.join('job', 'projects_id.json'), 'r') as projects:
        data = json.loads(projects.read())

    data_projects = '\n'.join(
        {"{!r}: {!r}".format(k, v) for k, v in data.items()}
    )

    console.print(
        f'\n[bold yellow]Projects:[/bold yellow]\n[bold blue]{data_projects}[/bold blue]'
    )


if __name__ == "__main__":

    # Two parameters, get_task and a projectID
    list_taks = {
        'get_task': get_tags,
        'get_project': get_projects,
        'list_projects': read_projects,
        'get_tags': get_tags
    }

    parameter = argv[1]
    if parameter in list_taks.keys():
        list_taks[parameter]()

    else:
        console.print(
            '[bold red]Você só possui permissões das seguintes pesquisas:[/bold red]\n'
            '[bold cyan]get_task | get_project | list_projects[/bold cyan]'
        )

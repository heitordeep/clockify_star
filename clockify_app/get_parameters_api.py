import json
from datetime import date as dt
from datetime import datetime, timedelta
from os import path
from sys import argv

from rich.console import Console

from update_requests import HandleRequests

console = Console()
request = HandleRequests()


class HandleParameters:
    def get_projects(self):

        response = request.get(url='/projects')

        data_project = {
            project['name']: project['id'] for project in response.json()
        }

        self.save_file('projects_id', data_project)

    def get_tasks(self):

        response = request.get(url=f'/projects/{argv[2]}/tasks?page-size=1000')

        data_task = {
            project['name']: project['id'] for project in response.json()
        }

        if data_task:
            self.save_file('task', data_task)
        else:
            console.print(
                f'\n[bold red]Não possui tasks no projeto pesquisado.[/bold red]'
            )

    def get_tags(self):

        response = request.get(url='/tags?page-size=1000')

        data_tags = {tags['name']: tags['id'] for tags in response.json()}

        self.save_file('tags', data_tags)

    def save_file(self, file_name, data):

        with open(path.join('job', f'{file_name}.json'), 'w') as f:
            f.write(json.dumps(data, ensure_ascii=False))

        console.print(
            f'\n[bold green]Arquivo {file_name}.json está pronto para uso![/bold green]'
        )

    def read_projects(self):
        with open(path.join('job', 'projects_id.json'), 'r') as projects:
            data = json.loads(projects.read())

        data_projects = '\n'.join(
            {"{!r}: {!r}".format(k, v) for k, v in data.items()}
        )

        console.print(
            f'\n[bold yellow]Projects:[/bold yellow]\n[bold blue]{data_projects}[/bold blue]'
        )

    def validation_parameter(self, parameter):

        # Two parameters, get_task and a projectID
        list_taks = {
            'get_task': parameters.get_tasks,
            'get_project': parameters.get_projects,
            'list_projects': parameters.read_projects,
            'get_tags': parameters.get_tags,
        }

        if parameter in list_taks.keys():
            list_taks[parameter]()
        else:
            console.print(
                '[bold red]Você só possui permissões das seguintes pesquisas:[/bold red]\n'
                '[bold cyan]get_task | get_project | list_projects[/bold cyan]'
            )


if __name__ == "__main__":

    parameters = HandleParameters()
    parameters.validation_parameter(argv[1])

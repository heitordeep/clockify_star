from sys import argv

from rich.console import Console

from clockify_app.clockify import Clockify

console = Console()
post_hour = Clockify()

if __name__ == "__main__":

    if 'stop' == argv[1]:
        post_hour.end()
    elif 'start' == argv[1]:
        post_hour.get_job()
    else:
        console.print(
            '[bold red]Opção digitada é invalida\nVocê só pode passar paramêtro STOP ou START[/bold red]'
        )

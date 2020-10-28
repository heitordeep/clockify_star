from sys import argv

from rich.console import Console

from clockify_app.clockify import Clockify

console = Console()


exec_clockify = Clockify()

if __name__ == "__main__":

    if 'stop' in argv[1]:
        exec_clockify.end()
    elif 'start' in argv[1]:
        exec_clockify.build_job()
    else:
        console.print(
            '[bold red]Opção digitada é invalida\nVocê só pode passar paramêtro:'
            ' STOP ou START[/bold red]'
        )

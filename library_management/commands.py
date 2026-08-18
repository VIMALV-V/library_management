import click


@click.command("hello-app")
def hello_app():
    print("Hello from custom command!")


commands = [hello_app]

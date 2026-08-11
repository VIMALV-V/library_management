import click


@click.command()
def hello():
    print("Hello from the custom Bench CLI!")


commands = [hello]

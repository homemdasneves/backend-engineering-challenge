import click
from managers.event_manager import EventManager

@click.group()
def cli():
    pass

@cli.command()
@click.option(
    '--input_file',
    type=click.STRING,
    prompt="Input JSON file with events", 
    help="Source json file to parse with the translation events.",
)
@click.option(
    "--window_size", 
    type=click.INT,
    prompt="Minutes to consider", 
    default=10,
    help="Last minutes for which to process events for the moving average")
def moving_avg(input_file, window_size):
    """ cals a moving avg of the delivery times from an events file"""
    click.echo(f"input_file: {input_file}; window_size: {window_size}")
    mng = EventManager()
    output = mng.calc_moving_average(input_file, window_size)
    click.echo(output)

@cli.command()
def generate_dummy_file():
    """ generates a dummy events file
    """
    mng = EventManager()
    mng.generate_events(50)

if __name__ == '__main__':
    cli()
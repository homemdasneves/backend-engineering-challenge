import click
from managers.event_manager import EventStream

@click.group()
def cli():
    pass

@cli.command()
@click.option(
    "--input_file",
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
    """ Calculates a moving average of the delivery times from an events file"""
    click.echo(f"input_file: {input_file}; window_size: {window_size}")

    event_stream = EventStream()
    output = event_stream.calc_moving_average(input_file, window_size)

    click.echo(output)

@cli.command()
def generate_dummy_file():
    """ generates a dummy events file
    """
    event_stream = EventStream()
    event_stream.generate_events(50, 5, "dummy_data.txt")

if __name__ == "__main__":
    cli()
import click

from .scrape import scrape as _scrape

@click.group()
def cli():
    """
    The Leapfrog CLI for managing scraping activities at
    https://www.hospitalsafetygrade.org/
    """

cli.add_command(_scrape)
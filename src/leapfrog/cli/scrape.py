'''
CLI scrape commands for leapfrog

author(s): Derek Herincx, derek663@gmail.com
last_updated: 01/15/2022
'''
from functools import wraps
import json
import os

import click
from click import Argument, Choice, Path, UsageError

from leapfrog import LeapfrogScraper
from leapfrog.utilities import URL

# sys.tracebacklimit = 0
VALID_FINDBY_CHOICES = ['city', 'zip_code', 'hospital', 'state']
# keys that we use within the CLI, but not needed for the URL creation
# including additional keys doesn't cause the script to fail, but don't
# want to confuse end users about their presence
KEYS_TO_EXCLUDE = ['num_reviews', 'output', 'test']
DOMAIN = 'https://www.hospitalsafetygrade.org/search?'

def name_casing(func):
    """Preserves original casing of any parameter name. Parameters, as
    defined by `click`, are both defined by the classes :class:`Argument`
    and :class:`Option`"""
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        name, opts, secondary_opts = func(self, *args, **kwargs)
        if self.preserve_casing:
            name = opts[0]
        return name, opts, secondary_opts
    return wrapper

class ArgumentWithCasing(Argument):
    """The command class to instantiate for a given `click` decorator. This
    allows us to further customize our CLI interface by specifying
    the :param:`cls` value
    """
    def __init__(self, *args, **kwargs):
        self.preserve_casing = kwargs.pop('preserve_casing')
        super().__init__(*args, **kwargs)

    @name_casing
    def _parse_decls(self, decls, expose_value):
        """Overwrites the :meth:`_parse_decls` in :class:`Parameter`
        because `click` automatically lower cases all parameter names, which
        we don't want since leapfrog requires the `findBy` key to be camel
        case
        """
        return super()._parse_decls(decls, expose_value)

@click.command()
@click.argument(
    "findBy",
    type=Choice(VALID_FINDBY_CHOICES),
    required=True,
    cls=ArgumentWithCasing,
    preserve_casing=True
)
@click.argument('output', type=Path(exists=False))
@click.option("-t", "--test", required=False, default=False, type=bool)
@click.option("-c", "--city", required=False)
@click.option("-z", "--zip_code", required=False)
@click.option("-s", "--state", required=False)
@click.option("-h", "--hospital", required=False)
@click.pass_context
def scrape(ctx, findBy, output, test, city, zip_code, state, hospital):
    """
    Scrape command indicating the level of scraping to perform

    \b
    Usage:
        $ leapfrog scrape [FINDBY] [-t, --TEST] [-r, --NUM_REVIEWS]
            [-c, --CITY] [-z, --ZIP_CODE] [-s, --STATE] [-h, --HOSPITAL]

    \b
    Positional Argument(s):
        FINDBY  Type of scrape to perform
        Possible Choices: city, zip_code, hospital, state

    \b
    Named Arguments:
        -t, --test          Engage test mode, which returns only 1 review
        -c, --city          City name
        -z, --zip_code      5-digit zipcode
        -s, --state         Two-letter U.S. state identifier
        -h, --hospital      Hospital name

    \b
    Examples:
        $ leapfrog scrape -t True state CA
            Gets the first review from the state of California
    """
    # `click` provides a :class:`Context` class that aggregates all the
    # values from all arguments/options in a :type:`dict`, hence we don't
    # need to individually work with parameters from :meth:`scrape`
    params = ctx.params
    if not params[findBy]:
        raise UsageError(f"Option --{findBy} is required")

    parametrized_url = URL(DOMAIN, params, KEYS_TO_EXCLUDE)()
    scraper = LeapfrogScraper(url=parametrized_url)
    reviews = scraper.get_hospital_metadata(test)

    with open(output, 'w') as outfile:
        json.dump(reviews, outfile)

    click.echo(f"Wrote data to {output} successfully!")

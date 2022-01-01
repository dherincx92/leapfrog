import click

VALID_TYPES = ['city_state', 'zip', 'hospital', 'state']
DOMAIN = 'https://www.hospitalsafetygrade.org/search?'

@click.command()
@click.argument("find_by", required=True)
@click.option("-p", "--num-pages", required=False, default=1, type=str)
@click.option("-z", "--zip", required=False)
@click.option("-s", "--state", required=False)
@click.option("-h", "--hospital", required=False)
@click.pass_context
def scrape(ctx, find_by, num_pages, zip, state, hospital):
    """
    Scrape commands indicating the type of scrape to perform

    \b
    Usage:
        $ leapfrog scrape [TYPE] [-p NUM_PAGES][-z ZIP][-s STATE][-h HOSPITAL]

    \b
    Positional Arguments:
        FIND_BY    Type of scrape to perform
        Possible choices: city_state, zip, hospital, state

    \b
    Named Arguments:
        -p, --num-pages     Number of pages to scrape
        Possible choices: Any integer type or the string `all`
        Default: 1
        -z --zip            5-digit zipcode
        -s --state          Two-letter U.S. state identifier
        -h --hospital       Hospital Name

    """
    find_by = find_by.lower()
    if find_by not in VALID_TYPES:
        click.echo(f"`{find_by}` is not a valid scrape type")

    # Echos warning if the scrape you're trying to perform requires
    # extra parameters (i.e. zip for `leapfrog scrape zip`)
    info_dict = ctx.to_info_dict()['command']['params']
    if not ctx.params[find_by]:
        for param in info_dict:
            if (
                param['param_type_name'] != 'argument' and
                '--help' not in param['opts']
            ):
                if param['opts'][1] == f'--{find_by}':
                    prefix = param['opts'][0]
                    click.echo(f"Missing required option: {prefix}")


    try:
        num_pages = int(num_pages)
    except ValueError: # if value provided is the str 'all'
        if num_pages.lower() == 'all':
            num_pages = num_pages


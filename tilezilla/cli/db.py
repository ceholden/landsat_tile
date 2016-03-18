""" Database query operations
"""
import click

from . import options
from ..db import TABLES, Database, DatacubeResource, DatasetResource

opt_db_table = click.argument('table', type=click.Choice(TABLES.keys()))


@click.group(help='Database information and queries')
@options.pass_config
@click.pass_context
def db(ctx, config):
    # Stick in context for sub-commands
    ctx.obj['db'] = Database.from_config(config['database'])


@db.command(short_help='Print database information')
@opt_db_table
@options.pass_config
@click.pass_context
def info(ctx, config, table):
    """ Print table information, like the table fields
    """
    print('Info: "{}"'.format(table))

@db.command(short_help='Search database')
@opt_db_table
@click.option('--filter', 'filter_', type=str,
              callback=options.callback_dict, multiple=True,
              help='Fitler TABLE by attr=value')
@options.pass_config
@click.pass_context
def search(ctx, config, filter_, table):
    """ Search a table according to some filters

    Example: search the "product" table for a given product ID
    """
    print('Search: "{}" where:\n{}'.format(table, filter_))
    query = ctx.obj['db'].session.query(TABLES[table]).filter_by(**filter_)
    for query_row in query:
        from IPython.core.debugger import Pdb; Pdb().set_trace()
        print(query_row)

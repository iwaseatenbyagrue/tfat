import click
import tfat.password as pw


@click.group("password")
def cli():
    """ tfat-password 0.1 - a simple set of tools for generating passwords
    """
    pass


@cli.command()
@click.option(
    "-c", "--count", type=int, default=1, show_default=True,
    help="Number of passwords to generate"
)
@click.option(
    "-e", "--encoding", default="hex", show_default=True,
    type=click.Choice(["hex", "base64","string_escape"]),
    help="Encoding to use on password"
)
@click.argument("size", type=int, default=16)
def generate(size, count, encoding):
    """ Generate a password string of `size`
    """
    for c in range(count):
        click.echo(pw.get_random_string(size, encoding=encoding).strip())


@cli.command()
@click.option(
    "-c", "--count", type=int, default=1, show_default=True,
    help="Number of passwords to create"
)
@click.option(
    "-u", "--uppercase", type=int, default=1, show_default=True,
    help="Minimum number of uppercase characters"
)
@click.option(
    "-l", "--lowercase", type=int, default=1, show_default=True,
    help="Minimum number of lowercase characters"
)
@click.option(
    "-d", "--digits", type=int, default=1, show_default=True,
    help="Minimum number of digits characters"
)
@click.option(
    "-p", "--punctuation", type=int, default=1, show_default=True,
    help="Minimum number of punctuation characters"
)
@click.argument("size", type=int, default=16)
def create(count, size, lowercase, uppercase, punctuation, digits):
    """ Create a password base on character class rules.

    All non-zero characters classes are used to create the password.

    """
    for c in range(count):
        click.echo(pw.get_random_string_from_rules(
            size,
            rules = {
                "lowercase": lowercase,
                "uppercase": uppercase,
                "digits": digits,
                "punctuation": punctuation,
            }
        ))

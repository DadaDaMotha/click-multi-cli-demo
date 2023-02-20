import logging
import textwrap
from pathlib import Path

import click

from rich import pretty

pretty.install()

source_dir = Path(__file__).parent.absolute()
packages_folder = source_dir / "commands"


class CLI(click.MultiCommand):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @property
    def default_log_level(self):
        raise NotImplementedError

    @property
    def plugin_folder(self):
        raise NotImplementedError

    def filename_to_command(self, filename):
        return filename.replace(".py", "").replace("_", "-")

    def command_to_filename(self, command):
        return "{}.py".format(command.replace("-", "_"))

    def list_commands(self, ctx):
        commands = []

        for p in self.plugin_folder.iterdir():
            filename = p.name
            if filename.startswith("__"):
                continue
            if filename.endswith(".py"):
                commands.append(self.filename_to_command(filename))
        commands.sort()

        return commands

    def get_command(self, ctx, command):
        ns = {}
        fn = Path(self.plugin_folder, self.command_to_filename(command))

        if not fn.exists():
            return

        with open(fn) as f:
            code = compile(f.read(), fn, "exec")
            eval(code, ns, ns)

        function_name = self.command_to_filename(command).replace(".py", "")
        cli = ns[function_name]

        return cli


class CookiecutterClickMultiCli(CLI):
    default_log_level = logging.WARN
    plugin_folder = Path(
        Path(__file__).parent, "commands", "cookiecutter_click_multi_cli"
    )


@click.command(
    cls=CookiecutterClickMultiCli,
    help=textwrap.dedent(
        """
    {{ cookiecutter.description }}
    """
    ),
)
@click.version_option(
    prog_name="cookiecutter_click_multi_cli", message="%(prog)s %(version)s"
)
def cookiecutter_click_multi_cli_cli():
    pass

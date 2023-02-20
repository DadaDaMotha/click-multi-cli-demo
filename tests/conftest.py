import shutil
import tempfile
from pathlib import Path

import pytest
from click.testing import CliRunner as BaseCliRunner
from traceback import print_tb
from cookiecutter_click_multi_cli.loader import cookiecutter_click_multi_cli_cli


class CliApp:
    with_traceback = True

    def __init__(self, cli, runner, temp=None, templates_path=None):
        self.cli = cli
        self.temp = temp
        self.templates_path = templates_path
        self.runner = runner

    def run(self, commands, **kwargs):
        return self.runner.invoke(self.cli, commands, **kwargs)


class CliRunner(BaseCliRunner):
    with_traceback = True

    def invoke(self, cli, commands, **kwargs):
        result = super(CliRunner, self).invoke(cli, commands, **kwargs)
        if not result.exit_code == 0 and self.with_traceback:
            print_tb(result.exc_info[2])
            print(result.exception)
        return result


@pytest.fixture(scope="function")
def temporary_directory():
    """Provides a temporary directory that is removed after the test."""
    directory = tempfile.mkdtemp()
    yield directory
    shutil.rmtree(directory)


@pytest.fixture(scope="function")
def temporary_path(temporary_directory):
    """Same as :func:`temporary_directory`, but providing a ``Path`` instead
    of a string."""

    yield Path(temporary_directory)


@pytest.fixture(scope="function")
def runner(temporary_directory):
    runner = CliRunner()
    with runner.isolated_filesystem(temp_dir=temporary_directory):
        yield runner


def create_cli_app(cli, runner, temp_path):
    """Bootstraps the app with a temp folder containing a yaml file
    that includes the settings to use the fixtures template folder to access
    testing templates."""

    return CliApp(cli, temp=temp_path, runner=runner)


@pytest.fixture(scope="function")
def cli_app(temporary_path, runner):
    app = create_cli_app(
        cli=cookiecutter_click_multi_cli_cli,
        runner=runner,
        temp_path=temporary_path,
    )
    yield app

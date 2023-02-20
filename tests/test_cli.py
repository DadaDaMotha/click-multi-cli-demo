import pytest

from cookiecutter_click_multi_cli.utils import module_path_root


def get_subcommands(module):
    folder = module_path_root(module)
    for file in folder.glob("*.py"):
        subcommand = file.parts[-1].replace(".py", "").replace("_", "-")
        if "--" in subcommand:
            continue
        yield subcommand


def test_cli_help(cli_app):
    result = cli_app.run(["--help"])
    assert result.exit_code == 0


@pytest.mark.parametrize(
    "subcommand",
    list(
        get_subcommands(
            "cookiecutter_click_multi_cli.commands.cookiecutter_click_multi_cli"
        )
    ),
)
def test_all_subcommands_help(subcommand, cli_app):
    result = cli_app.run([subcommand, "--help"])
    assert result.exit_code == 0

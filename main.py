import subprocess
import sys

import typer

app = typer.Typer(help="CLI for help managing Git Flow on Windows")


def run_git(command: list[str]):
    try:
        result = subprocess.run(["git"] + command, check=True, text=True)
        return result.returncode == 0
    except subprocess.CalledProcessError as e:
        typer.secho(
            f"Error executing command: git {' '.join(command)}", fg=typer.colors.RED
        )
        raise typer.Exit(code=1)


@app.command()
def init():
    typer.echo("Initializing Git Flow...")

    # Garante que estamos na main/master
    run_git(["checkout", "main"])

    # Crie e muda para a develop
    run_git(["checkout", "-b", "develop"])

    # Push para o remoto
    run_git(["push", "-u", "origin", "develop"])

    typer.secho(
        "Git Flow initialized successfully! You are on the develop branch.",
        fg=typer.colors.GREEN,
    )


@app.command()
def feat_start(name: str):
    typer.echo(f"Creating feature: {name}...")

    run_git(["checkout", "develop"])
    run_git(["pull", "origin", "develop"])

    run_git(["checkout", "-b", f"feature/{name}"])

    typer.secho(
        f"Feature '{name}' created! Good coding journey.", fg=typer.colors.GREEN
    )


@app.command()
def feat_finish(name: str):
    typer.echo(f"Finishing feature: {name}...")

    run_git(["checkout", "develop"])
    run_git(["pull", "origin", "develop"])

    run_git(["merge", f"feature/{name}"])
    run_git(["push", "origin", "develop"])

    run_git(["branch", "-d", f"feature/{name}"])

    typer.secho(
        f"Feature '{name}' integrated to develop and local branch deleted!",
        fg=typer.colors.GREEN,
    )


@app.command()
def release_start(version: str):
    typer.echo(f"Initializing release: {version}...")

    run_git(["checkout", "develop"])
    run_git(["pull", "origin", "develop"])

    run_git(["checkout", "-b", f"release/{version}"])

    typer.secho(
        f"✅ Release '{version}' created successfully from develop!",
        fg=typer.colors.GREEN,
    )
    typer.echo("Make sure to run tests and commit any necessary fixes in this branch.")


@app.command()
def release_finish(version: str):
    typer.echo(f"Finishing release: {version}...")

    run_git(["checkout", "main"])
    run_git(["pull", "origin", "main"])
    run_git(["merge", f"release/{version}"])
    run_git(["push", "origin", "main"])

    tag_name = f"v{version}"
    run_git(["tag", "-a", tag_name, "-m", f"Versao {version}"])
    run_git(["push", "origin", tag_name])

    run_git(["checkout", "develop"])
    run_git(["pull", "origin", "develop"])
    run_git(["merge", f"release/{version}"])
    run_git(["push", "origin", "develop"])

    run_git(["branch", "-d", f"release/{version}"])

    typer.secho(f"🎉 Release '{version}' finished!", fg=typer.colors.GREEN)
    typer.echo(f"Code pushed to 'main' with tag '{tag_name}'.")
    typer.echo("Changes merged back to 'develop'.")


if __name__ == "__main__":
    app()

import subprocess

import typer

app = typer.Typer(help="CLI for help managing Git Flow on Windows")


def run_git(command: list[str], step: int, action: str):
    # Log the sequential action number and a description before executing
    typer.secho(f"{step} - {action}", fg=typer.colors.CYAN)
    # Echo the exact git command being run for traceability
    typer.echo(f"    > git {' '.join(command)}")
    try:
        # Execute the git command and raise on a non-zero exit code
        result = subprocess.run(["git"] + command, check=True, text=True)
        return result.returncode == 0
    except subprocess.CalledProcessError:
        # Report the failing command and abort the CLI execution
        typer.secho(
            f"Error executing command: git {' '.join(command)}", fg=typer.colors.RED
        )
        raise typer.Exit(code=1)


@app.command()
def init():
    typer.echo("Initializing Git Flow...")
    # Ensure we are on main/master
    run_git(["checkout", "main"], 1, "Switch to main")
    # Create and switch to develop
    run_git(["checkout", "-b", "develop"], 2, "Create and switch to develop")
    # Push develop to the remote tracking origin
    run_git(["push", "-u", "origin", "develop"], 3, "Push develop to remote")
    typer.secho(
        "Git Flow initialized successfully! You are on the develop branch.",
        fg=typer.colors.GREEN,
    )


@app.command()
def feat_start(name: str):
    typer.echo(f"Creating feature: {name}...")
    # Move to develop as the feature base
    run_git(["checkout", "develop"], 1, "Switch to develop")
    # Update develop with the remote
    run_git(["pull", "origin", "develop"], 2, "Pull latest develop")
    # Create the feature branch from develop
    run_git(["checkout", "-b", f"feature/{name}"], 3, f"Create feature/{name}")
    typer.secho(
        f"Feature '{name}' created! Good coding journey.", fg=typer.colors.GREEN
    )


@app.command()
def feat_finish(name: str):
    typer.echo(f"Finishing feature: {name}...")
    # Switch back to develop to receive the integration
    run_git(["checkout", "develop"], 1, "Switch to develop")
    # Update develop with the remote
    run_git(["pull", "origin", "develop"], 2, "Pull latest develop")
    # Integrate the feature into develop
    run_git(["merge", f"feature/{name}"], 3, f"Merge feature/{name} into develop")
    # Push the updated develop to the remote
    run_git(["push", "origin", "develop"], 4, "Push develop to remote")
    # Delete the local feature branch
    run_git(["branch", "-d", f"feature/{name}"], 5, f"Delete local feature/{name}")
    typer.secho(
        f"Feature '{name}' integrated to develop and local branch deleted!",
        fg=typer.colors.GREEN,
    )


@app.command()
def release_start(version: str):
    typer.echo(f"Initializing release: {version}...")
    # Move to develop as the release base
    run_git(["checkout", "develop"], 1, "Switch to develop")
    # Update develop with the remote
    run_git(["pull", "origin", "develop"], 2, "Pull latest develop")
    # Create the release branch from develop
    run_git(["checkout", "-b", f"release/{version}"], 3, f"Create release/{version}")
    typer.secho(
        f"Release '{version}' created successfully from develop!",
        fg=typer.colors.GREEN,
    )
    typer.echo("Make sure to run tests and commit any necessary fixes in this branch.")


@app.command()
def release_finish(version: str):
    typer.echo(f"Finishing release: {version}...")
    # Move to main to receive the final version
    run_git(["checkout", "main"], 1, "Switch to main")
    # Update main with the remote
    run_git(["pull", "origin", "main"], 2, "Pull latest main")
    # Integrate the release into main
    run_git(["merge", f"release/{version}"], 3, f"Merge release/{version} into main")
    # Push the updated main to the remote
    run_git(["push", "origin", "main"], 4, "Push main to remote")
    tag_name = f"v{version}"
    # Create an annotated tag for the version
    run_git(
        ["tag", "-a", tag_name, "-m", f"Version {version}"], 5, f"Create tag {tag_name}"
    )
    # Push the tag to the remote
    run_git(["push", "origin", tag_name], 6, f"Push tag {tag_name}")
    # Switch back to develop for the back-merge
    run_git(["checkout", "develop"], 7, "Switch to develop")
    # Update develop with the remote
    run_git(["pull", "origin", "develop"], 8, "Pull latest develop")
    # Integrate the release back into develop
    run_git(["merge", f"release/{version}"], 9, f"Merge release/{version} into develop")
    # Push the updated develop to the remote
    run_git(["push", "origin", "develop"], 10, "Push develop to remote")
    # Delete the local release branch
    run_git(
        ["branch", "-d", f"release/{version}"], 11, f"Delete local release/{version}"
    )
    typer.secho(f"Release '{version}' finished!", fg=typer.colors.GREEN)
    typer.echo(f"Code pushed to 'main' with tag '{tag_name}'.")
    typer.echo("Changes merged back to 'develop'.")


if __name__ == "__main__":
    app()

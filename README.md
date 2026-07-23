<div align="center">
  <img src="assets/logo.svg" alt="flowin logo" width="140" />

  # flowin

  **A CLI that automates the [Git Flow](https://nvie.com/posts/a-successful-git-branching-model/) branching model.**

  Built with [Typer](https://typer.tiangolo.com/) · Managed with [uv](https://docs.astral.sh/uv/)
</div>

---

## What it is

`flowin` wraps the repetitive `git` commands behind Git Flow into a handful of
short, memorable subcommands. Instead of remembering the exact sequence of
`checkout`, `pull`, `merge`, `tag` and `push` for every feature or release, you
run one command and `flowin` executes the steps for you — printing each step and
the exact `git` command it runs, so nothing happens behind your back.

If any `git` step fails, `flowin` reports the failing command and stops
immediately (exit code `1`), leaving the repository in a state you can inspect.

## Requirements

- **Python** 3.9 or newer
- **git** available on your `PATH`
- **[uv](https://docs.astral.sh/uv/)** (recommended) — or plain `pip`

## Installation

### Using uv (recommended)

Clone the repo and let `uv` create the virtual environment and install the
project (including the `typer` dependency) from the lockfile:

```bash
git clone https://github.com/MarcelloBB/flowin
cd flowin
uv sync
```

Run the CLI through `uv`:

```bash
uv run flowin --help
```

To install it as a global tool so `flowin` is available anywhere:

```bash
uv tool install .
flowin --help
```

### Using pip

```bash
git clone https://github.com/MarcelloBB/flowin
cd flowin
pip install -e .
flowin --help
```

## Usage

```bash
flowin [COMMAND] [ARGS]
```

Every command prints the ordered steps and the underlying `git` command before
running it, for example:

```
Creating feature: login...
1 - Switch to develop
    > git checkout develop
2 - Pull latest develop
    > git pull origin develop
3 - Create feature/login
    > git checkout -b feature/login
Feature 'login' created! Good coding journey.
```

### Commands

| Command | Argument | What it does |
| --- | --- | --- |
| `init` | — | Bootstraps Git Flow: creates the `develop` branch from `main` and pushes it to `origin`. |
| `feat-start` | `<name>` | Creates `feature/<name>` from an up-to-date `develop`. |
| `feat-finish` | `<name>` | Merges `feature/<name>` into `develop`, pushes it, and deletes the local feature branch. |
| `release-start` | `<version>` | Creates `release/<version>` from an up-to-date `develop`. |
| `release-finish` | `<version>` | Merges the release into `main`, tags it `v<version>`, back-merges into `develop`, pushes everything, and deletes the local release branch. |

### Examples

```bash
# One-time setup of the Git Flow branches
flowin init

# Start working on a feature, then integrate it
flowin feat-start login
flowin feat-finish login

# Cut a release, stabilize it, then ship it
flowin release-start 1.2.0
# ...run tests, commit fixes on the release branch...
flowin release-finish 1.2.0   # tags the commit as v1.2.0
```

## How it works

`flowin` follows the classic Git Flow model with two long-lived branches:

- **`main`** — always production-ready; every commit is a released version.
- **`develop`** — the integration branch where features come together.

Supporting branches are short-lived:

- **`feature/*`** — branch off `develop`, merge back into `develop`.
- **`release/*`** — branch off `develop`, merge into both `main` (tagged) and
  `develop`.

Under the hood each command is a thin, traceable sequence of `git` calls made
through `run_git()` in [`main.py`](main.py). It runs `git` via `subprocess`,
echoes each step, and aborts the whole flow the moment a command returns a
non-zero exit code.

```
              feat-start                 feat-finish
   develop ───────●─────────► feature/x ──────●──────► develop
      │                                                   │
      │ release-start                     release-finish  │
      └──────────► release/y ─────────────────┬───────────┘  (back-merge)
                                              └──► main  (tagged vY)
```

## Development

Set up the environment and run the CLI from source:

```bash
uv sync
uv run flowin --help
```

The project uses a single module, [`main.py`](main.py). Dependencies live in
[`pyproject.toml`](pyproject.toml) and are pinned in `uv.lock` for reproducible
installs.

## License

No license has been declared yet.

<p align="center">
  <img src="./assets/logo.svg" alt="Flowin Logo" width="120">
</p>

<h1 align="center">Flowin</h1>

<p align="center">
  A minimalist helper for Git Flow.
</p>

---

## Overview

**Flowin** is a CLI tool designed to simplify and automate your Git Flow operations. Instead of manually running repetitive sequences of Git commands for branches, releases, hotfixes, and features, Flowin provides intuitive commands to manage your repository's workflow effortlessly.

## How It Works
Flowin automates the Git Flow strategy by executing the underlying Git commands for you behind a single CLI:

* **Feature Workflow:** Spawns a dedicated feature branch from `develop`, tracks your work, and automatically merges it back into `develop` once complete, cleaning up the local branch.
* **Release Management:** Cuts a release branch from `develop`, prepares versioning, and handles the dual merge into both `main` and `develop` along with automatic Git tagging.
* **Hotfixes:** Quickly branches off from `main` to address critical production issues, merging the fix back into both `main` and `develop` simultaneously.

## Installation

You can install it by cloning the repo and calling `pip`
```bash
git clone https://github.com/MarcelloBB/flowin.git
cd flowin
pip install -e .
```

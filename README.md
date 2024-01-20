# Gester

Gester is a creative collection of games utilizing an in-house gesture processing library that reads in webcam data to generate an approximation of your hand moving on a desk.

## Stack

## Getting Started

First, run
```bash
git submodule update --init --recursive
```

This instructions will be for MacOS only.

First, install some dependcies and restart your shell:
```bash
brew update
brew install pyenv
brew install pipx
```

Make sure that you follow the [pyenv](https://github.com/pyenv/pyenv) directions to set up your shell.

Now navigate to this direction (`gesture-library/`):
```bash
pyenv install 3.12
pyenv local 3.12
```

Now get poetry (our dependency manager), create a virtual environment, and install our dependencies:
```
pipx install poetry
poetry shell
poetry install
```


## Screenshots
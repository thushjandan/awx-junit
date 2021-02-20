![Build status](https://github.com/thushjandan/awx-junit/actions/workflows/python-test.yml/badge.svg?branch=main)
[![PyPI version](https://badge.fury.io/py/awx-junit.svg)](https://badge.fury.io/py/awx-junit)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/awx-junit?style=flati)
![PyPI - License](https://img.shields.io/pypi/l/awx-junit)
![Libraries.io dependency status for latest release](https://img.shields.io/librariesio/release/pypi/awx-junit)

# awx-junit
> A command utility to generate a JUnit XML report from an Ansible Tower or AWX Job.

## Installation
Install awx-junit with pip.
```sh
pip install awx-junit
```

## Usage Example
Use the AWX cli (awxkit) to get job events of a certain job from an Ansible Tower or AWX instance. Pipe the resulting JSON output from awxcli to awx-junit utility
```sh
awx job_events list --job <job_id> --all | awx-junit
```

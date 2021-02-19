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

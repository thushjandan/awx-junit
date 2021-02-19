# awx-junit
> A command utility to generate a JUnit XML report from an Ansible Tower or AWX Job.

## Installation
Install awx-junit with pip.
```sh
pip install awx-junit
```

## Usage Example
Use the AWX cli (awxkit) to get the job events from a Ansible Tower or AWX instance. Pipe the resulting JSON to awx-junit utility
```sh
awx job_events list --job <job_id> --all | awx-junit
```

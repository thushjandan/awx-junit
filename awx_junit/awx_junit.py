#!/usr/bin/env python3
import sys
import os
import json
import argparse
from collections import defaultdict
from junit_xml import TestSuite, TestCase


AWX_FAILED_EVENTS = [
    'runner_on_failed', 
    'runner_on_async_failed', 
]

AWX_OK_EVENTS = [
    'runner_on_ok', 
    'runner_on_async_ok', 
]

AWX_ERROR_EVENTS = [
    'runner_on_error', 
    'runner_on_unreachable'
]

AWX_SKIPPED_EVENTS = [
    'runner_on_skipped', 
]

AWX_EVENTS = AWX_FAILED_EVENTS + AWX_OK_EVENTS + AWX_ERROR_EVENTS + AWX_SKIPPED_EVENTS


def main():
    my_parser = argparse.ArgumentParser(prog='awx-junit',
        usage='awx job_events list --job <job_id> --all | awx-junit',
        description='Generates a JUnit XML report from a JSON formatted AWX job events.'
    )
    args = my_parser.parse_args()

    if sys.stdin.isatty():
        print("stdin does not contain a JSON", file=sys.stderr)
        my_parser.print_help(sys.stderr)
        sys.exit(1)

    try:
        awx_data = json.load(sys.stdin)
    except TypeError:
        print("Invalid JSON", file=sys.stderr)
        my_parser.print_help(sys.stderr)
        sys.exit(1)
    except ValueError:
        print("Input is not a JSON", file=sys.stderr)
        my_parser.print_help(sys.stderr)
        sys.exit(1)

    # Check datastructure
    if not 'results' in awx_data:
        print("Content does not look like AWX job_events payload", file=sys.stderr)
        my_parser.print_help(sys.stderr)
        sys.exit(1)

    test_suites = defaultdict(dict)
    for result in awx_data['results']:
        if result['event'] in AWX_EVENTS:
            case = TestCase(
                name="{} on {}".format(result['task'], result['host_name']),
                classname=os.path.splitext(result['event_data']['playbook'])[0].replace('/', '.'),
                file=result['event_data']['playbook']
            )
            if 'duration' in result['event_data']:
                case.elapsed_sec = result['event_data']['duration']

            if 'end' in result['event_data']:
                case.timestamp = result['event_data']['end']

            # Add failure info
            if result['event'] in AWX_FAILED_EVENTS:
                case.add_failure_info(
                    message=result['event_display'], 
                    output=result['stdout']
                )
            # Add error info
            if result['event'] in AWX_ERROR_EVENTS:
                case.add_error_info(
                    message=result['event_display'], 
                    output=result['stdout']
                )
            # Add Skipped message
            if result['event'] in AWX_SKIPPED_EVENTS:
                case.add_skipped_info(
                    message=result['event_display'], 
                    output=result['stdout']
                )

            # Add TestCase to list
            if result['event_data']['task_uuid'] in test_suites:
                test_suites[result['event_data']['task_uuid']]['cases'].append(case)
            else:
                test_suites[result['event_data']['task_uuid']]['name'] = result['event_data']['task']
                test_suites[result['event_data']['task_uuid']]['cases'] = [case]
    # Create TestSuites and add to list
    junit_data = []
    for suite in test_suites.keys():
        junit_data.append(
            TestSuite(test_suites[suite]['name'], test_suites[suite]['cases'])
        )
    # Export to JUnit XML
    sys.stdout.write(TestSuite.to_xml_string(junit_data))

if __name__ == '__main__':
    main()

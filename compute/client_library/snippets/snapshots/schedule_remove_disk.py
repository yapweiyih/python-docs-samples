#  Copyright 2024 Google LLC
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
# flake8: noqa


# This file is automatically generated. Please do not modify it directly.
# Find the relevant recipe file in the samples/recipes or samples/ingredients
# directory and apply your changes there.


# [START compute_snapshot_schedule_remove]
from __future__ import annotations

import sys
from typing import Any

from google.api_core.extended_operation import ExtendedOperation
from google.cloud import compute_v1


def wait_for_extended_operation(
    operation: ExtendedOperation, verbose_name: str = "operation", timeout: int = 300
) -> Any:
    """
    Waits for the extended (long-running) operation to complete.

    If the operation is successful, it will return its result.
    If the operation ends with an error, an exception will be raised.
    If there were any warnings during the execution of the operation
    they will be printed to sys.stderr.

    Args:
        operation: a long-running operation you want to wait on.
        verbose_name: (optional) a more verbose name of the operation,
            used only during error and warning reporting.
        timeout: how long (in seconds) to wait for operation to finish.
            If None, wait indefinitely.

    Returns:
        Whatever the operation.result() returns.

    Raises:
        This method will raise the exception received from `operation.exception()`
        or RuntimeError if there is no exception set, but there is an `error_code`
        set for the `operation`.

        In case of an operation taking longer than `timeout` seconds to complete,
        a `concurrent.futures.TimeoutError` will be raised.
    """
    result = operation.result(timeout=timeout)

    if operation.error_code:
        print(
            f"Error during {verbose_name}: [Code: {operation.error_code}]: {operation.error_message}",
            file=sys.stderr,
            flush=True,
        )
        print(f"Operation ID: {operation.name}", file=sys.stderr, flush=True)
        raise operation.exception() or RuntimeError(operation.error_message)

    if operation.warnings:
        print(f"Warnings during {verbose_name}:\n", file=sys.stderr, flush=True)
        for warning in operation.warnings:
            print(f" - {warning.code}: {warning.message}", file=sys.stderr, flush=True)

    return result


def snapshot_schedule_detach_disk(
    project_id: str, zone: str, region: str, disk_name: str, schedule_name: str
) -> None:
    """
    Detaches a snapshot schedule from a specified disk in a given project and zone.
    Args:
        project_id (str): The ID of the Google Cloud project.
        zone (str): The zone where the disk is located.
        region (str): The location of the snapshot schedule
        disk_name (str): The name of the disk with the associated snapshot schedule
        schedule_name (str): The name of the snapshot schedule that you are removing from this disk
    Returns:
        None
    """
    disks_remove_request = compute_v1.DisksRemoveResourcePoliciesRequest(
        resource_policies=[f"regions/{region}/resourcePolicies/{schedule_name}"]
    )

    client = compute_v1.DisksClient()
    operation = client.remove_resource_policies(
        project=project_id,
        zone=zone,
        disk=disk_name,
        disks_remove_resource_policies_request_resource=disks_remove_request,
    )
    wait_for_extended_operation(operation, "Detaching snapshot schedule from disk")


# [END compute_snapshot_schedule_remove]

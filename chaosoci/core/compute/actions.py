# -*- coding: utf-8 -*-
from collections import defaultdict
from random import choice
from typing import Any, Dict, List

import oci
from chaoslib.exceptions import ActivityFailed, FailedActivity
from chaoslib.types import Configuration, Secrets
from oci.retry import DEFAULT_RETRY_STRATEGY

from chaosoci import oci_client
from chaosoci.types import OCIResponse

from logzero import logger

from oci.config import from_file
from oci.core import ComputeClient, ComputeManagementClient

from .common import (filter_instances,
                     get_instances, get_instance_pools, filter_instance_pools)

__all__ = ["stop_instance", "stop_random_instance", "stop_instances_in_compartment",
           "start_instance_pool", "start_all_instance_pools_in_compartment",
           "stop_instance_pool", "stop_all_instance_pools_in_compartment",
           "terminate_instance_pool", "terminate_all_instance_pools_in_compartment",
           "reset_instance_pool", "reset_all_instance_pools_in_compartment",
           "softreset_instance_pool", "softreset_all_instance_pools_in_compartment"]


# Compute Client Actions

def stop_instance(instance_id: str, force: bool = False,
                  configuration: Configuration = None,
                  secrets: Secrets = None) -> OCIResponse:
    """Stop a given Compute instance."""
    client = oci_client(ComputeClient, configuration, secrets,
                        skip_deserialization=True)

    action = "STOP" if force else "SOFTSTOP"
    ret = client.instance_action(instance_id=instance_id, action=action).data

    return ret


def stop_random_instance(filters: List[Dict[str, Any]],
                         compartment_id: str = None,
                         force: bool = False,
                         configuration: Configuration = None,
                         secrets: Secrets = None) -> OCIResponse:
    """
    Stop a a random compute instance within a given compartment.
    If filters are provided, the scope will be reduced to those instances
    matching the filters.

    Please refer to: https://oracle-cloud-infrastructure-python-sdk.readthedocs.io/en/latest/api/core/models/oci.core.models.Instance.html#oci.core.models.Instance
    for details on the available filters under the 'parameters' section.
    """  # noqa: E501
    client = oci_client(ComputeClient, configuration, secrets,
                        skip_deserialization=False)

    action = "STOP" if force else "SOFTSTOP"

    compartment_id = compartment_id or from_file().get('compartment')
    if compartment_id is None:
        raise ActivityFailed('We have not been able to find a compartment,'
                             ' without one, we cannot continue.')

    instances = get_instances(client, compartment_id)

    filters = filters or None
    if filters is not None:
        instances = filter_instances(instances, filters=filters)

    instance_id = choice(instances).id

    s_client = oci_client(ComputeClient, configuration, secrets,
                          skip_deserialization=True)
    ret = s_client.instance_action(instance_id=instance_id, action=action)

    return ret.data


def stop_instances_in_compartment(filters: List[Dict[str, Any]],
                                  instances_ids: List[str] = None,
                                  configuration: Configuration = None,
                                  compartment_id: str = None,
                                  secrets: Secrets = None) -> OCIResponse:
    """Stop the given OCI Compute instances,  If  only an Compartment is specified, all instances in
    that Compartment will be stopped. If you need more control, you can
    also provide a list of filters following the documentation.
    Please refer to: https://oracle-cloud-infrastructure-python-sdk.readthedocs.io/en/latest/api/core/models/oci.core.models.Instance.html#oci.core.models.Instance
    for details on the available filters under the 'parameters' section."""

    client = oci_client(ComputeClient, configuration, secrets,
                        skip_deserialization=True)
    if not instances_ids:
        logger.warning('Based on configuration provided I am going to '
                       'stop all instances in the Compartment %s! matching the filter criteria'
                       % compartment_id)

        compartment_id = compartment_id or from_file().get('compartment')
        instances = get_instances(client, compartment_id)

        filters = filters or None
        if filters is not None:
            instances_ids = filter_instances(instances, filters=filters)

        if not instances_ids:
            raise FailedActivity(
                'No instances found matching filters: %s' % str(filters))

        logger.debug('Instances in Compartment %s selected: %s}.' % (
            compartment_id, str(instances_ids)))

    stop_instances_ret = []

    for instance_id in instances_ids:
        logger.debug("Picked Compute Instance '{}' from Compartment '{}' to be stopped", instance_id, compartment_id)

        stop_instances_ret.append(stop_instance(instance_id, False))

    return stop_instances_ret


# Compute Client Management Actions

def stop_instance_pool(instance_pool_id: str,
                       configuration: Configuration = None,
                       secrets: Secrets = None) -> OCIResponse:
    """Stop the given OCI Compute instance pool."""

    client = oci_client(ComputeManagementClient, configuration, secrets,
                        skip_deserialization=True)

    stop_instance_pool_response = client.stop_instance_pool(
        instance_pool_id).data

    return stop_instance_pool_response


def stop_all_instance_pools_in_compartment(instance_pool_ids: List[str],
                                           filters: List[Dict[str, Any]],
                                           configuration: Configuration = None,
                                           compartment_id: str = None,
                                           secrets: Secrets = None) -> OCIResponse:
    """Stop the given OCI Compute instance pool. If you need more control, you can
    also provide a list of filters following the documentation.
    Please refer to: https://oracle-cloud-infrastructure-python-sdk.readthedocs.io/en/latest/api/core/models/oci.core.models.InstancePool.html#oci.core.models.Instance
    for details on the available filters under the 'parameters' section."""

    client = oci_client(ComputeManagementClient, configuration, secrets,
                        skip_deserialization=True)

    if not instance_pool_ids:
        logger.warning('Based on configuration provided I am going to '
                       'stop all Instance Pools in the Compartment %s! matching the filter criteria'
                       % compartment_id)

        compartment_id = compartment_id or from_file().get('compartment')
        instance_pools = get_instance_pools(client, compartment_id)

        filters = filters or None
        if filters is not None:
            instance_pool_ids = filter_instance_pools(instance_pools, filters=filters)

        if not instance_pool_ids:
            raise FailedActivity(
                'No Instance Pools found matching filters: %s' % str(filters))

        logger.debug('Instance Pools in Compartment %s selected: %s}.' % (
            compartment_id, str(instance_pool_ids)))

    stop_instance_pool_response = []

    for instance_pool_id in instance_pool_ids:
        logger.debug("Picked Compute Instance Pool '{}' from Compartment '{}' to be stopped", instance_pool_id,
                     compartment_id)

        stop_instance_pool_response = stop_instance_pool(
            instance_pool_id)

    return stop_instance_pool_response


def start_instance_pool(instance_pool_id: str,
                        configuration: Configuration = None,
                        secrets: Secrets = None) -> OCIResponse:
    """Start the given OCI Compute instances."""

    client = oci_client(ComputeManagementClient, configuration, secrets,
                        skip_deserialization=True)

    start_instance_pool_response = client.start_instance_pool(
        instance_pool_id).data

    return start_instance_pool_response


def start_all_instance_pools_in_compartment(instance_pool_ids: List[str],
                                            filters: List[Dict[str, Any]],
                                            configuration: Configuration = None,
                                            compartment_id: str = None,
                                            secrets: Secrets = None) -> OCIResponse:
    """Start the given OCI Compute instances,  If  only an Compartment is specified, all instances in
    that Compartment will be stopped. If you need more control, you can
    also provide a list of filters following the documentation.
    Please refer to: https://oracle-cloud-infrastructure-python-sdk.readthedocs.io/en/latest/api/core/models/oci.core.models.InstancePool.html#oci.core.models.Instance
    for details on the available filters under the 'parameters' section."""

    client = oci_client(ComputeManagementClient, configuration, secrets,
                        skip_deserialization=True)

    if not instance_pool_ids:
        logger.warning('Based on configuration provided I am going to '
                       'Start all Instance Pools in the Compartment %s! matching the filter criteria'
                       % compartment_id)

        compartment_id = compartment_id or from_file().get('compartment')
        instance_pools = get_instance_pools(client, compartment_id)

        filters = filters or None
        if filters is not None:
            instance_pool_ids = filter_instance_pools(instance_pools, filters=filters)

        if not instance_pool_ids:
            raise FailedActivity(
                'No Instance Pools found matching filters: %s' % str(filters))

        logger.debug('Instance Pools in Compartment %s selected: %s}.' % (
            compartment_id, str(instance_pool_ids)))

    start_instance_pool_response = []

    for instance_pool_id in instance_pool_ids:
        logger.debug("Picked Compute Instance Pool '{}' from Compartment '{}' to be started", instance_pool_id,
                     compartment_id)

        start_instance_pool_response = start_instance_pool(
            instance_pool_id)

    return start_instance_pool_response


def terminate_instance_pool(instance_pool_id: str,
                            configuration: Configuration = None,
                            secrets: Secrets = None) -> OCIResponse:
    """Terminate the given OCI Compute instances."""

    client = oci_client(ComputeManagementClient, configuration, secrets,
                        skip_deserialization=True)

    terminate_instance_pool_response = client.terminate_instance_pool(
        instance_pool_id).data

    return terminate_instance_pool_response


def terminate_all_instance_pools_in_compartment(instance_pool_ids: List[str],
                                                filters: List[Dict[str, Any]],
                                                configuration: Configuration = None,
                                                compartment_id: str = None,
                                                secrets: Secrets = None) -> OCIResponse:
    """Terminate the given OCI Compute instances,  If  only an Compartment is specified, all instances in
    that Compartment will be terminated. If you need more control, you can
    also provide a list of filters following the documentation.
    Please refer to: https://oracle-cloud-infrastructure-python-sdk.readthedocs.io/en/latest/api/core/models/oci.core.models.InstancePool.html#oci.core.models.Instance
    for details on the available filters under the 'parameters' section."""

    client = oci_client(ComputeManagementClient, configuration, secrets,
                        skip_deserialization=True)

    if not instance_pool_ids:
        logger.warning('Based on configuration provided I am going to '
                       'Terminate all Instance Pools in the Compartment %s! matching the filter criteria'
                       % compartment_id)

        compartment_id = compartment_id or from_file().get('compartment')
        instance_pools = get_instance_pools(client, compartment_id)

        filters = filters or None
        if filters is not None:
            instance_pool_ids = filter_instance_pools(instance_pools, filters=filters)

        if not instance_pool_ids:
            raise FailedActivity(
                'No Instance Pools found matching filters: %s' % str(filters))

        logger.debug('Instance Pools in Compartment %s selected: %s}.' % (
            compartment_id, str(instance_pool_ids)))

    terminate_instance_pool_response = []

    for instance_pool_id in instance_pool_ids:
        logger.debug("Picked Compute Instance Pool '{}' from Compartment '{}' to be terminated", instance_pool_id,
                     compartment_id)

        terminate_instance_pool_response = terminate_instance_pool(
            instance_pool_id)

    return terminate_instance_pool_response


def reset_instance_pool(instance_pool_id: str,
                        configuration: Configuration = None,
                        secrets: Secrets = None) -> OCIResponse:
    """Reset the given OCI Compute Instance Pools"""

    client = oci_client(ComputeManagementClient, configuration, secrets,
                        skip_deserialization=True)

    reset_instance_pool_response = client.reset_instance_pool(
        instance_pool_id).data

    return reset_instance_pool_response


def reset_all_instance_pools_in_compartment(instance_pool_ids: List[str],
                                            filters: List[Dict[str, Any]],
                                            configuration: Configuration = None,
                                            compartment_id: str = None,
                                            secrets: Secrets = None) -> OCIResponse:
    """Reset the given OCI Compute Instance Pools,  If  only an Compartment is specified, all Instance Pools in
    that Compartment will be Reset. If you need more control, you can
    also provide a list of filters following the documentation.
    Please refer to: https://oracle-cloud-infrastructure-python-sdk.readthedocs.io/en/latest/api/core/models/oci.core.models.InstancePool.html#oci.core.models.Instance
    for details on the available filters under the 'parameters' section."""

    client = oci_client(ComputeManagementClient, configuration, secrets,
                        skip_deserialization=True)

    if not instance_pool_ids:
        logger.warning('Based on configuration provided I am going to '
                       'Reset all Instance Pools in the Compartment %s! matching the filter criteria'
                       % compartment_id)

        compartment_id = compartment_id or from_file().get('compartment')
        instance_pools = get_instance_pools(client, compartment_id)

        filters = filters or None
        if filters is not None:
            instance_pool_ids = filter_instance_pools(instance_pools, filters=filters)

        if not instance_pool_ids:
            raise FailedActivity(
                'No instances found matching filters: %s' % str(filters))

        logger.debug('Instance Pools in Compartment %s selected: %s}.' % (
            compartment_id, str(instance_pool_ids)))

    reset_instance_pool_response = []

    for instance_pool_id in instance_pool_ids:
        logger.debug("Picked Compute Instance Pool '{}' from Compartment '{}' to be reset", instance_pool_id,
                     compartment_id)

        reset_instance_pool_response = reset_instance_pool(
            instance_pool_id)

    return reset_instance_pool_response


def softreset_instance_pool(instance_pool_id: str,
                            configuration: Configuration = None,
                            secrets: Secrets = None) -> OCIResponse:
    """Soft Reset the given OCI Compute instance pool."""

    client = oci_client(ComputeManagementClient, configuration, secrets,
                        skip_deserialization=True)

    softreset_instance_pool_response = client.softreset_instance_pool(
        instance_pool_id).data

    return softreset_instance_pool_response


def softreset_all_instance_pools_in_compartment(instance_pool_ids: List[str],
                                                filters: List[Dict[str, Any]],
                                                configuration: Configuration = None,
                                                compartment_id: str = None,
                                                secrets: Secrets = None) -> OCIResponse:
    """SoftReset the given OCI Compute Instance Pools,  If  only an Compartment is specified, all Instance Pools in
    that Compartment will be SoftReset. If you need more control, you can
    also provide a list of filters following the documentation.
    Please refer to: https://oracle-cloud-infrastructure-python-sdk.readthedocs.io/en/latest/api/core/models/oci.core.models.InstancePool.html#oci.core.models.Instance
    for details on the available filters under the 'parameters' section."""

    client = oci_client(ComputeManagementClient, configuration, secrets,
                        skip_deserialization=True)

    if not instance_pool_ids:
        logger.warning('Based on configuration provided I am going to '
                       'terminate all Instance Pools in the Compartment %s! matching the filter criteria'
                       % compartment_id)

        compartment_id = compartment_id or from_file().get('compartment')
        instance_pools = get_instance_pools(client, compartment_id)

        filters = filters or None
        if filters is not None:
            instance_pool_ids = filter_instance_pools(instance_pools, filters=filters)

        if not instance_pool_ids:
            raise FailedActivity(
                'No Instance Pools found matching filters: %s' % str(filters))

        logger.debug('Instance Pools in Compartment %s selected: %s}.' % (
            compartment_id, str(instance_pool_ids)))

    softreset_instance_pool_response = []

    for instance_pool_id in instance_pool_ids:
        logger.debug("Picked Compute Instance Pool '{}' from Compartment '{}' to be stopped", instance_pool_id,
                     compartment_id)

        softreset_instance_pool_response = softreset_instance_pool(
            instance_pool_id)

    return softreset_instance_pool_response

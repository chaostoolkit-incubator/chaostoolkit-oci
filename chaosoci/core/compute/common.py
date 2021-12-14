# -*- coding: utf-8 -*-
__all__ = ["get_instances", "filter_instances", "get_instance_pools", "filter_instance_pools"]

from typing import Any, Dict, List

from chaoslib.exceptions import ActivityFailed

from logzero import logger

from oci.core import ComputeClient, ComputeManagementClient
from oci.core.models import Instance, InstancePool


def get_instances(client: ComputeClient = None,
                  compartment_id: str = None) -> List[Instance]:
    """Return a complete, unfiltered list of instances in the compartment."""
    instances = []

    instances_raw = client.list_instances(compartment_id=compartment_id)
    instances.extend(instances_raw.data)
    while instances_raw.has_next_page:
        instances_raw = client.list_instances(compartment_id=compartment_id,
                                              page=instances_raw.next_page)
        instances.extend(instances_raw.data)

    return instances


def filter_instances(instances: List[Instance] = None,
                     filters: Dict[str, Any] = None) -> List[Instance]:
    """Return only those instances that match the filters provided."""
    instances = instances or None

    if instances is None:
        raise ActivityFailed('No instances were found.')

    filters_set = {x for x in filters}
    available_filters_set = {x for x in instances[0].attribute_map}

    # Partial filtering may return instances we do not want. We avoid it.
    if not filters_set.issubset(available_filters_set):
        raise ActivityFailed('Some of the chosen filters were not found,'
                             ' we cannot continue.')

    # Walk the instances and find those that match the given filters.
    filtered = []
    for instance in instances:
        sentinel = True
        for attr, val in filters.items():
            if val != getattr(instance, attr, None):
                sentinel = False
                break

        if sentinel:
            filtered.append(instance)

    return filtered


def get_instance_pools(client: ComputeManagementClient = None,
                       compartment_id: str = None) -> List[InstancePool]:
    """Return a complete, unfiltered list of Instance Pools in the compartment."""
    instance_pools = []

    instances_pool_raw = client.list_instance_pools(compartment_id=compartment_id)
    instance_pools.extend(instances_pool_raw.data)
    while instances_pool_raw.has_next_page:
        instances_pool_raw = client.list_instances(compartment_id=compartment_id,
                                                   page=instances_pool_raw.next_page)
        instance_pools.extend(instances_pool_raw.data)

    return instance_pools


def filter_instance_pools(instance_pools: List[InstancePool] = None,
                          filters: Dict[str, Any] = None) -> List[InstancePool]:
    """Return only those Instance Pools that match the filters provided."""
    instance_pools = instance_pools or None

    if instance_pools is None:
        raise ActivityFailed('No Instance Pools were found.')

    filters_set = {x for x in filters}
    available_filters_set = {x for x in instance_pools[0].attribute_map}

    # Partial filtering may return instances we do not want. We avoid it.
    if not filters_set.issubset(available_filters_set):
        raise ActivityFailed('Some of the chosen filters were not found,'
                             ' we cannot continue.')

    # Walk the instances and find those that match the given filters.
    filtered = []
    for instance_pool in instance_pools:
        sentinel = True
        for attr, val in filters.items():
            if val != getattr(instance_pool, attr, None):
                sentinel = False
                break

        if sentinel:
            filtered.append(instance_pool)

    return filtered

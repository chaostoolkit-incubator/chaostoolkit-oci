# -*- coding: utf-8 -*-
__all__ = ["get_instances", "filter_instances"]

from typing import Any, Dict, List

from chaoslib.exceptions import ActivityFailed

from logzero import logger

from oci.core import ComputeClient
from oci.core.models import Instance


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

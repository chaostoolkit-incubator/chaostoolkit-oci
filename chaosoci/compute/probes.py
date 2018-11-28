# -*- coding: utf-8 -*-
from typing import Any, List, Dict

from oci.core import ComputeClient
from oci.config import from_file

from chaoslib.types import Configuration, Secrets
from chaoslib.exceptions import ActivityFailed

from chaosoci import oci_client

__all__ = ['count_instances']


def count_instances(filters: List[Dict[str, Any]], compartment_id: str = None,
                    configuration: Configuration = None,
                    secrets: Secrets = None) -> int:
    """ Return the number of instances in accordance with the given filters.

        Please refer to: https://oracle-cloud-infrastructure-python-sdk.readthedocs.io/en/latest/api/core/models/oci.core.models.Instance.html#oci.core.models.Instance

        for details on the available filters under the 'parameters' section.
    """  # noqa: E501
    compartment_id = compartment_id or from_file().get('compartment')

    if compartment_id is None:
        raise ActivityFailed('We have not been able to find a compartment,'
                             ' without one, we cannot continue.')

    client = oci_client(ComputeClient, configuration, secrets,
                        skip_deserialization=False)

    filters = filters or None
    instances = _get_instances(client, compartment_id)

    if filters is not None:
        return len(_filter_instances(instances, filters=filters))

    return len(instances)


def _get_instances(client: ComputeClient = None,
                   compartment_id: str = None) -> List:
    """Return a complete, unfiltered list of instances in the compartment."""
    instances = []

    instances_raw = client.list_instances(compartment_id=compartment_id)
    instances.extend(instances_raw.data)
    while instances_raw.has_next_page:
        instances_raw = client.list_instances(compartment_id=compartment_id,
                                              page=instances_raw.next_page)
        instances.extend(instances_raw.data)

    return instances


def _filter_instances(instances: List = None,
                      filters: Dict[str, Any] = None) -> List:
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

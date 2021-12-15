# -*- coding: utf-8 -*-
from typing import Any, Dict, List

from chaoslib.exceptions import ActivityFailed
from chaoslib.types import Configuration, Secrets

from oci.config import from_file
from oci.core import ComputeClient, ComputeManagementClient

from chaosoci import oci_client

from .common import get_load_balancers, get_backend_sets, filter_load_balancers

__all__ = ['count_load_bal', 'count_backend_sets']


def count_load_bal(filters: List[Dict[str, Any]], compartment_id: str = None,
                   configuration: Configuration = None,
                   secrets: Secrets = None) -> int:
    """
    Return the number of instances in accordance with the given filters.

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
    instances = get_load_balancers(client, compartment_id)

    if filters is not None:
        return len(filter_load_balancers(instances, filters=filters))

    return len(instances)


def count_backend_sets(filters: List[Dict[str, Any]], loadbalancer_id: str = None,
                       configuration: Configuration = None,
                       secrets: Secrets = None) -> int:

    loadbalancer_id = loadbalancer_id or from_file().get('load_balancer')

    if loadbalancer_id is None:
        raise ActivityFailed('We have not been able to find a compartment,'
                             ' without one, we cannot continue.')

    client = oci_client(ComputeClient, configuration, secrets,
                        skip_deserialization=False)

    filters = filters or None
    backend_sets = get_backend_sets(client, loadbalancer_id)

    if filters is not None:
        return len(filter_load_balancers(backend_sets, filters=filters))

    return len(backend_sets)

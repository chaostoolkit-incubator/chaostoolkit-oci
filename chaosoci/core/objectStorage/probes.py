# -*- coding: utf-8 -*-
from typing import Any, Dict, List

from chaoslib.exceptions import ActivityFailed
from chaoslib.types import Configuration, Secrets

from oci.config import from_file
from oci.core import ComputeClient, ComputeManagementClient

from chaosoci import oci_client

__all__ = ['count_buckets', 'count_objects']

from chaosoci.core.objectStorage.common import get_buckets, filter_buckets, filter_obstore_objects, get_objects


def count_buckets(filters: List[Dict[str, Any]], compartment_id: str = None,
                    configuration: Configuration = None,
                    secrets: Secrets = None) -> int:
    """
    Return the number of buckets in accordance with the given filters.

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
    buckets = get_buckets(client, compartment_id)

    if filters is not None:
        return len(filter_buckets(buckets, filters=filters))

    return len(buckets)


def count_objects(filters: List[Dict[str, Any]], compartment_id: str = None,
                         configuration: Configuration = None,
                         secrets: Secrets = None) -> int:
    """
    Return the number of objects in accordance with the given filters.

    Please refer to: https://oracle-cloud-infrastructure-python-sdk.readthedocs.io/en/latest/api/core/models/oci.core.models.InstancePool.html#oci.core.models.Instance

    for details on the available filters under the 'parameters' section.
    """  # noqa: E501
    compartment_id = compartment_id or from_file().get('compartment')

    if compartment_id is None:
        raise ActivityFailed('We have not been able to find a compartment,'
                             ' without one, we cannot continue.')

    client = oci_client(ComputeManagementClient, configuration, secrets,
                        skip_deserialization=False)

    filters = filters or None
    objects = get_objects(client, compartment_id)

    if filters is not None:
        return len(filter_obstore_objects(objects, filters=filters))

    return len(objects)

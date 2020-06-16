# -*- coding: utf-8 -*-
from random import choice
from typing import Any, Dict, List

from chaoslib.exceptions import ActivityFailed
from chaoslib.types import Configuration, Secrets

from chaosoci import oci_client
from chaosoci.types import OCIResponse

from logzero import logger

from oci.config import from_file
from oci.core import ComputeClient

from .common import (filter_instances,
                     get_instances)

__all__ = ["stop_instance", "stop_random_instance"]


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

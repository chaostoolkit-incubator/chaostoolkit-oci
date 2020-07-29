# coding: utf-8
# Copyright 2020, Oracle Corporation and/or its affiliates.

__all__ = ['count_route_tables']

from typing import Any, Dict, List

from chaoslib.exceptions import ActivityFailed
from chaoslib.types import Configuration, Secrets

from chaosoci import oci_client

from logzero import logger

from oci.config import from_file
from oci.core import VirtualNetworkClient

from .common import (get_route_tables)

from .filters import (filter_route_tables)


def count_route_tables(filters: List[Dict[str, Any]],
                       compartment_id: str = None,
                       vcn_id: str = None,
                       configuration: Configuration = None,
                       secrets: Secrets = None) -> int:
    """
    Returns the number of Route Tables in the compartment 'compartment_id'
    and vcn 'vcn_id' and according to the given filters.

    Please refer to: https://oracle-cloud-infrastructure-python-sdk.readthedocs.io/en/latest/api/core/models/oci.core.models.RouteTable.html#

    for details on the available filters under the 'parameters' section.
    """  # noqa: E501
    compartment_id = compartment_id or from_file().get('compartment')

    if compartment_id is None:
        raise ActivityFailed('A valid compartment id is required.')

    client = oci_client(VirtualNetworkClient, configuration, secrets,
                        skip_deserialization=False)

    filters = filters or None
    route_tables = get_route_tables(client, compartment_id, vcn_id)
    if filters is not None:
        return len(filter_route_tables(route_tables, filters=filters))
    else:
        return len(route_tables)

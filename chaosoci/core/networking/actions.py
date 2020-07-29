# coding: utf-8
# Copyright 2020, Oracle Corporation and/or its affiliates.

__all__ = ["delete_route_table_by_id", "delete_route_table_by_filters"]

from random import choice
from typing import Any, Dict, List

from chaoslib.exceptions import ActivityFailed
from chaoslib.types import Configuration, Secrets

from chaosoci import oci_client
from chaosoci.types import OCIResponse
from chaosoci.util.constants import FILTER_ERR

from logzero import logger

from oci.config import from_file
from oci.core import VirtualNetworkClient

from .common import (get_route_tables)

from .filters import (filter_route_tables)


def delete_route_table_by_id(rt_id: str, force: bool = False,
                             configuration: Configuration = None,
                             secrets: Secrets = None) -> OCIResponse:
    """
    Deletes a given route table using the route table id.

    Parameters:
                Required:
                    - rt_id: the id of the route table
    """

    client = oci_client(VirtualNetworkClient, configuration, secrets,
                        skip_deserialization=True)
    if not rt_id:
        raise ActivityFailed('A route table id is required.')

    ret = client.delete_route_table(rt_id=rt_id).data
    logger.debug("Route table %s deleted", rt_id)
    return ret


def delete_route_table_by_filters(compartment_id: str, vcn_id: str,
                                  filters: Dict[str, Any], force: bool = False,
                                  configuration: Configuration = None,
                                  secrets: Secrets = None) -> OCIResponse:
    """
    Search for a route table in VCN using the specified filters and
    then deletes it.

    Parameters:
                Required:
                    - compartment_id: the compartment id of the VCN
                    - vcn_id: the id of the VCN
                    - filters: the set of filters for the route table.
    Please refer to
    https://oracle-cloud-infrastructure-python-sdk.readthedocs.io/en/latest/api/core/models/oci.core.models.RouteTable.html#
    for the route table filters.
    """

    client = oci_client(VirtualNetworkClient, configuration, secrets,
                        skip_deserialization=False)

    if compartment_id is None or vcn_id is None:
        raise ActivityFailed('A compartment id or vcn id is required.')
    else:
        unfiltered = get_route_tables(client, compartment_id, vcn_id)

        if filters is None:
            raise ActivityFailed(FILTER_ERR)
        else:
            filtered = filter_route_tables(unfiltered, filters)

            if (len(filtered) == 0):
                raise ActivityFailed(FILTER_ERR)
            else:
                ret = client.delete_route_table(filtered[0].id).data
                logger.debug("Route table %s deleted",
                             filtered[0].display_name)
                return ret

# coding: utf-8
# Copyright 2020, Oracle Corporation and/or its affiliates.

__all__ = ["get_route_table", "get_route_tables"]

from typing import Any, Dict, List

from chaoslib.exceptions import ActivityFailed

from logzero import logger

from oci.core import VirtualNetworkClient
from oci.core.models import (RouteRule,
                             RouteTable)


def get_route_tables(client: VirtualNetworkClient = None,
                     compartment_id: str = None,
                     vcn_id: str = None) -> List[RouteTable]:
    """
    Returns a complete, unfiltered list of route tables of a vcn in the
    compartment.
    """

    route_tables = []
    route_tables_raw = client.list_route_tables(compartment_id=compartment_id,
                                                vcn_id=vcn_id)
    route_tables.extend(route_tables_raw.data)
    while route_tables_raw.has_next_page:
        route_tables_raw = client.list_route_tables(
            compartment_id=compartment_id,
            vcn_id=vcn_id,
            page=route_tables_raw.next_page)
        route_tables.extend(route_tables_raw.data)

    return route_tables

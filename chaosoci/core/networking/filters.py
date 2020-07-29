# coding: utf-8
# Copyright 2020, Oracle Corporation and/or its affiliates.

__all__ = ["filter_route_tables"]

from typing import Any, Dict, List

from chaoslib.exceptions import ActivityFailed
from chaosoci.util.constants import FILTER_ERR

from logzero import logger

from oci.core import VirtualNetworkClient
from oci.core.models import (RouteRule,
                             RouteTable)


def filter_route_tables(route_tables: List[RouteTable] = None,
                        filters: Dict[str, Any] = None) -> List[RouteTable]:
    """
    Return only those route tables that match the filters provided.
    """
    route_tables = route_tables or None

    if route_tables is None:
        raise ActivityFailed('No route tables were found.')

    filters_set = {x for x in filters}

    available_filters_set = {x for x in route_tables[0].attribute_map}

    # Partial filtering may return route tables we do not want. We avoid it.
    if not filters_set.issubset(available_filters_set):
        raise ActivityFailed(FILTER_ERR)

    # Walk the route tables and find those that match the given filters.
    filtered = []
    for route_table in route_tables:
        sentinel = True
        for attr, val in filters.items():
            if val != getattr(route_table, attr, None):
                sentinel = False
                break

        if sentinel:
            filtered.append(route_table)

    return filtered

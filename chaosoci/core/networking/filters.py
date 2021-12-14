# coding: utf-8
# Copyright 2020, Oracle Corporation and/or its affiliates.

__all__ = ["filter_route_tables", "filter_nat_gateway", "filter_service_gateway", "filter_internet_gateway"]

from typing import Any, Dict, List

from chaoslib.exceptions import ActivityFailed
from chaosoci.util.constants import FILTER_ERR

from logzero import logger

from oci.core import VirtualNetworkClient
from oci.core.models import (RouteTable, NatGateway, InternetGateway, ServiceGateway)


def filter_route_tables(route_tables: List[RouteTable] = None,
                        filters: Dict[str, Any] = None) -> List[RouteTable]:
    """
    Return only those route tables that match the filters provided.
    """
    return filter_networks("Route Tables", route_tables, filters)


def filter_nat_gateway(nat_gateways: List[NatGateway] = None,
                       filters: Dict[str, Any] = None) -> List[NatGateway]:
    """
    Return only those network gateways that match the filters provided.
    """
    return filter_networks("Nat Gateway", nat_gateways, filters)


def filter_internet_gateway(internet_gateways: List[InternetGateway] = None,
                             filters: Dict[str, Any] = None) -> List[InternetGateway]:
    """
    Return only those internet gateways that match the filters provided.
    """
    return filter_networks("Internet Gateway", internet_gateways, filters)


def filter_service_gateway(service_gateways: List[ServiceGateway] = None,
                            filters: Dict[str, Any] = None) -> List[ServiceGateway]:
    """
    Return only those service gateways that match the filters provided.
    """

    return filter_networks("Service Gateway", service_gateways, filters)


def filter_networks(gateway_type, gateways, filters):
    gateways = gateways or None

    if gateways is None:
        raise ActivityFailed('No {} were found.', gateway_type)

    filters_set = {x for x in filters}

    available_filters_set = {x for x in gateways[0].attribute_map}

    # Partial filtering may return service gateways we do not want. We avoid it.
    if not filters_set.issubset(available_filters_set):
        raise ActivityFailed(FILTER_ERR)

    # Walk the service gateways and find those that match the given filters.
    filtered = []
    for service_gateway in gateways:
        sentinel = True
        for attr, val in filters.items():
            if val != getattr(service_gateway, attr, None):
                sentinel = False
                break

        if sentinel:
            filtered.append(service_gateway)

    return filtered

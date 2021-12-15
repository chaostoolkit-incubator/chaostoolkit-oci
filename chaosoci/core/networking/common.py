# coding: utf-8
# Copyright 2020, Oracle Corporation and/or its affiliates.

__all__ = ["get_nat_gateway", "get_route_tables", "get_internet_gateway", "get_service_gateway"]

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


def get_nat_gateway(client: VirtualNetworkClient = None,
                    compartment_id: str = None,
                    vcn_id: str = None) -> List[RouteTable]:
    """
    Returns a complete, unfiltered list of Nat Gateways of a vcn in the
    compartment.
    """
    nat_gateway = []
    nat_gateway_raw = client.list_nat_gateways(compartment_id=compartment_id,
                                               vcn_id=vcn_id)
    nat_gateway.extend(nat_gateway_raw.data)
    while nat_gateway_raw.has_next_page:
        nat_gateway_raw = client.list_nat_gateways(
            compartment_id=compartment_id,
            vcn_id=vcn_id,
            page=nat_gateway_raw.next_page)
        nat_gateway.extend(nat_gateway_raw.data)

    return nat_gateway


def get_internet_gateway(client: VirtualNetworkClient = None,
                         compartment_id: str = None,
                         vcn_id: str = None) -> List[RouteTable]:
    """
    Returns a complete, unfiltered list of Internet Gateways of a vcn in the
    compartment.
    """
    internet_gateway = []
    internet_gateway_raw = client.list_internet_gateways(compartment_id=compartment_id,
                                                         vcn_id=vcn_id)
    internet_gateway.extend(internet_gateway_raw.data)
    while internet_gateway_raw.has_next_page:
        internet_gateway_raw = client.list_internet_gateways(
            compartment_id=compartment_id,
            vcn_id=vcn_id,
            page=internet_gateway_raw.next_page)
        internet_gateway.extend(internet_gateway_raw.data)

    return internet_gateway


def get_service_gateway(client: VirtualNetworkClient = None,
                        compartment_id: str = None,
                        vcn_id: str = None) -> List[RouteTable]:
    """
    Returns a complete, unfiltered list of Service Gateways of a vcn in the
    compartment.
    """
    service_gateway = []
    service_gateway_raw = client.list_service_gateways(compartment_id=compartment_id,
                                                       vcn_id=vcn_id)
    service_gateway.extend(service_gateway_raw.data)
    while service_gateway_raw.has_next_page:
        service_gateway_raw = client.list_service_gateways(
            compartment_id=compartment_id,
            vcn_id=vcn_id,
            page=service_gateway_raw.next_page)
        service_gateway.extend(service_gateway_raw.data)

    return service_gateway

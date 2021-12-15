# coding: utf-8
# Copyright 2020, Oracle Corporation and/or its affiliates.

__all__ = ["delete_route_table_by_id", "delete_route_table_by_filters",
           "delete_nat_gateway_by_id", "delete_nat_gateway_by_filters",
           "delete_internet_gateway_by_id", "delete_internet_gateway_by_filters",
           "delete_service_gateway_by_id", "delete_service_gateway_by_filters"]

from random import choice
from typing import Any, Dict, List

from chaoslib.exceptions import ActivityFailed
from chaoslib.types import Configuration, Secrets
from oci.retry import DEFAULT_RETRY_STRATEGY

from chaosoci import oci_client
from chaosoci.types import OCIResponse
from chaosoci.util.constants import FILTER_ERR

from logzero import logger

from oci.config import from_file
from oci.core import VirtualNetworkClient

from .common import (get_route_tables, get_service_gateway, get_internet_gateway, get_nat_gateway)

from .filters import (filter_route_tables, filter_nat_gateway, filter_internet_gateway, filter_service_gateway)


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
                                  retry_strategy=None,
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

            if len(filtered) == 0:
                raise ActivityFailed(FILTER_ERR)
            else:
                if not retry_strategy:
                    retry_strategy = DEFAULT_RETRY_STRATEGY

                ret = client.delete_route_table(filtered[0].id, retry_strategy).data
                logger.debug("Route table %s deleted",
                             filtered[0].display_name)
                return ret


def delete_nat_gateway_by_id(nw_id: str, force: bool = False,
                             configuration: Configuration = None,
                             secrets: Secrets = None) -> OCIResponse:
    """
    Deletes a given Nat Gateway using the Nat Gateway id.

    Parameters:
                Required:
                    - nw_id: the id of the Nat Gateway
    """

    client = oci_client(VirtualNetworkClient, configuration, secrets,
                        skip_deserialization=True)
    if not nw_id:
        raise ActivityFailed('A Nat Gateway id is required.')

    ret = client.delete_nat_gateway(nw_id=nw_id).data
    logger.debug("Nat Gateway %s deleted", nw_id)
    return ret


def delete_nat_gateway_by_filters(compartment_id: str, vcn_id: str,
                                  filters: Dict[str, Any], force: bool = False,
                                  retry_strategy=None,
                                  configuration: Configuration = None,
                                  secrets: Secrets = None) -> OCIResponse:
    """
    Search for a Nat Gateway in VCN using the specified filters and
    then deletes it.

    Parameters:
                Required:
                    - compartment_id: the compartment id of the VCN
                    - vcn_id: the id of the VCN
                    - filters: the set of filters for the Nat Gateway.
    Please refer to
    https://oracle-cloud-infrastructure-python-sdk.readthedocs.io/en/latest/api/core/models/oci.core.models.NatGateway.html#
    for the Nat Gateway filters.
    """

    client = oci_client(VirtualNetworkClient, configuration, secrets,
                        skip_deserialization=False)

    if compartment_id is None or vcn_id is None:
        raise ActivityFailed('A compartment id or vcn id is required.')
    else:
        unfiltered = get_nat_gateway(client, compartment_id, vcn_id)

        if filters is None:
            raise ActivityFailed(FILTER_ERR)
        else:
            filtered = filter_nat_gateway(unfiltered, filters)

            if len(filtered) == 0:
                raise ActivityFailed(FILTER_ERR)
            else:
                if not retry_strategy:
                    retry_strategy = DEFAULT_RETRY_STRATEGY

                ret = client.delete_nat_gateway(filtered[0].id, retry_strategy).data
                logger.debug("Nat Gateway %s deleted",
                             filtered[0].display_name)
                return ret


def delete_internet_gateway_by_id(nw_id: str, force: bool = False,
                                  configuration: Configuration = None,
                                  secrets: Secrets = None) -> OCIResponse:
    """
    Deletes a given Internet Gateway using the Internet Gateway id.

    Parameters:
                Required:
                    - nw_id: the id of the Internet Gateway
    """

    client = oci_client(VirtualNetworkClient, configuration, secrets,
                        skip_deserialization=True)
    if not nw_id:
        raise ActivityFailed('A Internet Gateway id is required.')

    ret = client.delete_internet_gateway(ig_id=nw_id).data
    logger.debug("Internet Gateway %s deleted", nw_id)
    return ret


def delete_internet_gateway_by_filters(compartment_id: str, vcn_id: str,
                                       filters: Dict[str, Any], force: bool = False,
                                       retry_strategy=None,
                                       configuration: Configuration = None,
                                       secrets: Secrets = None) -> OCIResponse:
    """
    Search for a Internet Gateway in VCN using the specified filters and
    then deletes it.

    Parameters:
                Required:
                    - compartment_id: the compartment id of the VCN
                    - vcn_id: the id of the VCN
                    - filters: the set of filters for the Internet Gateway.
    Please refer to
    https://oracle-cloud-infrastructure-python-sdk.readthedocs.io/en/latest/api/core/models/oci.core.models.InternetGateway.html#
    for the Internet Gateway filters.
    """

    client = oci_client(VirtualNetworkClient, configuration, secrets,
                        skip_deserialization=False)

    if compartment_id is None or vcn_id is None:
        raise ActivityFailed('A compartment id or vcn id is required.')
    else:
        unfiltered = get_internet_gateway(client, compartment_id, vcn_id)

        if filters is None:
            raise ActivityFailed(FILTER_ERR)
        else:
            filtered = filter_internet_gateway(unfiltered, filters)

            if len(filtered) == 0:
                raise ActivityFailed(FILTER_ERR)
            else:
                if not retry_strategy:
                    retry_strategy = DEFAULT_RETRY_STRATEGY

            ret = client.delete_internet_gateway(filtered[0].id, retry_strategy).data
            logger.debug("Internet Gateway %s deleted",
                         filtered[0].display_name)
            return ret


def delete_service_gateway_by_id(nw_id: str, force: bool = False,
                                 configuration: Configuration = None,
                                 secrets: Secrets = None) -> OCIResponse:
    """
    Deletes a given Service Gateway using the Service Gateway id.

    Parameters:
                Required:
                    - nw_id: the id of the Service Gateway
    """

    client = oci_client(VirtualNetworkClient, configuration, secrets,
                        skip_deserialization=True)
    if not nw_id:
        raise ActivityFailed('A Service Gateway id is required.')

    ret = client.delete_service_gateway(sg_id=nw_id).data
    logger.debug("Service Gateway %s deleted", nw_id)
    return ret


def delete_service_gateway_by_filters(compartment_id: str, vcn_id: str,
                                      filters: Dict[str, Any], force: bool = False,
                                      retry_strategy=None,
                                      configuration: Configuration = None,
                                      secrets: Secrets = None) -> OCIResponse:
    """
    Search for a Service Gateway in VCN using the specified filters and
    then deletes it.

    Parameters:
                Required:
                    - compartment_id: the compartment id of the VCN
                    - vcn_id: the id of the VCN
                    - filters: the set of filters for the Service Gateway.
    Please refer to
    https://oracle-cloud-infrastructure-python-sdk.readthedocs.io/en/latest/api/core/models/oci.core.models.ServiceGateway.html#
    for the Service Gateway filters.
    """

    client = oci_client(VirtualNetworkClient, configuration, secrets,
                        skip_deserialization=False)

    if compartment_id is None or vcn_id is None:
        raise ActivityFailed('A compartment id or vcn id is required.')
    else:
        unfiltered = get_service_gateway(client, compartment_id, vcn_id)

        if filters is None:
            raise ActivityFailed(FILTER_ERR)
        else:
            filtered = filter_service_gateway(unfiltered, filters)

            if len(filtered) == 0:
                raise ActivityFailed(FILTER_ERR)
            else:
                if not retry_strategy:
                    retry_strategy = DEFAULT_RETRY_STRATEGY

            ret = client.delete_service_gateway(filtered[0].id, retry_strategy).data
            logger.debug("Service Gateway %s deleted",
                         filtered[0].display_name)
            return ret

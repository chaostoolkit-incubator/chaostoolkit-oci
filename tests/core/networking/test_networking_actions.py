# coding: utf-8
# Copyright 2020, Oracle Corporation and/or its affiliates.

import pytest

from unittest.mock import MagicMock, patch

from chaoslib.exceptions import ActivityFailed

from chaosoci.core.networking.actions import (delete_route_table_by_id, delete_route_table_by_filters,
                                              delete_nat_gateway_by_id, delete_nat_gateway_by_filters,
                                              delete_internet_gateway_by_id, delete_internet_gateway_by_filters,
                                              delete_service_gateway_by_id, delete_service_gateway_by_filters)
from chaosoci.core.networking.common import get_nat_gateway
from chaosoci.util.constants import FILTER_ERR
# FILTER_ERR = 'Some of the chosen filters were not found, we cannot continue.'

@patch('chaosoci.core.networking.actions.oci_client', autospec=True)
def test_delete_route_table_by_id(oci_client):
    network_client = MagicMock()
    oci_client.return_value = network_client
    rt_id = "ocid1.routetable.oc1.phx.aawnm2cdxq3naniep5dsiixtchqjuypcx7l7"
    rt_ids = [rt_id, ""]
    for id in rt_ids:
        if id == rt_id:
            delete_route_table_by_id(id)
            network_client.delete_route_table.assert_called_with(rt_id=id)
        else:
            with pytest.raises(ActivityFailed) as f:
                delete_route_table_by_id(id)
            assert 'A route table id is required.'

@patch('chaosoci.core.networking.actions.filter_route_tables', autospec=True)
@patch('chaosoci.core.networking.actions.get_route_tables', autospec=True)
@patch('chaosoci.core.networking.actions.oci_client', autospec=True)
def test_delete_route_table_by_filters(oci_client, get_route_tables,
                                       filter_route_tables):
    network_client = MagicMock()
    oci_client.return_value = network_client

    c_id = "ocid1.compartment.oc1..oadsocmof6r6ksovxmda44ikwxje7xxu"
    vcn_id = "ocid1.vcn.oc1.phx.amaaaaaapwxjxiqavc6zohqv4whr6y65qwwjcexhex"

    c_ids = [c_id, None]
    vcn_ids = [vcn_id, None]
    filters = [[{'display_name': 'random_name', 'region': 'uk-london-1'}],
               None]

    for c in c_ids:
        for v in vcn_ids:
            for f in filters:
                if c is None or v is None:
                    with pytest.raises(ActivityFailed) as c_failed:
                        delete_route_table_by_filters(c, v, f)
                    assert 'A compartment id or vcn id is required.'
                elif f is None:
                    with pytest.raises(ActivityFailed) as f_failed:
                        delete_route_table_by_filters(c, v, f)
                    assert FILTER_ERR
                else:
                    with pytest.raises(ActivityFailed) as rt_failed:
                        delete_route_table_by_filters(c, v, f)
                        network_client.delete_route_table.assert_called_with(
                            filter_route_tables(route_tables=get_route_tables(
                                oci_client, c, v), filters=f)[0].id)

@patch('chaosoci.core.networking.actions.oci_client', autospec=True)
def test_delete_nat_gateway_by_id(oci_client):
    network_client = MagicMock()
    oci_client.return_value = network_client
    nw_id = "ocid1.routetable.oc1.phx.aawnm2cdxq3naniep5dsiixtchqjuypcx7l7"
    nw_ids = [nw_id, ""]
    for id in nw_ids:
        if id == nw_id:
            delete_nat_gateway_by_id(id)
            network_client.delete_nat_gateway.assert_called_with(nw_id=id)
        else:
            with pytest.raises(ActivityFailed) as f:
                delete_route_table_by_id(id)
            assert 'A route table id is required.'

@patch('chaosoci.core.networking.actions.filter_nat_gateway', autospec=True)
@patch('chaosoci.core.networking.actions.get_nat_gateway', autospec=True)
@patch('chaosoci.core.networking.actions.oci_client', autospec=True)
def test_delete_nat_gateway_by_filters(oci_client, get_nat_gateway,
                                       filter_nat_gateway):
    network_client = MagicMock()
    oci_client.return_value = network_client

    c_id = "ocid1.compartment.oc1..oadsocmof6r6ksovxmda44ikwxje7xxu"
    vcn_id = "ocid1.vcn.oc1.phx.amaaaaaapwxjxiqavc6zohqv4whr6y65qwwjcexhex"

    c_ids = [c_id, None]
    vcn_ids = [vcn_id, None]
    filters = [[{'display_name': 'random_name', 'region': 'uk-london-1'}],
               None]

    for c in c_ids:
        for v in vcn_ids:
            for f in filters:
                if c is None or v is None:
                    with pytest.raises(ActivityFailed) as c_failed:
                        delete_nat_gateway_by_filters(c, v, f)
                    assert 'A compartment id or vcn id is required.'
                elif f is None:
                    with pytest.raises(ActivityFailed) as f_failed:
                        delete_nat_gateway_by_filters(c, v, f)
                    assert FILTER_ERR
                else:
                    with pytest.raises(ActivityFailed) as rt_failed:
                        delete_nat_gateway_by_filters(c, v, f)
                        network_client.delete_nat_gateway.assert_called_with(
                            filter_nat_gateway(route_tables=get_nat_gateway(
                                oci_client, c, v), filters=f)[0].id)

@patch('chaosoci.core.networking.actions.oci_client', autospec=True)
def test_delete_internet_gateway_by_id(oci_client):
    network_client = MagicMock()
    oci_client.return_value = network_client
    ig_id = "ocid1.routetable.oc1.phx.aawnm2cdxq3naniep5dsiixtchqjuypcx7l7"
    ig_ids = [ig_id, ""]
    for id in ig_ids:
        if id == ig_id:
            delete_internet_gateway_by_id(id)
            network_client.delete_internet_gateway.assert_called_with(ig_id=id)
        else:
            with pytest.raises(ActivityFailed) as f:
                delete_internet_gateway_by_id(id)
            assert 'A route table id is required.'

@patch('chaosoci.core.networking.actions.filter_internet_gateway', autospec=True)
@patch('chaosoci.core.networking.actions.get_internet_gateway', autospec=True)
@patch('chaosoci.core.networking.actions.oci_client', autospec=True)
def test_delete_internet_gateway_by_filters(oci_client, get_route_tables,
                                       filter_internet_gateway):
    network_client = MagicMock()
    oci_client.return_value = network_client

    c_id = "ocid1.compartment.oc1..oadsocmof6r6ksovxmda44ikwxje7xxu"
    vcn_id = "ocid1.vcn.oc1.phx.amaaaaaapwxjxiqavc6zohqv4whr6y65qwwjcexhex"

    c_ids = [c_id, None]
    vcn_ids = [vcn_id, None]
    filters = [[{'display_name': 'random_name', 'region': 'uk-london-1'}],
               None]

    for c in c_ids:
        for v in vcn_ids:
            for f in filters:
                if c is None or v is None:
                    with pytest.raises(ActivityFailed) as c_failed:
                        delete_internet_gateway_by_filters(c, v, f)
                    assert 'A compartment id or vcn id is required.'
                elif f is None:
                    with pytest.raises(ActivityFailed) as f_failed:
                        delete_internet_gateway_by_filters(c, v, f)
                    assert FILTER_ERR
                else:
                    with pytest.raises(ActivityFailed) as rt_failed:
                        delete_internet_gateway_by_filters(c, v, f)
                        network_client.delete_internet_gateway.assert_called_with(
                            filter_internet_gateway(route_tables=get_route_tables(
                                oci_client, c, v), filters=f)[0].id)

@patch('chaosoci.core.networking.actions.oci_client', autospec=True)
def test_delete_service_gateway_by_id(oci_client):
    network_client = MagicMock()
    oci_client.return_value = network_client
    sg_id = "ocid1.routetable.oc1.phx.aawnm2cdxq3naniep5dsiixtchqjuypcx7l7"
    sg_ids = [sg_id, ""]
    for id in sg_ids:
        if id == sg_id:
            delete_service_gateway_by_id(id)
            network_client.delete_service_gateway.assert_called_with(sg_id=id)
        else:
            with pytest.raises(ActivityFailed) as f:
                delete_service_gateway_by_id(id)
            assert 'A route table id is required.'

@patch('chaosoci.core.networking.actions.filter_service_gateway', autospec=True)
@patch('chaosoci.core.networking.actions.get_service_gateway', autospec=True)
@patch('chaosoci.core.networking.actions.oci_client', autospec=True)
def test_delete_service_gateway_by_filters(oci_client, get_service_gateway,
                                       filter_service_gateway):
    network_client = MagicMock()
    oci_client.return_value = network_client

    c_id = "ocid1.compartment.oc1..oadsocmof6r6ksovxmda44ikwxje7xxu"
    vcn_id = "ocid1.vcn.oc1.phx.amaaaaaapwxjxiqavc6zohqv4whr6y65qwwjcexhex"

    c_ids = [c_id, None]
    vcn_ids = [vcn_id, None]
    filters = [[{'display_name': 'random_name', 'region': 'uk-london-1'}],
               None]

    for c in c_ids:
        for v in vcn_ids:
            for f in filters:
                if c is None or v is None:
                    with pytest.raises(ActivityFailed) as c_failed:
                        delete_service_gateway_by_filters(c, v, f)
                    assert 'A compartment id or vcn id is required.'
                elif f is None:
                    with pytest.raises(ActivityFailed) as f_failed:
                        delete_service_gateway_by_filters(c, v, f)
                    assert FILTER_ERR
                else:
                    with pytest.raises(ActivityFailed) as rt_failed:
                        delete_service_gateway_by_filters(c, v, f)
                        network_client.delete_service_gateway.assert_called_with(
                            filter_service_gateway(get_service_gateway(
                                oci_client, c, v), filters=f)[0].id)

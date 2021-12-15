# coding: utf-8
# Copyright 2020, Oracle Corporation and/or its affiliates.

import pytest

from unittest import TestCase as T
from unittest.mock import MagicMock, patch

from chaoslib.exceptions import ActivityFailed

from chaosoci.core.networking.probes import (count_route_tables,
                                             filter_route_tables, count_nat_gateway, count_internet_gateway,
                                             count_service_gateway)

@patch('chaosoci.core.networking.probes.filter_route_tables', autospec=True)
@patch('chaosoci.core.networking.probes.get_route_tables', autospec=True)
@patch('chaosoci.core.networking.probes.oci_client', autospec=True)
def test_count_route_tables(oci_client, get_route_tables, filter_route_tables):
    network_client = MagicMock()
    oci_client.return_value = network_client

    c_id = "ocid1.compartment.oc1..oadsocmof6r6ksovxmda44ikwxje7xxu"
    filters = [{'display_name': 'random_name', 'region': 'uk-london-1'}]

    c_ids = [c_id]

    for id in c_ids:
        if id == c_id:
            count_route_tables(filters=filters, compartment_id=id)
            filter_route_tables.assert_called_with(
                get_route_tables(
                    oci_client, id), filters)
        else:
            with pytest.raises(ActivityFailed) as f:
                count_route_tables(filters=filters, compartment_id=id)
            assert 'A valid compartment id is required.'

@patch('chaosoci.core.networking.probes.filter_nat_gateway', autospec=True)
@patch('chaosoci.core.networking.probes.get_nat_gateway', autospec=True)
@patch('chaosoci.core.networking.probes.oci_client', autospec=True)
def test_count_nat_gateway(oci_client, get_nat_gateway, filter_nat_gateway):
    network_client = MagicMock()
    oci_client.return_value = network_client

    c_id = "ocid1.compartment.oc1..oadsocmof6r6ksovxmda44ikwxje7xxu"
    filters = [{'display_name': 'random_name', 'region': 'uk-london-1'}]

    c_ids = [c_id]

    for id in c_ids:
        if id == c_id:
            count_nat_gateway(filters=filters, compartment_id=id)
            filter_nat_gateway.assert_called_with(
                get_nat_gateway(
                    oci_client, id), filters)
        else:
            with pytest.raises(ActivityFailed) as f:
                count_nat_gateway(filters=filters, compartment_id=id)
            assert 'A valid compartment id is required.'

@patch('chaosoci.core.networking.probes.filter_internet_gateway', autospec=True)
@patch('chaosoci.core.networking.probes.get_internet_gateway', autospec=True)
@patch('chaosoci.core.networking.probes.oci_client', autospec=True)
def test_count_internet_gateway(oci_client, get_internet_gateway, filter_internet_gateway):
    network_client = MagicMock()
    oci_client.return_value = network_client

    c_id = "ocid1.compartment.oc1..oadsocmof6r6ksovxmda44ikwxje7xxu"
    filters = [{'display_name': 'random_name', 'region': 'uk-london-1'}]

    c_ids = [c_id]

    for id in c_ids:
        if id == c_id:
            count_internet_gateway(filters=filters, compartment_id=id)
            filter_internet_gateway.assert_called_with(
                get_internet_gateway(
                    oci_client, id), filters)
        else:
            with pytest.raises(ActivityFailed) as f:
                count_internet_gateway(filters=filters, compartment_id=id)
            assert 'A valid compartment id is required.'

@patch('chaosoci.core.networking.probes.filter_service_gateway', autospec=True)
@patch('chaosoci.core.networking.probes.get_service_gateway', autospec=True)
@patch('chaosoci.core.networking.probes.oci_client', autospec=True)
def test_count_service_gateway(oci_client, get_service_gateway, filter_service_gateway):
    network_client = MagicMock()
    oci_client.return_value = network_client

    c_id = "ocid1.compartment.oc1..oadsocmof6r6ksovxmda44ikwxje7xxu"
    filters = [{'display_name': 'random_name', 'region': 'uk-london-1'}]

    c_ids = [c_id]

    for id in c_ids:
        if id == c_id:
            count_service_gateway(filters=filters, compartment_id=id)
            filter_service_gateway.assert_called_with(
                get_service_gateway(
                    oci_client, id), filters)
        else:
            with pytest.raises(ActivityFailed) as f:
                count_service_gateway(filters=filters, compartment_id=id)
            assert 'A valid compartment id is required.'
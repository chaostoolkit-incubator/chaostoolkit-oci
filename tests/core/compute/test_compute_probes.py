# -*- coding: utf-8 -*-
from unittest import TestCase as T
from unittest.mock import MagicMock, patch

from chaosoci.core.compute.probes import count_instances


@patch('chaosoci.core.compute.probes.filter_instances', autospec=True)
@patch('chaosoci.core.compute.probes.get_instances', autospec=True)
@patch('chaosoci.core.compute.probes.oci_client', autospec=True)
def test_count_instances(oci_client, get_instances, filter_instances):
    compute_client = MagicMock()
    oci_client.return_value = compute_client

    c_id = "ocid1.compartment.oc1..oadsocmof6r6ksovxmda44ikwxje7xxu"
    filters = [{'display_name': 'random_name', 'region': 'uk-london-1'}]

    count_instances(filters=filters, compartment_id=c_id)
    filter_instances.assert_called_with(instances=get_instances(oci_client,
                                                                c_id),
                                        filters=filters)


@patch('chaosoci.core.compute.probes.filter_instances', autospec=True)
@patch('chaosoci.core.compute.probes.get_instances', autospec=True)
@patch('chaosoci.core.compute.probes.oci_client', autospec=True)
def test_count_instances_ret_int(oci_client, get_instances, filter_instances):
    compute_client = MagicMock()
    oci_client.return_value = compute_client

    filter_instances.return_value = ['one', 'two', 'three']
    c_id = "ocid1.compartment.oc1..oadsocmof6r6ksovxmda44ikwxje7xxu"
    filters = [{'display_name': 'random_name', 'region': 'uk-london-1'}]

    n = count_instances(filters=filters, compartment_id=c_id)
    T().assertEqual(n, 3)

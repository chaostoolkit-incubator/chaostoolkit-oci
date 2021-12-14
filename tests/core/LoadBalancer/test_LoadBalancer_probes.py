# -*- coding: utf-8 -*-
from unittest import TestCase as T
from unittest.mock import MagicMock, patch

from chaosoci.core.loadBalancer.probes import count_load_bal, count_backend_sets


@patch('chaosoci.core.loadBalancer.probes.filter_load_balancers', autospec=True)
@patch('chaosoci.core.loadBalancer.probes.get_load_balancers', autospec=True)
@patch('chaosoci.core.loadBalancer.probes.oci_client', autospec=True)
def test_count_load_bal(oci_client, get_load_balancers, filter_load_balancers):
    lb_client = MagicMock()
    oci_client.return_value = lb_client

    c_id = "ocid1.compartment.oc1..oadsocmof6r6ksovxmda44ikwxje7xxu"
    filters = [{'display_name': 'random_name', 'region': 'uk-london-1'}]

    count_load_bal(filters=filters, compartment_id=c_id)
    filter_load_balancers.assert_called_with(get_load_balancers(oci_client, c_id),
                                             filters)


@patch('chaosoci.core.loadBalancer.probes.filter_load_balancers', autospec=True)
@patch('chaosoci.core.loadBalancer.probes.get_backend_sets', autospec=True)
@patch('chaosoci.core.loadBalancer.probes.oci_client', autospec=True)
def test_count_count_backend_sets(oci_client, get_backend_sets, filter_load_balancers):
    lb_client = MagicMock()
    oci_client.return_value = lb_client

    lb_id = "lb-id"
    filters = [{'display_name': 'random_name', 'region': 'uk-london-1'}]

    count_backend_sets(filters=filters, loadbalancer_id=lb_id)
    filter_load_balancers.assert_called_with(get_backend_sets(oci_client, lb_id),
                                             filters)

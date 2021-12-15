# -*- coding: utf-8 -*-
from unittest import TestCase as T
from unittest.mock import MagicMock, patch

from chaosoci.core.objectStorage.probes import count_buckets, count_objects


@patch('chaosoci.core.objectStorage.probes.filter_buckets', autospec=True)
@patch('chaosoci.core.objectStorage.probes.get_buckets', autospec=True)
@patch('chaosoci.core.objectStorage.probes.oci_client', autospec=True)
def test_count_buckets(oci_client, get_buckets, filter_buckets):
    compute_client = MagicMock()
    oci_client.return_value = compute_client

    c_id = "ocid1.compartment.oc1..oadsocmof6r6ksovxmda44ikwxje7xxu"
    filters = [{'display_name': 'random_name', 'region': 'uk-london-1'}]

    count_buckets(filters=filters, compartment_id=c_id)
    filter_buckets.assert_called_with(get_buckets(oci_client, c_id),
                                      filters)


@patch('chaosoci.core.objectStorage.probes.filter_obstore_objects', autospec=True)
@patch('chaosoci.core.objectStorage.probes.get_objects', autospec=True)
@patch('chaosoci.core.objectStorage.probes.oci_client', autospec=True)
def test_count_objects(oci_client, get_objects, filter_obstore_objects):
    compute_client = MagicMock()
    oci_client.return_value = compute_client

    c_id = "ocid1.compartment.oc1..oadsocmof6r6ksovxmda44ikwxje7xxu"
    filters = [{'display_name': 'random_name', 'region': 'uk-london-1'}]

    count_objects(filters=filters, compartment_id=c_id)
    filter_obstore_objects.assert_called_with(get_objects(oci_client, c_id),
                                              filters)

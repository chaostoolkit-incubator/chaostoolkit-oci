# -*- coding: utf-8 -*-
from unittest.mock import MagicMock, patch

from chaosoci.core.compute.actions import stop_instance, stop_random_instance

@patch('chaosoci.core.compute.actions.oci_client', autospec=True)
def test_stop_instance(oci_client):
    compute_client = MagicMock()
    oci_client.return_value = compute_client
    inst_id = "i-1234567890abcdef0"
    action = "SOFTSTOP"
    stop_instance(inst_id, force=False)
    compute_client.instance_action.assert_called_with(instance_id=inst_id,
                                                      action=action)


@patch('chaosoci.core.compute.actions.filter_instances', autospec=True)
@patch('chaosoci.core.compute.actions.get_instances', autospec=True)
@patch('chaosoci.core.compute.actions.oci_client', autospec=True)
def test_filter_stop_random_instances(oci_client, get_instances,
                                      filter_instances):
    instance = MagicMock()
    instance.id = "i-1234567890abcdef0"

    c_id = "ocid1.compartment.oc1..oadsocmof6r6ksovxmda44ikwxje7xxu"
    filters = [{'display_name': 'random_name', 'region': 'uk-london-1'}]

    instances = [instance, instance, instance, instance]
    filter_instances.return_value = instances

    stop_random_instance(filters=filters, compartment_id=c_id)
    filter_instances.assert_called_with(instances=get_instances(oci_client,
                                                                c_id),
                                        filters=filters)


@patch('chaosoci.core.compute.actions.filter_instances', autospec=True)
@patch('chaosoci.core.compute.actions.get_instances', autospec=True)
@patch('chaosoci.core.compute.actions.oci_client', autospec=True)
def test_stop_random_instances(oci_client, get_instances, filter_instances):
    compute_client = MagicMock()
    instance = MagicMock()
    oci_client.return_value = compute_client

    c_id = "ocid1.compartment.oc1..oadsocmof6r6ksovxmda44ikwxje7xxu"
    filters = [{'display_name': 'random_name', 'region': 'uk-london-1'}]
    action = "SOFTSTOP"

    instance.id = "i-1234567890abcdef0"
    instances = [instance, instance, instance, instance]
    filter_instances.return_value = instances

    stop_random_instance(filters=filters, compartment_id=c_id)

    compute_client.instance_action.assert_called_with(instance_id=instance.id,
                                                      action=action)

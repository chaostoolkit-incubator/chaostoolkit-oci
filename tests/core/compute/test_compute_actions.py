# -*- coding: utf-8 -*-
from unittest.mock import MagicMock, patch

from chaosoci.core.compute.actions import stop_instance, stop_random_instance, stop_instances_in_compartment, \
    start_instance_pool, start_all_instance_pools_in_compartment, \
    stop_instance_pool, stop_all_instance_pools_in_compartment, \
    terminate_instance_pool, terminate_all_instance_pools_in_compartment, \
    reset_instance_pool, reset_all_instance_pools_in_compartment, \
    softreset_instance_pool, softreset_all_instance_pools_in_compartment


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


@patch('chaosoci.core.compute.actions.oci_client', autospec=True)
def test_start_instance_pool(oci_client):
    compute_client = MagicMock()
    oci_client.return_value = compute_client
    instance_pool_id = "i-1234567890abcdef0"
    start_instance_pool(instance_pool_id)
    compute_client.start_instance_pool.assert_called_with(instance_pool_id)


@patch('chaosoci.core.compute.actions.oci_client', autospec=True)
def test_stop_instance_pool(oci_client):
    compute_client = MagicMock()
    oci_client.return_value = compute_client
    inst_id = "i-1234567890abcdef0"
    stop_instance_pool(inst_id)
    compute_client.stop_instance_pool.assert_called_with(inst_id)


@patch('chaosoci.core.compute.actions.oci_client', autospec=True)
def test_terminate_instance_pool(oci_client):
    compute_client = MagicMock()
    oci_client.return_value = compute_client
    inst_id = "i-1234567890abcdef0"
    terminate_instance_pool(inst_id)
    compute_client.terminate_instance_pool.assert_called_with(inst_id)


@patch('chaosoci.core.compute.actions.oci_client', autospec=True)
def test_reset_instance_pool(oci_client):
    compute_client = MagicMock()
    oci_client.return_value = compute_client
    inst_id = "i-1234567890abcdef0"
    reset_instance_pool(inst_id)
    compute_client.reset_instance_pool.assert_called_with(inst_id)


@patch('chaosoci.core.compute.actions.oci_client', autospec=True)
def test_softreset_instance_pool(oci_client):
    compute_client = MagicMock()
    oci_client.return_value = compute_client
    inst_id = "i-1234567890abcdef0"
    softreset_instance_pool(inst_id)
    compute_client.softreset_instance_pool.assert_called_with(inst_id)


@patch('chaosoci.core.compute.actions.filter_instances', autospec=True)
@patch('chaosoci.core.compute.actions.get_instances', autospec=True)
@patch('chaosoci.core.compute.actions.oci_client', autospec=True)
def test_stop_instances_in_compartment(oci_client, get_instances, filter_instances):
    compute_client = MagicMock()
    instance = MagicMock()
    oci_client.return_value = compute_client

    c_id = "ocid1.compartment.oc1..oadsocmof6r6ksovxmda44ikwxje7xxu"
    filters = [{'display_name': 'random_name', 'region': 'uk-london-1'}]

    instance.id = "i-1234567890abcdef0"
    instances = [instance, instance, instance, instance]
    filter_instances.return_value = instances

    action = "SOFTSTOP"

    stop_random_instance(filters=filters, compartment_id=c_id)

    compute_client.instance_action.assert_called_with(instance_id=instance.id, action=action)


@patch('chaosoci.core.compute.actions.filter_instance_pools', autospec=True)
@patch('chaosoci.core.compute.actions.get_instance_pools', autospec=True)
@patch('chaosoci.core.compute.actions.oci_client', autospec=True)
def test_start_all_instance_pools_in_compartment(oci_client, get_instance_pools, filter_instance_pools):
    compute_client = MagicMock()
    instance = MagicMock()
    oci_client.return_value = compute_client

    c_id = "ocid1.compartment.oc1..oadsocmof6r6ksovxmda44ikwxje7xxu"
    filters = [{'display_name': 'random_name', 'region': 'uk-london-1'}]

    instance.id = "i-1234567890abcdef0"
    instances = [instance, instance, instance, instance]
    filter_instance_pools.return_value = instances

    start_all_instance_pools_in_compartment(instance_pool_ids=[], filters=filters, compartment_id=c_id)

    filter_instance_pools.assert_called_with(get_instance_pools(oci_client,
                                                                c_id),
                                             filters)


@patch('chaosoci.core.compute.actions.filter_instances', autospec=True)
@patch('chaosoci.core.compute.actions.get_instances', autospec=True)
@patch('chaosoci.core.compute.actions.oci_client', autospec=True)
def test_stop_instances_in_compartment(oci_client, get_instances, filter_instances):
    compute_client = MagicMock()
    instance = MagicMock()
    oci_client.return_value = compute_client

    c_id = "ocid1.compartment.oc1..oadsocmof6r6ksovxmda44ikwxje7xxu"
    filters = [{'display_name': 'random_name', 'region': 'uk-london-1'}]

    instance.id = "i-1234567890abcdef0"
    instances = [instance, instance, instance, instance]
    filter_instances.return_value = instances

    stop_instances_in_compartment(instances_ids=[], filters=filters, compartment_id=c_id)

    filter_instances.assert_called_with(instances=get_instances(oci_client,
                                                                c_id),
                                        filters=filters)


@patch('chaosoci.core.compute.actions.filter_instance_pools', autospec=True)
@patch('chaosoci.core.compute.actions.get_instance_pools', autospec=True)
@patch('chaosoci.core.compute.actions.oci_client', autospec=True)
def test_stop_all_instance_pools_in_compartment(oci_client, get_instance_pools, filter_instance_pools):
    compute_client = MagicMock()
    instance = MagicMock()
    oci_client.return_value = compute_client

    c_id = "ocid1.compartment.oc1..oadsocmof6r6ksovxmda44ikwxje7xxu"
    filters = [{'display_name': 'random_name', 'region': 'uk-london-1'}]

    instance.id = "i-1234567890abcdef0"
    instances = [instance, instance, instance, instance]
    filter_instance_pools.return_value = instances

    stop_all_instance_pools_in_compartment(instance_pool_ids=[], filters=filters, compartment_id=c_id)

    filter_instance_pools.assert_called_with(get_instance_pools(oci_client,
                                                                          c_id),
                                             filters)


@patch('chaosoci.core.compute.actions.filter_instance_pools', autospec=True)
@patch('chaosoci.core.compute.actions.get_instance_pools', autospec=True)
@patch('chaosoci.core.compute.actions.oci_client', autospec=True)
def test_terminate_all_instance_pools_in_compartment(oci_client, get_instance_pools, filter_instance_pools):
    compute_client = MagicMock()
    instance = MagicMock()
    oci_client.return_value = compute_client

    c_id = "ocid1.compartment.oc1..oadsocmof6r6ksovxmda44ikwxje7xxu"
    filters = [{'display_name': 'random_name', 'region': 'uk-london-1'}]

    instance.id = "i-1234567890abcdef0"
    instances = [instance, instance, instance, instance]
    filter_instance_pools.return_value = instances

    terminate_all_instance_pools_in_compartment(instance_pool_ids=[], filters=filters, compartment_id=c_id)

    filter_instance_pools.assert_called_with(get_instance_pools(oci_client,
                                                                          c_id),
                                             filters)


@patch('chaosoci.core.compute.actions.filter_instance_pools', autospec=True)
@patch('chaosoci.core.compute.actions.get_instance_pools', autospec=True)
@patch('chaosoci.core.compute.actions.oci_client', autospec=True)
def test_reset_all_instance_pools_in_compartment(oci_client, get_instance_pools, filter_instance_pools):
    compute_client = MagicMock()
    instance = MagicMock()
    oci_client.return_value = compute_client

    c_id = "ocid1.compartment.oc1..oadsocmof6r6ksovxmda44ikwxje7xxu"
    filters = [{'display_name': 'random_name', 'region': 'uk-london-1'}]

    instance.id = "i-1234567890abcdef0"
    instances = [instance, instance, instance, instance]
    filter_instance_pools.return_value = instances

    reset_all_instance_pools_in_compartment(instance_pool_ids=[], filters=filters, compartment_id=c_id)

    filter_instance_pools.assert_called_with(get_instance_pools(oci_client,
                                                                          c_id),
                                             filters)


@patch('chaosoci.core.compute.actions.filter_instance_pools', autospec=True)
@patch('chaosoci.core.compute.actions.get_instance_pools', autospec=True)
@patch('chaosoci.core.compute.actions.oci_client', autospec=True)
def test_softreset_all_instance_pools_in_compartment(oci_client, get_instance_pools, filter_instance_pools):
    compute_client = MagicMock()
    instance = MagicMock()
    oci_client.return_value = compute_client

    c_id = "ocid1.compartment.oc1..oadsocmof6r6ksovxmda44ikwxje7xxu"
    filters = [{'display_name': 'random_name', 'region': 'uk-london-1'}]

    instance.id = "i-1234567890abcdef0"
    instances = [instance, instance, instance, instance]
    filter_instance_pools.return_value = instances

    softreset_all_instance_pools_in_compartment(instance_pool_ids=[], filters=filters, compartment_id=c_id)

    filter_instance_pools.assert_called_with(get_instance_pools(oci_client,
                                                                          c_id),
                                             filters)

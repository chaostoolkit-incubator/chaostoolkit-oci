# -*- coding: utf-8 -*-
from unittest.mock import MagicMock, patch

from chaosoci.core.objectStorage.actions import delete_bucket, delete_buckets_in_compartment, \
    delete_object, delete_objects_in_compartment


@patch('chaosoci.core.objectStorage.actions.oci_client', autospec=True)
def test_delete_bucket(oci_client):
    objectStore_client = MagicMock()
    oci_client.return_value = objectStore_client
    namespace_name = "namespace_name"
    bucket_name = "bucket_name"
    delete_bucket(namespace_name, bucket_name)
    objectStore_client.delete_bucket.assert_called_with(namespace_name, bucket_name)


@patch('chaosoci.core.objectStorage.actions.filter_buckets', autospec=True)
@patch('chaosoci.core.objectStorage.actions.get_buckets', autospec=True)
@patch('chaosoci.core.objectStorage.actions.oci_client', autospec=True)
def test_delete_buckets_in_compartment(oci_client, get_buckets, filter_buckets):
    objectStore_client = MagicMock()
    bucket_mock = MagicMock()
    oci_client.return_value = objectStore_client

    c_id = "ocid1.compartment.oc1..oadsocmof6r6ksovxmda44ikwxje7xxu"
    filters = [{'display_name': 'random_name', 'region': 'uk-london-1'}]

    namespace_name = "namespace_name"

    bucket_mock = [bucket_mock, bucket_mock, bucket_mock, bucket_mock]
    filter_buckets.return_value = bucket_mock

    delete_buckets_in_compartment(filters=filters, namespace_name=namespace_name, bucket_names=[],
                                  compartment_id=c_id)

    filter_buckets.assert_called_with(buckets=get_buckets(oci_client,
                                                                c_id),
                                        filters=filters)


@patch('chaosoci.core.objectStorage.actions.oci_client', autospec=True)
def test_delete_object(oci_client):
    objectStore_client = MagicMock()
    oci_client.return_value = objectStore_client
    namespace_name = "namespace_name"
    bucket_name = "bucket_name"
    object_name = "object_name"
    delete_object(namespace_name, bucket_name, object_name)
    objectStore_client.delete_object.assert_called_with(namespace_name, bucket_name, object_name)


@patch('chaosoci.core.objectStorage.actions.filter_obstore_objects', autospec=True)
@patch('chaosoci.core.objectStorage.actions.get_objects', autospec=True)
@patch('chaosoci.core.objectStorage.actions.oci_client', autospec=True)
def test_delete_objects_in_compartment(oci_client, get_objects, filter_obstore_objects):
    objectStore_client = MagicMock()
    object_mock = MagicMock()
    oci_client.return_value = objectStore_client

    c_id = "ocid1.compartment.oc1..oadsocmof6r6ksovxmda44ikwxje7xxu"
    filters = [{'display_name': 'random_name', 'region': 'uk-london-1'}]

    namespace_name = "namespace_name"
    bucket_name = "bucket_name"

    object_mock = [object_mock, object_mock, object_mock, object_mock]
    filter_obstore_objects.return_value = object_mock

    delete_objects_in_compartment(filters=filters, namespace_name=namespace_name, bucket_name=bucket_name,
                                  object_names=[], compartment_id=c_id)

    filter_obstore_objects.assert_called_with(objects=get_objects(oci_client,
                                                                c_id),
                                        filters=filters)


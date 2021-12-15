# -*- coding: utf-8 -*-
from collections import defaultdict
from random import choice
from typing import Any, Dict, List

import oci
from chaoslib.exceptions import ActivityFailed, FailedActivity
from chaoslib.types import Configuration, Secrets
from oci.load_balancer import LoadBalancerClient
from oci.object_storage import ObjectStorageClient
from oci.retry import DEFAULT_RETRY_STRATEGY

from chaosoci import oci_client
from chaosoci.types import OCIResponse

from logzero import logger

from oci.config import from_file
from oci.core import ComputeClient, ComputeManagementClient

from .common import (get_buckets, filter_buckets, get_objects, filter_obstore_objects)

__all__ = ["delete_bucket", "delete_buckets_in_compartment",
           "delete_object", "delete_objects_in_compartment"]


# Compute Client Actions

def delete_bucket(namespace_name: str,
                  bucket_name: str,
                  configuration: Configuration = None,
                  secrets: Secrets = None) -> OCIResponse:
    """Delete a given Bucket"""

    client = oci_client(ObjectStorageClient, configuration, secrets,
                        skip_deserialization=True)
    delete_bucket_response = client.delete_bucket(namespace_name, bucket_name).data

    return delete_bucket_response


def delete_buckets_in_compartment(filters: List[Dict[str, Any]],
                                  namespace_name: str,
                                  bucket_names: List[str] = None,
                                  configuration: Configuration = None,
                                  compartment_id: str = None,
                                  secrets: Secrets = None) -> OCIResponse:
    """Delete the given OCI bucket,  If  only an Compartment is specified, all buckets in
    that Compartment will be deleted. If you need more control, you can
    also provide a list of filters following the documentation.
    Please refer to: https://oracle-cloud-infrastructure-python-sdk.readthedocs.io/en/latest/api/object_storage/models/oci.object_storage.models.Bucket.html#oci.object_storage.models.Bucket
    for details on the available filters under the 'parameters' section."""

    client = oci_client(ObjectStorageClient, configuration, secrets,
                        skip_deserialization=True)
    if not bucket_names:
        logger.warning('Based on configuration provided I am going to '
                       'delete all buckets in the Compartment %s! matching the filter criteria'
                       % compartment_id)

        compartment_id = compartment_id or from_file().get('compartment')
        bucket_names = get_buckets(client, compartment_id)

        filters = filters or None
        if filters is not None:
            bucket_names = filter_buckets(bucket_names, filters=filters)

        if not bucket_names:
            raise FailedActivity(
                'No buckets found matching filters: %s' % str(filters))

        logger.debug('Buckets in Compartment %s selected: %s}.' % (
            compartment_id, str(bucket_names)))

    delete_bucket_response = []

    for bucket_name in bucket_names:
        logger.debug("Picked bucket '{}' from Compartment '{}' to be deleted", bucket_name, compartment_id)

        delete_bucket_response.append(delete_bucket(namespace_name, bucket_name))

    return delete_bucket_response


def delete_object(namespace_name: str,
                  bucket_name: str,
                  object_name: str,
                  configuration: Configuration = None,
                  secrets: Secrets = None) -> OCIResponse:
    """Delete a given object"""

    client = oci_client(ObjectStorageClient, configuration, secrets,
                        skip_deserialization=True)
    delete_object_response = client.delete_object(namespace_name, bucket_name, object_name).data

    return delete_object_response


def delete_objects_in_compartment(filters: List[Dict[str, Any]],
                                  namespace_name: str,
                                  bucket_name: str,
                                  object_names: List[str] = None,
                                  configuration: Configuration = None,
                                  compartment_id: str = None,
                                  secrets: Secrets = None) -> List[Dict[str, Any]]:
    """Delete the given OCI Object,  If  only an Compartment is specified, all objects in
    that Compartment will be deleted. If you need more control, you can
    also provide a list of filters following the documentation.
    Please refer to: https://oracle-cloud-infrastructure-python-sdk.readthedocs.io/en/latest/api/object_storage/models/oci.object_storage.models.ObjectSummary.html#oci.object_storage.models.ObjectSummary
    for details on the available filters under the 'parameters' section."""

    client = oci_client(ObjectStorageClient, configuration, secrets,
                        skip_deserialization=True)
    if not object_names:
        logger.warning('Based on configuration provided I am going to '
                       'delete all objects in the Compartment %s! matching the filter criteria'
                       % compartment_id)

        compartment_id = compartment_id or from_file().get('compartment')
        object_names = get_objects(client, compartment_id)

        filters = filters or None
        if filters is not None:
            object_names = filter_obstore_objects(object_names, filters=filters)

        if not object_names:
            raise FailedActivity(
                'No objects found matching filters: %s' % str(filters))

        logger.debug('Objects in Compartment %s selected: %s}.' % (
            compartment_id, str(object_names)))

    delete_object_response = []

    for object_name in object_names:
        logger.debug("Picked Object '{}' from Compartment '{}' to be deleted", bucket_name, compartment_id)

        delete_object_response.append(delete_object(namespace_name, bucket_name, object_name))

    return delete_object_response

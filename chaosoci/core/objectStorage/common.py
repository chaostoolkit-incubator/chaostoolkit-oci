# -*- coding: utf-8 -*-
__all__ = ["get_buckets", "filter_buckets", "get_objects", "filter_obstore_objects"]

from typing import Any, Dict, List

from chaoslib.exceptions import ActivityFailed

from logzero import logger

from oci.core import ComputeClient, ComputeManagementClient
from oci.object_storage.models import Bucket, ObjectSummary

from oci.object_storage import ObjectStorageClient


def get_buckets(client: ObjectStorageClient = None,
                compartment_id: str = None) -> List[Bucket]:
    """Return a complete, unfiltered list of buckets in the compartment."""
    buckets = []

    buckets_raw = client.list_buckets(compartment_id=compartment_id)
    buckets.extend(buckets_raw.data)
    while buckets_raw.has_next_page:
        buckets_raw = client.list_buckets(compartment_id=compartment_id,
                                          page=buckets_raw.next_page)
        buckets.extend(buckets_raw.data)

    return buckets


def filter_buckets(buckets: List[Bucket] = None,
                     filters: Dict[str, Any] = None) -> List[Bucket]:
    """Return only those buckets that match the filters provided."""
    buckets = buckets or None

    if buckets is None:
        raise ActivityFailed('No buckets were found.')

    filters_set = {x for x in filters}
    available_filters_set = {x for x in buckets[0].attribute_map}

    # Partial filtering may return buckets we do not want. We avoid it.
    if not filters_set.issubset(available_filters_set):
        raise ActivityFailed('Some of the chosen filters were not found,'
                             ' we cannot continue.')

    # Walk the buckets and find those that match the given filters.
    filtered = []
    for bucket in buckets:
        sentinel = True
        for attr, val in filters.items():
            if val != getattr(bucket, attr, None):
                sentinel = False
                break

        if sentinel:
            filtered.append(bucket)

    return filtered


def get_objects(client: ObjectStorageClient = None,
                compartment_id: str = None) -> List[ObjectSummary]:
    """Return a complete, unfiltered list of instances in the compartment."""
    objects = []

    objects_raw = client.list_objects(compartment_id=compartment_id)
    objects.extend(objects_raw.data)
    while objects_raw.has_next_page:
        objects_raw = client.list_objects(compartment_id=compartment_id,
                                          page=objects_raw.next_page)
        objects.extend(objects_raw.data)

    return objects


def filter_obstore_objects(objects: List[ObjectSummary] = None,
                     filters: Dict[str, Any] = None) -> List[ObjectSummary]:
    """Return only those instances that match the filters provided."""
    objects = objects or None

    if objects is None:
        raise ActivityFailed('No instances were found.')

    filters_set = {x for x in filters}
    available_filters_set = {x for x in objects[0].attribute_map}

    # Partial filtering may return instances we do not want. We avoid it.
    if not filters_set.issubset(available_filters_set):
        raise ActivityFailed('Some of the chosen filters were not found,'
                             ' we cannot continue.')

    # Walk the instances and find those that match the given filters.
    filtered = []
    for bucket in objects:
        sentinel = True
        for attr, val in filters.items():
            if val != getattr(bucket, attr, None):
                sentinel = False
                break

        if sentinel:
            filtered.append(bucket)

    return filtered
# -*- coding: utf-8 -*-
__all__ = ["get_load_balancers", "filter_load_balancers", "get_backend_sets"]

from typing import Any, Dict, List

from chaoslib.exceptions import ActivityFailed

from logzero import logger

from oci.core import ComputeClient, ComputeManagementClient
from oci.core.models import Instance, InstancePool
from oci.load_balancer import LoadBalancerClient
from oci.load_balancer.models import LoadBalancer


def get_load_balancers(client: LoadBalancerClient = None,
                       compartment_id: str = None) -> List[Instance]:
    """Return a complete, unfiltered list of instances in the compartment."""
    load_bals = []

    load_bals_raw = client.list_load_balancers(compartment_id=compartment_id)
    load_bals.extend(load_bals_raw.data)
    while load_bals_raw.has_next_page:
        load_bals_raw = client.list_load_balancers(compartment_id=compartment_id,
                                                   page=load_bals_raw.next_page)
        load_bals.extend(load_bals_raw.data)

    return load_bals


def filter_load_balancers(load_bals: List[LoadBalancer] = None,
                          filters: Dict[str, Any] = None) -> List[LoadBalancer]:
    """Return only those load_bals that match the filters provided."""
    load_bals = load_bals or None

    if load_bals is None:
        raise ActivityFailed('No load_bals were found.')

    filters_set = {x for x in filters}
    available_filters_set = {x for x in load_bals[0].attribute_map}

    # Partial filtering may return load_bals we do not want. We avoid it.
    if not filters_set.issubset(available_filters_set):
        raise ActivityFailed('Some of the chosen filters were not found,'
                             ' we cannot continue.')

    # Walk the load_bals and find those that match the given filters.
    filtered = []
    for load_bal in load_bals:
        sentinel = True
        for attr, val in filters.items():
            if val != getattr(load_bal, attr, None):
                sentinel = False
                break

        if sentinel:
            filtered.append(load_bal)

    return filtered


def get_backend_sets(client: LoadBalancerClient = None,
                     loadbalancer_id: str = None) -> List[Instance]:
    """Return a complete, unfiltered list of instances in the compartment."""
    backend_set = []

    backend_set_raw = client.list_backend_sets(load_balancer_id=loadbalancer_id)
    backend_set.extend(backend_set_raw.data)
    while backend_set_raw.has_next_page:
        backend_set_raw = client.list_backend_sets(load_balancer_id=loadbalancer_id,
                                                   page=backend_set_raw.next_page)
        backend_set.extend(backend_set_raw.data)

    return backend_set

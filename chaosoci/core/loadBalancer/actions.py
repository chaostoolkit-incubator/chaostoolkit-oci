# -*- coding: utf-8 -*-

from chaoslib.types import Configuration, Secrets
from oci.load_balancer import LoadBalancerClient

from chaosoci import oci_client
from chaosoci.types import OCIResponse

__all__ = ["delete_backend_server", "delete_backend_set",
           "delete_hostname", "delete_listener",
           "delete_load_balancer", "delete_routing_policy",
           "delete_path_route_set"]


# Compute Client Actions

def delete_backend_server(load_balancer_id: str,
                          backend_set_name: str,
                          backend_name: str,
                          configuration: Configuration = None,
                          secrets: Secrets = None) -> OCIResponse:
    """Delete a given backend server"""

    client = oci_client(LoadBalancerClient, configuration, secrets,
                        skip_deserialization=True)
    delete_backend_response = client.delete_backend(load_balancer_id, backend_name, backend_set_name).data

    return delete_backend_response


def delete_backend_set(load_balancer_id: str,
                       backend_set_name: str,
                       configuration: Configuration = None,
                       secrets: Secrets = None) -> OCIResponse:
    """Delete a given backend set"""
    client = oci_client(LoadBalancerClient, configuration, secrets,
                        skip_deserialization=False)

    delete_backend_set_response = client.delete_backend_set(load_balancer_id, backend_set_name).data

    return delete_backend_set_response


# Compute Client Management Actions

def delete_hostname(load_balancer_id: str,
                    load_balancer_name: str,
                    configuration: Configuration = None,
                    secrets: Secrets = None) -> OCIResponse:
    """Delete a given hostname"""

    client = oci_client(LoadBalancerClient, configuration, secrets,
                        skip_deserialization=True)

    delete_hostname_response = client.delete_hostname(load_balancer_id, load_balancer_name).data

    return delete_hostname_response


def delete_listener(listener_id: str,
                    listener_name: str,
                    configuration: Configuration = None,
                    secrets: Secrets = None) -> OCIResponse:
    """Delete a given LB Listener"""

    client = oci_client(LoadBalancerClient, configuration, secrets,
                        skip_deserialization=True)

    delete_listener_response = client.delete_listener(listener_id, listener_name).data

    return delete_listener_response


def delete_load_balancer(load_balancer_id: str,
                         configuration: Configuration = None,
                         secrets: Secrets = None) -> OCIResponse:
    """Delete a given Load Balancer"""

    client = oci_client(LoadBalancerClient, configuration, secrets,
                        skip_deserialization=True)

    delete_load_balancer_response = client.delete_load_balancer(load_balancer_id).data

    return delete_load_balancer_response


def delete_path_route_set(load_balancer_id: str,
                          path_route_set_name: str,
                          configuration: Configuration = None,
                          secrets: Secrets = None) -> OCIResponse:
    """Delete a given set path route"""

    client = oci_client(LoadBalancerClient, configuration, secrets,
                        skip_deserialization=True)

    delete_path_route_set_response = client.delete_path_route_set(load_balancer_id, path_route_set_name).data

    return delete_path_route_set_response


def delete_routing_policy(load_balancer_id: str,
                          routing_policy_name: str,
                          configuration: Configuration = None,
                          secrets: Secrets = None) -> OCIResponse:
    """Delete a given routing policy"""

    client = oci_client(LoadBalancerClient, configuration, secrets,
                        skip_deserialization=True)

    delete_routing_policy_response = client.delete_routing_policy(load_balancer_id, routing_policy_name).data

    return delete_routing_policy_response

# -*- coding: utf-8 -*-
from unittest.mock import MagicMock, patch

from chaosoci.core.loadBalancer.actions import delete_backend_server, delete_backend_set, \
    delete_hostname, delete_listener, \
    delete_load_balancer, delete_routing_policy, \
    delete_path_route_set


@patch('chaosoci.core.loadBalancer.actions.oci_client', autospec=True)
def test_delete_backend_server(oci_client):
    lb_client = MagicMock()
    oci_client.return_value = lb_client
    load_balancer_id = "lb-id"
    backend_set_name = "bes-name"
    backend_name = "be-name"
    delete_backend_server(load_balancer_id, backend_set_name, backend_name)
    lb_client.delete_backend.assert_called_with(load_balancer_id, backend_name, backend_set_name)


@patch('chaosoci.core.loadBalancer.actions.oci_client', autospec=True)
def test_delete_backend_set(oci_client):
    lb_client = MagicMock()
    oci_client.return_value = lb_client
    load_balancer_id = "lb-id"
    backend_set_name = "bes-name"
    delete_backend_set(load_balancer_id, backend_set_name)
    lb_client.delete_backend_set.assert_called_with(load_balancer_id, backend_set_name)


@patch('chaosoci.core.loadBalancer.actions.oci_client', autospec=True)
def test_delete_hostname(oci_client):
    lb_client = MagicMock()
    oci_client.return_value = lb_client
    load_balancer_id = "lb-id"
    load_balancer_name = "bes-name"
    delete_hostname(load_balancer_id, load_balancer_name)
    lb_client.delete_hostname.assert_called_with(load_balancer_id, load_balancer_name)


@patch('chaosoci.core.loadBalancer.actions.oci_client', autospec=True)
def test_delete_listener(oci_client):
    lb_client = MagicMock()
    oci_client.return_value = lb_client
    listener_id = "lb-id"
    listener_name = "bes-name"
    delete_listener(listener_id, listener_name)
    lb_client.delete_listener.assert_called_with(listener_id, listener_name)


@patch('chaosoci.core.loadBalancer.actions.oci_client', autospec=True)
def test_delete_load_balancer(oci_client):
    lb_client = MagicMock()
    oci_client.return_value = lb_client
    load_balancer_id = "lb-id"
    delete_load_balancer(load_balancer_id)
    lb_client.delete_load_balancer.assert_called_with(load_balancer_id)


@patch('chaosoci.core.loadBalancer.actions.oci_client', autospec=True)
def test_delete_path_route_set(oci_client):
    lb_client = MagicMock()
    oci_client.return_value = lb_client
    load_balancer_id = "lb-id"
    path_route_set_name = "bes-name"
    delete_path_route_set(load_balancer_id, path_route_set_name)
    lb_client.delete_path_route_set.assert_called_with(load_balancer_id, path_route_set_name)


@patch('chaosoci.core.loadBalancer.actions.oci_client', autospec=True)
def test_delete_routing_policy(oci_client):
    lb_client = MagicMock()
    oci_client.return_value = lb_client
    load_balancer_id = "lb-id"
    routing_policy_name = "bes-name"
    delete_routing_policy(load_balancer_id, routing_policy_name)
    lb_client.delete_routing_policy.assert_called_with(load_balancer_id, routing_policy_name)

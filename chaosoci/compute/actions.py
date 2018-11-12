# -*- coding: utf-8 -*-
from oci.core import ComputeClient

from chaoslib.types import Configuration, Secrets

from chaosoci import oci_client
from chaosoci.types import OCIResponse


__all__ = ["stop_instance"]


def stop_instance(instance_id: str, force: bool = False,
                  configuration: Configuration = None,
                  secrets: Secrets = None) -> OCIResponse:
    """Stop a given Compute instance."""
    action = "SOFTSTOP"
    client = oci_client(ComputeClient, configuration, secrets)

    if force is True:
        action = "STOP"

    ret = client.instance_action(instance_id=instance_id, action=action)

    return ret.data

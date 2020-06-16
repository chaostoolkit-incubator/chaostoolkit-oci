# -*- coding: utf-8 -*-
from typing import List

from oci.config import from_file, validate_config

from chaoslib.discovery.discover import (discover_actions, discover_probes,
                                         initialize_discovery_result)
from chaoslib.types import (Discovery, DiscoveredActivities,
                            DiscoveredSystemInfo, Configuration, Secrets)
from logzero import logger

__version__ = '0.2.0'
__all__ = ["__version__", "discover", "oci_client"]


def oci_client(resource_name: str, configuration: Configuration = None,
               secrets: Secrets = None, skip_deserialization: bool = False):
    """Create an oci configuration object"""

    # As secrets is attached to configuration in OCI, it is not used.
    configuration = configuration or {}

    if not configuration.get('tenancy'):
        configuration = from_file()
    else:
        validate_config(configuration)

    return resource_name(configuration,
                         skip_deserialization=skip_deserialization)


def discover(discover_system: bool = True) -> Discovery:
    """
    Discover OCI capabilities from this extension as well, if an OCI
    configuration is available, some information about the OCI environment.
    """
    logger.info("Discovering capabilities from chaostoolkit-oci")

    discovery = initialize_discovery_result(
        "chaostoolkit-oci", __version__, "oci")
    discovery["activities"].extend(load_exported_activities())
    if discover_system:
        discovery["system"] = explore_oci_system()

    return discovery


###############################################################################
# Private functions
###############################################################################
def load_exported_activities() -> List[DiscoveredActivities]:
    """
    Extract metadata from actions and probes exposed by this extension.
    """
    activities = []
    activities.extend(discover_actions("chaosoci.core.compute.actions"))
    activities.extend(discover_probes("chaosoci.core.compute.probes"))
    return activities


def explore_oci_system() -> DiscoveredSystemInfo:
    """
    Fetch information from the current OCI context.
    """
    logger.info("Discovering OCI system")
    # TBD
    return {}

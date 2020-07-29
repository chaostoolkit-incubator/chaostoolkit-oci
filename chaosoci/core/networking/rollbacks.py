# coding: utf-8
# Copyright 2020, Oracle Corporation and/or its affiliates.

__all__ = ["delete_nat_rollback"]

from random import choice
from typing import Any, Dict, List

from chaoslib.exceptions import ActivityFailed
from chaoslib.types import Configuration, Secrets

from chaosoci import oci_client
from chaosoci.types import OCIResponse

from logzero import logger

from oci.config import from_file
from oci.core import VirtualNetworkClient

from .common import (get_route_tables)

from .filters import (filter_route_tables)

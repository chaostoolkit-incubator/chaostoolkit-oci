# -*- coding: utf-8 -*-
from typing import Any, Dict
from oci.core.models.instance import Instance

__all__ = ["OCIResponse", "OCIInstance"]

# really dependent on the type of resource called
OCIResponse = Dict[str, Any]
OCIInstance = Instance

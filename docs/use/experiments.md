# Using chaostoolkit-oci

### Creating experiments

To use the probes and actions from this package, add the following to your
experiment file:

```json
{
    "type": "action",
    "name": "stop-a-compute-instance",
    "provider": {
        "type": "python",
        "module": "chaosoci.core.compute.actions",
        "func": "stop_instance",
        "arguments": {
            "instance_id": "ocid1.instance.oc1.uk-london-1.abwgiljr4hngf7ktirgpp4ebl3w7fdarvhe6if4tu4r7y4fh3tsde7vbm5lq"
        }
    }
}
```

That's it!

Now, let us say we only want an action to be executed after probing that a given value is within 
a desired threshold; simple enough, we need to add a probe to our experiment, as follows:

```
"type": "probe",
"name": "count-the-number-of-instances",
"tolerance": [2, 10],
"provider": {
    "type": "python",
    "module": "chaosoci.core.compute.probes",
    "func": "count_instances",
    "arguments": {
	"filters": {
	    "region": "uk-london-1",
	    "lifecycle_state": "RUNNING"
	}
    }
}
```

For a list of available filters please refer to: [oci.core.models.Instance](https://oracle-cloud-infrastructure-python-sdk.readthedocs.io/en/latest/api/core/models/oci.core.models.Instance.html#oci.core.models.Instance).

Please explore the code to see existing probes and actions.

### Running experiments

```
chaos run experiment.json
```

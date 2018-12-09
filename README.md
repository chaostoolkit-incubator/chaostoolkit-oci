# Chaos Toolkit Extension for OCI

[![Build Status](https://travis-ci.org/chaostoolkit-incubator/chaostoolkit-oci.svg?branch=master)](https://travis-ci.org/chaostoolkit-incubator/chaostoolkit-oci)
[![Python versions](https://img.shields.io/pypi/pyversions/chaostoolkit-oci.svg)](https://www.python.org/)

This project is a collection of [actions][] and [probes][], gathered as an
extension to the [Chaos Toolkit][chaostoolkit].

[actions]: http://chaostoolkit.org/reference/api/experiment/#action
[probes]: http://chaostoolkit.org/reference/api/experiment/#probe
[chaostoolkit]: http://chaostoolkit.org

## Install

This package requires Python 3.5+

To be used from your experiment, this package must be installed in the Python
environment where [chaostoolkit][] already lives.

```
$ pip install -U chaostoolkit-oci
```

## Usage

To use the probes and actions from this package, add the following to your
experiment file:

```json
{
    "type": "action",
    "name": "stop-a-compute-instance",
    "provider": {
        "type": "python",
        "module": "chaosoci.compute.actions",
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
    "module": "chaosoci.compute.probes",
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

### Exploring probes and actions

In order to see which probes and actions are available, it is not necessary to dive into the source code.

Instead, run the script in the scripts directory as follows:

```./scripts/show_actions_and_probes.sh```

The script will output the Service and Type (e.g. Compute and Actions) and subsequently, will print the actions with the parameters they receive, which will give you a clue as to how they can be used within the experiment.

## Configuration

### Credentials

This extension uses the [oci-python-sdk][] library under the hood. This library expects
that you have properly [configured][creds] your environment to connect and
authenticate with the OCI services.

[oci-python-sdk]: https://github.com/oracle/oci-python-sdk
[creds]: https://docs.cloud.oracle.com/iaas/Content/API/Concepts/apisigningkey.htm

The way of doing this is by having a ~/.oci directory that contains a config file 
and the necessary api access pem files.

```
[DEFAULT]
user=ocid1.user.oc1..aaaaaaaabyneck4zsklp55y4ebgt2gvlwf7ypsz7hskluh3hpshfb3jelsew
fingerprint=88:c8:92:44:cf:5b:f8:de:f9:f0:44:cf:da:54:a2:c6
key_file=/home/user/.oci/oci_api_key.pem
tenancy=ocid1.tenancy.oc1..aaaaaaaarx3oltzmcws24bsf2mp77h6vbqwieembc74s2gohnfjjanmedxqj
compartment=ocid1.compartment.oc1..aaaaaaaaeaoardsao2cymuokft6crf6okik5uan4msovmdai44akwxje7tla
region=uk-london-1
namespace=tenancyname
```


## Contribute

If you wish to contribute more functions to this package, you are more than
welcome to do so. Please, fork this project, make your changes following the
usual [PEP 8][pep8] code style, sprinkling with tests and submit a PR for
review.

[pep8]: https://pycodestyle.readthedocs.io/en/latest/

The Chaos Toolkit projects require all contributors must sign a
[Developer Certificate of Origin][dco] on each commit they would like to merge
into the master branch of the repository. Please, make sure you can abide by
the rules of the DCO before submitting a PR.

[dco]: https://github.com/probot/dco#how-it-works

### Develop

If you wish to develop on this project, make sure to install the development
dependencies. But first, [create a virtual environment][venv] and then install
those dependencies.

[venv]: http://chaostoolkit.org/reference/usage/install/#create-a-virtual-environment

```console
$ pip install -r requirements-dev.txt -r requirements.txt 
```

Then, point your environment to this directory:

```console
$ python setup.py develop
```

Now, you can edit the files and they will be automatically be seen by your
environment, even when running from the `chaos` command locally.

### Test

To run the tests for the project execute the following:

```
$ pytest
```

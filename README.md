# Chaos Toolkit Extension for OCI

[![Build Status](https://travis-ci.org/chaostoolkit-incubator/chaostoolkit-oci.svg?branch=master)](https://travis-ci.org/chaostoolkit-incubator/chaostoolkit-oci)
[![Python versions](https://img.shields.io/pypi/pyversions/chaostoolkit-oci.svg)](https://www.python.org/)

This project is a collection of [actions][] and [probes][], gathered as an
extension to the [Chaos Toolkit][chaostoolkit].

[actions]: http://chaostoolkit.org/reference/api/experiment/#action
[probes]: http://chaostoolkit.org/reference/api/experiment/#probe
[chaostoolkit]: http://chaostoolkit.org

[oci-configuration]: https://docs.cloud.oracle.com/iaas/Content/API/Concepts/apisigningkey.htm
[oci-python-sdk]: https://docs.cloud.oracle.com/en-us/iaas/Content/API/SDKDocs/pythonsdk.htm

## Pre-requisites

* Install Python 3.5+
* Install pip

## Create a virtual environment

Create a local virtual environment where you can install dependencies:

```
python3 -m venv ~/.venvs/chaostk
```

Activate the environment:

```
source  ~/.venvs/chaostk/bin/activate
```

## Install dependencies

If you intend to only __use__ this toolkit, install the following dependencies in your virtual environment:

```
pip install chaostoolkit
pip install -U chaostoolkit-oci
```

If you intend to develop and contribute or use the latest from this repo, install the additional developer dependencies and point your environment to this directory:

```
pip install chaostoolkit
pip install -r requirements-dev.txt -r requirements.txt
python setup.py develop
```

Now, you can edit the files and they will be automatically be seen by your
environment, even when running from the `chaos` command locally.

Verify that the chaostoolkit has been installed properly:

```
chaos --version
```

## Discover capabilities and experiments

```
chaos discover --no-install chaostoolkit-oci
```

## Configuration

### Credentials

This extension uses the [oci-python-sdk][oci-python-sdk] library under the hood. It expects that you have properly [configured][oci-configuration] your environment to connect and authenticate with the OCI services.

The easiest way of doing this is by having a ~/.oci directory that contains a config file 
and the necessary api access pem files.

```
[DEFAULT]
user=ocid1.user.oc1..aaaaaaaabyneck4zsklp55y4ebgxxxxxxx7ypsz7hskluh3hpshfb3jelsew
fingerprint=00:ab:23:45:bc:6d:e7:fg:h8:i9:00:jk:lm:12:34:56
key_file=/home/user/.oci/oci_api_key.pem
tenancy=ocid1.tenancy.oc1..aaaaaaaarx3oltzmcws24bsfxxxxxxxxbqwieembc74s2gohnfjjanmedxqj
compartment=ocid1.compartment.oc1..aaaaaaaaeaoardsao2cyxxxxxxxcrf6okik5uan4msovmdai44akwxje7tla
region=uk-london-1
namespace=tenancyname
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

### Test

To run the tests for the project execute the following:

```
$ pytest
```
 

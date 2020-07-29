[dco]: https://github.com/probot/dco#how-it-works
[oci-python-sdk]: https://oracle-cloud-infrastructure-python-sdk.readthedocs.io/en/latest/api/landing.html
[pep8]: https://pycodestyle.pycqa.org/en/latest/
[signing-commits]: https://help.github.com/en/github/authenticating-to-github/signing-commits

# Contributing to chaostoolkit-oci

If you are interested to contribute to chaostoolkit-oci, you also need to install some additional libraries:

```
pip install -r requirements-dev.txt
```

Your contributions should follow the [OCI Python SDK API model][oci-python-sdk] for example:

* Compute is under `chaosoci/core/compute`, 
* VCN is under `chaosoci/core/vcn`, 
* MySQL should be under `chaosoci/mysql`, and so on.

Commits need to be [signed][signing-commits].

## Coding Style

[PEP 8][pep8].

## Tests

You also need to submit tests for your functions. Tests follow the package convention as the [OCI Python SDK API model][oci-python-sdk].

To run the tests for the project execute the following:

```
pytest
```

## External contributors

If you wish to contribute to this project, follow this process:

1. Fork this project
2. Create your issue branch (issue-xxx)
3. Write your code and push to your issue branch.
4. Raise a pull request to https://github.com/chaostoolkit-incubator/chaostoolkit-oci/master

The Chaos Toolkit projects require all contributors must sign a
[Developer Certificate of Origin][dco] on each commit they would like to merge
into the master branch of the repository. Please, make sure you can abide by
the rules of the DCO before submitting a PR.

## Tests

To run the tests for the project execute the following:

```
pytest
```
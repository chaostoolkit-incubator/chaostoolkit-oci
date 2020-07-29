# Installing chaostoolkit, chaostoolkit-oci and dependencies

### Clone the repo

```
git clone https://github.com/oracle/chaostoolkit-oci.git
cd chaostoolkit-oci
```

### Installing chaostoolkit

pip install -r requirements.txt

Verify that the chaostoolkit has been installed properly:

```
chaos --version
```

### Installing chaostoolkit-oci

```
python setup.py develop
```

### Discovering capabilities

```
chaos discover --no-install chaostoolkit-oci
```

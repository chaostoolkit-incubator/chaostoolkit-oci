// Copyright (c) 2020, Oracle and/or its affiliates.
// Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl.

pipeline {
    options {
        disableConcurrentBuilds()
    }

    agent {
        docker {
            image "${RUNNER_IMAGE}"
        }
    }

    stages {
        stage('Build') {
            steps {
                sh """
                    # create virtual environment
                    sudo pip-3.6 install virtualenv
                    virtualenv ~/.venvs/chaostk

                    # enter the python virtual environment
                    source ~/.venvs/chaostk/bin/activate

                    # install oci sdk
                    pip-3.6 install oci

                    # install dependencies
                    pip-3.6 install -r requirements.txt -r requirements-dev.txt
                    chaos --version

                    # setup dev environment
                    python3.6 setup.py develop

                    # run the CI script
                    bash ./ci.bash
                """
            }
        }
    }
}
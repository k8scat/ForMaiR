pipeline {
    agent {
        docker {
            image 'python:3.6-alpine'
        }
    }
    stages {
        stage('Release to PyPI.org') {
            steps {
                withCredentials(bindings: [
                    usernamePassword(credentialsId: 'pypi_token',
                    passwordVariable: 'password',
                    usernameVariable: 'username')
                ]) {
                    sh '''
                    python -m pip install --upgrade pip setuptools wheel twine
                    pip install -r requirements.txt
                    python setup.py sdist bdist_wheel
                    twine upload -u $username -p $password dist/*
                    '''
                }
            }
        }
    }
}

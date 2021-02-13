pipeline {
    agent {
        docker {
            image 'python:3.6-alpine'
            args '-v /var/jenkins_home/.cache/pip:/root/.cache/pip'
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
                    python -m pip install -i http://mirrors.aliyun.com/pypi/simple/ \
                    --trusted-host mirrors.aliyun.com \
                    --upgrade pip setuptools wheel twine
                    pip install -r requirements.txt
                    python setup.py sdist bdist_wheel
                    twine upload -u $username -p $password dist/*
                    '''
                }
            }
        }
    }
}

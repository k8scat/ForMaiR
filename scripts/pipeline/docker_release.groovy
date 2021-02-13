pipeline {
    agent {
        label 'master'
    }
    stages {
        stage('Release to DockerHub') {
            steps {
                withCredentials(bindings: [
                    usernamePassword(credentialsId: 'dockerhub_k8scat',
                    passwordVariable: 'password',
                    usernameVariable: 'username')
                ]) {
                    sh '''
                    docker login -u $username -p $password
                    docker build -t formair:latest .
                    docker push k8scat/formair:latest
                    '''
                }
            }
        }
    }
}

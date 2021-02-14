pipeline {
    agent {
        label 'master'
    }

    parameters {
        string (
            name: 'tag',
            defaultValue: 'latest',
            description: 'build tag'
        )
    }

    stages {
        stage('Release to DockerHub') {
            steps {
                withCredentials(bindings: [
                    usernamePassword(credentialsId: 'dockerhub_k8scat',
                    passwordVariable: 'password',
                    usernameVariable: 'username')
                ]) {
                    sh """
                    docker login -u ${username} -p ${password}
                    docker build -t k8scat/formair:${params.tag} .
                    docker push k8scat/formair:latest
                    """
                }
            }
        }
    }
}

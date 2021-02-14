pipeline {
    agent {
        label 'master'
    }

    parameters {
        string (
            name: 'tags',
            defaultValue: 'latest',
            description: 'build tags seperated with comma, for example: latest,1.3.1'
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
                    tags=(${params.tags//,/ })
                    for tag in ${tags[@]}
                    do
                        docker build -t k8scat/formair:${tag} .
                        docker push k8scat/formair:${tag}
                    done
                    """
                }
            }
        }
    }
}

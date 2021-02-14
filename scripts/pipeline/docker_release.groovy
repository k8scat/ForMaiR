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
                    script {
                        sh "docker login -u ${username} -p ${password}"
                        def tags = "${params.tags}".split(',')
                        for (tag in tags) {
                            sh """
                            docker build -t k8scat/formair:${tag} .
                            docker push k8scat/formair:${tag}
                            """
                        }
                    }
                }
            }
        }
    }
}

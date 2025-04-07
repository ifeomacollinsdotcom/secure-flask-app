pipeline {
    agent { label 'n2' }

    environment {
        INVENTORY = 'inventory.ini'
        PLAYBOOK = 'site.yml'
    }

    stages {
        stage('Verify Artifact') {
            steps {
                echo 'Checking file integrity...'
                sh 'sha256sum -c hash.txt'
            }
        }

        stage('Deploy to Ubuntu (n1)') {
            steps {
                echo 'Running Ansible playbook with roles...'
                sh "ansible-playbook -i ${INVENTORY} ${PLAYBOOK}"
            }
        }
    }

    post {
        success {
            echo 'App deployed successfully!'
        }
        failure {
            echo 'Deployment failed.'
        }
    }
}

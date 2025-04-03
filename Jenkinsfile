pipeline {
    agent {
        label 'centos-agent'  // This should match the label of your Jenkins agent
    }
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        
        stage('Build Artifact') {
            steps {
                sh '''
                mkdir -p artifact
                cp -r app/* artifact/
                tar -czf artifact.tar.gz -C artifact .
                '''
            }
        }
        
        stage('Generate Hash') {
            steps {
                sh '''
                sha256sum artifact.tar.gz | cut -d " " -f1 > hash.txt
                cat hash.txt
                '''
            }
        }
        
        stage('Archive Artifacts') {
            steps {
                archiveArtifacts artifacts: 'artifact.tar.gz,hash.txt', fingerprint: true
            }
        }
        
        stage('Deploy with Ansible') {
            steps {
                sh '''
                # Make sure MongoDB init script is available to Ansible
                cp app/init_db.js ansible/roles/mongodb/files/
                
                cd ansible
                ansible-playbook -i inventory site.yml -e "workspace=${WORKSPACE}"
                '''
            }
        }
    }
    
    post {
        success {
            echo 'Deployment successful!'
        }
        failure {
            echo 'Deployment failed!'
        }
    }
}

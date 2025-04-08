pipeline {
    agent any  // You can change to 'n1' or 'any' depending on your Jenkins configuration

    environment {
        APP_NAME = "flask-app"
        SERVER_IP = "172.31.10.61"  // No space at the end of the IP address
        DEPLOY_DIR = "/var/www/flask-app"  // Your app directory on the server
        REMOTE_USER = "n2"  // Remote server username (replace with actual)
        REMOTE_SSH_KEY = credentials('ssh-key')  // Use the correct credentials name
    }

    stages {
        stage('Checkout') {
            steps {
                // Checkout the code from the Git repository
                git 'https://github.com/ifeomacollinsdotcom/flask-app.git'
            }
        }

        stage('Set up Python') {
            steps {
                // Set up Python environment (assuming Python 3)
                script {
                    sh '''
                    sudo apt-get update
                    sudo apt-get install -y python3 python3-pip
                    python3 -m venv venv
                    source venv/bin/activate
                    pip install --upgrade pip
                    '''
                }
            }
        }

        stage('Install dependencies') {
            steps {
                // Install required Python packages
                script {
                    sh '''
                    source venv/bin/activate
                    pip install -r requirements.txt  # Assuming you have a requirements.txt file
                    '''
                }
            }
        }

        stage('Run Tests') {
            steps {
                // If you have test scripts, run them here
                script {
                    sh '''
                    source venv/bin/activate
                    python -m unittest discover -s tests  # Modify based on your test setup
                    '''
                }
            }
        }

        stage('Deploy') {
            steps {
                // Deploy your app to the remote server (EC2 in your case)
                script {
                    sh '''
                    ssh -o StrictHostKeyChecking=no -i ${REMOTE_SSH_KEY} ${REMOTE_USER}@${SERVER_IP} << 'EOF'
                    cd ${DEPLOY_DIR}
                    git pull origin main  # Update the code from repository (adjust branch if needed)
                    source venv/bin/activate
                    pip install -r requirements.txt  # Install dependencies if new ones are added
                    sudo systemctl restart flask-app.service  # Restart your Flask service
                    EOF
                    '''
                }
            }
        }

        stage('Clean up') {
            steps {
                // Clean up workspace (if needed)
                cleanWs()
            }
        }
    }

    post {
        always {
            // Always clean up or notify after the pipeline finishes
            echo "Pipeline completed"
        }
        success {
            // Send a notification or email on successful deployment
            echo "App deployed successfully"
        }
        failure {
            // Send a notification or email on failure
            echo "Deployment failed!"
        }
    }
}

pipeline {
    agent {
        label 'n2'  // Updated to match your inventory hostname
        docker {
            image 'centos:8'
            args '-v /home/jenkins/.ssh:/root/.ssh:ro -m 2GB --cpus=1'
        }
    }

    options {
        timeout(time: 30, unit: 'MINUTES')
        buildDiscarder(logRotator(numToKeepStr: '10'))
        disableConcurrentBuilds()
    }

    environment {
        ARTIFACT_DIR = "${WORKSPACE}/artifact"
        ANSIBLE_CONFIG = "${WORKSPACE}/ansible/ansible.cfg"
        DEPLOYMENT_ID = sh(script: 'date +%Y%m%d-%H%M%S', returnStdout: true).trim()
        WEB_SERVER_IP = '172.31.44.87'  // n1
        AGENT_IP = '172.31.8.209'       // n2
    }

    stages {
        stage('Checkout') {
            steps {
                script {
                    // Fix Git security before checkout
                    sh 'git config --global --add safe.directory ${WORKSPACE}'
                    checkout([
                        $class: 'GitSCM',
                        branches: scm.branches,
                        extensions: scm.extensions + [
                            [$class: 'CleanBeforeCheckout'],
                            [$class: 'CloneOption', depth: 1, noTags: true]
                        ],
                        userRemoteConfigs: scm.userRemoteConfigs
                    ])
                }
            }
        }

        stage('Build & Verify') {
            parallel {
                stage('Build Artifact') {
                    steps {
                        sh """
                        mkdir -p ${ARTIFACT_DIR}
                        find app/ -type f \( -name "*.py" -o -name "*.js" \) -exec cp --parents {} ${ARTIFACT_DIR} \;
                        tar -czf artifact.tar.gz -C ${ARTIFACT_DIR} .
                        """
                    }
                }
                stage('Run Tests') {
                    steps {
                        sh """
                        source ${WORKSPACE}/venv/bin/activate
                        python -m pytest app/tests/ --junitxml=test-results.xml
                        """
                    }
                    post {
                        always {
                            junit 'test-results.xml'
                        }
                    }
                }
            }
        }

        stage('Generate Hashes') {
            steps {
                sh """
                sha256sum artifact.tar.gz > full_hash.txt
                md5sum artifact.tar.gz > md5_hash.txt
                """
                stash includes: 'full_hash.txt,md5_hash.txt', name: 'hashfiles'
            }
        }

        stage('Deploy') {
            parallel {
                stage('Deploy Web Servers (n1)') {
                    when {
                        expression { env.DEPLOY_TARGET == null || env.DEPLOY_TARGET == 'web' }
                    }
                    steps {
                        withCredentials([sshUserPrivateKey(
                            credentialsId: 'ansible-ssh-key',
                            keyFileVariable: 'SSH_KEY'
                        )]) {
                            sh """
                            cd ansible
                            ansible-playbook -i inventory site.yml \
                              --limit web_server \
                              -e "deployment_id=${DEPLOYMENT_ID}" \
                              --private-key=${SSH_KEY} \
                              | tee deploy-web-${DEPLOYMENT_ID}.log
                            """
                        }
                    }
                }
                stage('Configure Jenkins Agent (n2)') {
                    when {
                        expression { env.DEPLOY_TARGET == null || env.DEPLOY_TARGET == 'agent' }
                    }
                    steps {
                        script {
                            // Self-deploy to agent n2
                            if (env.NODE_NAME == 'n2') {
                                withCredentials([sshUserPrivateKey(
                                    credentialsId: 'ansible-ssh-key',
                                    keyFileVariable: 'SSH_KEY'
                                )]) {
                                    sh """
                                    cd ansible
                                    ansible-playbook -i inventory agent.yml \
                                      --limit '${env.NODE_NAME}' \
                                      -e "deployment_id=${DEPLOYMENT_ID}" \
                                      --private-key=${SSH_KEY} \
                                      | tee deploy-agent-${DEPLOYMENT_ID}.log
                                    """
                                }
                            }
                        }
                    }
                }
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: '**/deploy-*.log,test-results.xml', fingerprint: true
            cleanWs()
        }
        success {
            slackSend(color: 'good', 
                     message: """✅ DEPLOYED: ${env.JOB_NAME} #${env.BUILD_NUMBER}
                     • Web Server: n1 (${WEB_SERVER_IP})
                     • Jenkins Agent: n2 (${AGENT_IP})
                     ${env.BUILD_URL}""")
        }
        failure {
            script {
                if (currentBuild.result == 'FAILURE') {
                    build job: 'Rollback-Deployment',
                    parameters: [
                        string(name: 'DEPLOYMENT_ID', value: "${DEPLOYMENT_ID}"),
                        string(name: 'TARGET_GROUP', value: "jenkins_agent"),  // Focus on n2
                        string(name: 'FAILED_JOB_URL', value: "${env.BUILD_URL}")
                    ],
                    propagate: false
                }
            }
            slackSend(color: 'danger',
                     message: """❌ FAILED: ${env.JOB_NAME} #${env.BUILD_NUMBER}
                     Rolling back ${DEPLOYMENT_ID} on agent n2
                     ${env.BUILD_URL}""")
        }
    }
}

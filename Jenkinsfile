pipeline {
    agent any

    stages {
        stage('1. Checkout Code') {
            steps {
                echo 'Checking out Student Academic Management Platform source code'
                checkout scm
            }
        }

        stage('2. Build') {
            steps {
                sh 'python3 --version'
                sh 'python3 -m venv .venv'
                sh '. .venv/bin/activate && pip install --upgrade pip'
                sh '. .venv/bin/activate && pip install -r requirements.txt'
                sh '. .venv/bin/activate && ruff check app tests run.py --output-format concise'
            }
        }

        stage('3. Unit Test') {
            steps {
                sh '. .venv/bin/activate && pytest -v --junitxml=pytest-report.xml --cov=app --cov-report=term'
            }
            post {
                always {
                    junit allowEmptyResults: true, testResults: 'pytest-report.xml'
                }
            }
        }

        stage('4. Package') {
            steps {
                sh 'tar --exclude=.git --exclude=.venv --exclude=__pycache__ -czf student-academic-platform.tar.gz app tests run.py requirements.txt Dockerfile Jenkinsfile k8s'
                archiveArtifacts artifacts: 'student-academic-platform.tar.gz', fingerprint: true
            }
        }

        stage('5. Deploy') {
            steps {
                echo 'Deployment stage: build the Docker image and apply Kubernetes manifests in the deployment workflow.'
                sh 'test -f Dockerfile && test -f k8s/deployment.yaml && test -f k8s/service.yaml'
            }
        }
    }

    post {
        success {
            echo 'Pipeline completed successfully!'
        }
        failure {
            echo 'Pipeline failed. Check Console Output for details.'
        }
    }
}

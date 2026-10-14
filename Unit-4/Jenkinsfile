
pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                    python3 -m venv .venv
                    .venv/bin/pip install --upgrade pip
                    .venv/bin/pip install -r requirements.txt
                    .venv/bin/pip install pytest pytest-cov ruff
                '''
            }
        }

        stage('Lint') {
            steps {
                sh '.venv/bin/ruff check app tests run.py --output-format concise'
            }
        }

        stage('Unit Tests') {
            steps {
                sh '''
                    export PYTHONPATH="$WORKSPACE"
                    .venv/bin/python -m pytest tests/ -v \
                        --junitxml=pytest-report.xml \
                        --cov=app --cov-report=term
                '''
            }
            post {
                always {
                    junit allowEmptyResults: true,
                          testResults: 'pytest-report.xml'
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t student-academic-platform:v1.0.0 .'
            }
        }
    }

    post {
        success {
            echo 'Tests passed and Docker image built successfully.'
        }
        failure {
            echo 'Pipeline failed. Check Console Output for details.'
        }
    }
}

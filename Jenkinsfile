// Jenkinsfile (Declarative Pipeline)
pipeline {
    // Defines where the entire pipeline runs.
    // 'any' means on any available agent.
    agent any

    // Global environment variables for the entire pipeline.
    environment {
        APP_NAME = "personal_finance_tracker_app"
        CONTAINER_NAME = "${APP_NAME}_container"
        APP_INT_PORT = "5001"   // Internal port for the application
        APP_EXT_PORT = "5010"   // Exposed port for the application
        // BUILD_NUMBER is a built-in Jenkins environment variable.
        IMAGE_TAG = "${env.BUILD_NUMBER}"
    }

    // Defines the main stages of the pipeline.
    stages {
        stage('Clean Workspace') {
            steps {
                echo 'Cleaning workspace...'
                cleanWs() // Built-in step for cleaning workspace
            }
        }

        stage('Clone Code') {
            steps {
                echo 'Cloning source code from Git...'
                git branch: 'main', url: 'https://github.com/xopsguru/fintracker.git'
            }
        }

        // This stage contains parallel execution of sub-stages.
        stage('Build & Test (Parallel)') {
            parallel {
                // First parallel branch: Build Frontend
                stage('Build Frontend') {
                    steps {
                        echo 'Starting frontend build...'
                        sh 'sleep 5' // Simulate work
                        echo 'Frontend build completed.'
                    }
                }

                // Second parallel branch: Build Backend
                stage('Build Backend') {
                    steps {
                        echo 'Starting backend build...'
                        sh 'sleep 7' // Simulate work
                        echo 'Backend build completed.'
                    }
                }

                // Third parallel branch: Run Unit Tests
                stage('Run Unit Tests') {
                    steps {
                        echo 'Executing unit tests...'
                        sh 'sleep 3' // Simulate work
                        echo 'Unit tests passed.'
                    }
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                echo "Building Docker image: ${env.APP_NAME}:${env.IMAGE_TAG}"
                // Ensure Docker daemon is accessible without sudo on agent
                sh "docker build --no-cache -t ${env.APP_NAME}:${env.IMAGE_TAG} ."
            }
        }

        stage('Stop & Remove Existing Container') {
            steps {
                echo "Stopping and removing old container: ${env.CONTAINER_NAME}"
                // '|| true' makes the command succeed even if container doesn't exist
                sh """
                    docker stop ${env.CONTAINER_NAME} || true
                    docker rm ${env.CONTAINER_NAME} || true
                """
            }
        }

        stage('Run Docker Container') {
            steps {
                echo "Running new container: ${env.CONTAINER_NAME} on port ${env.APP_EXT_PORT}"
                sh "docker run -p ${env.APP_INT_PORT}:${env.APP_EXT_PORT} --name ${env.CONTAINER_NAME} -d ${env.APP_NAME}:${env.IMAGE_TAG}"
            }
        }
    }

    // Post-build actions, executed after all stages are done.
    post {
        always {
            echo "Pipeline for ${env.APP_NAME} finished. Status: ${currentBuild.result}"
            echo "Container: ${env.CONTAINER_NAME}, Image Tag: ${env.IMAGE_TAG}"
        }
        success {
            echo 'Pipeline completed successfully! 🎉'
        }
        failure {
            echo 'Pipeline failed! ❌ Please check the logs.'
        }
    }
}
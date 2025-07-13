// Jenkinsfile (Declarative Pipeline)
pipeline { // Declarative syntax for Jenkins Pipeline
    // Defines where the entire pipeline runs.
    // 'any' means on any available agent.
    agent any

    // Global environment variables for the entire pipeline.
    environment {
        APP_NAME = "personal_finance_tracker_app" // Name of the application
        CONTAINER_NAME = "${APP_NAME}_container" //
        APP_INT_PORT = "5001"   // Internal port for the application
        APP_EXT_PORT = "5010"   // Exposed port for the application
        // BUILD_NUMBER is a built-in Jenkins environment variable.
        IMAGE_TAG = "${env.BUILD_NUMBER}" // Tag for the Docker image, based on the build number
    }

    // Defines the main stages of the pipeline.
    stages { // Each stage represents a step in the CI/CD process.
        stage('Clean Workspace') { // Stage to clean the workspace before starting
            steps { // Steps are the individual actions within a stage.
                echo 'Cleaning workspace...' // Log message for clarity
                cleanWs() // Built-in step for cleaning workspace 
            }
        }

        stage('Clone Code') { // Stage to clone the source code from Git repository
            steps { //
                echo 'Cloning source code from Git...' //
                git branch: 'dev', url: 'https://github.com/xopsguru/fintracker.git' //
            }
        }

        // This stage contains parallel execution of sub-stages.
        stage('Build & Test (Parallel)') { //
            parallel { // Allows multiple stages to run concurrently for efficiency
                // First parallel branch: Build Frontend
                stage('Build Frontend') { // Stage for building the frontend
                    steps {
                        echo 'Starting frontend build...'
                        sh 'sleep 5' // Simulate work with a sleep command
                        // In a real scenario, this would be replaced with actual build commands
                        echo 'Frontend build completed.'
                    }
                }

                // Second parallel branch: Build Backend
                stage('Build Backend') {
                    steps {
                        echo 'Starting backend build...'
                        sh 'sleep 7' // Simulate work
                        // In a real scenario, this would be replaced with actual build commands
                        echo 'Backend build completed.'
                    }
                }

                // Third parallel branch: Run Unit Tests
                stage('Run Unit Tests') {
                    steps {
                        echo 'Executing unit tests...'
                        sh 'sleep 3' // Simulate unit tests
                        // In a real scenario, this would be replaced with actual test commands
                        echo 'Unit tests passed.'
                    }
                }
            }
        }
        // --- ADD THIS DEBUG STAGE ---
        stage('Verify Dockerfile Content') {
            steps {
                echo 'Content of Dockerfile in workspace:'
                sh 'cat Dockerfile' // This will print the Dockerfile content to the console output
            }
        }
        // --- END DEBUG STAGE ---

        stage('Build Docker Image') { // Stage to build the Docker image
            steps {
                echo "Building Docker image: ${env.APP_NAME}:${env.IMAGE_TAG}"
                // Ensure Docker daemon is accessible without sudo on agent
                sh "docker build --no-cache --pull -t ${env.APP_NAME}:${env.IMAGE_TAG} ." // Build the Docker image
            }
        }

        stage('Stop & Remove Existing Container') { // Stage to stop and remove any existing Docker container
            steps {
                echo "Stopping and removing old container: ${env.CONTAINER_NAME}"
                // '|| true' makes the command succeed even if container doesn't exist
                sh """
                    docker stop ${env.CONTAINER_NAME} || true //
                    docker rm ${env.CONTAINER_NAME} || true
                """
            }
        }

        stage('Run Docker Container') { // Stage to run the Docker container with the built image
            steps {
                echo "Running new container: ${env.CONTAINER_NAME} on port ${env.APP_EXT_PORT}"
                sh "docker run -p ${env.APP_EXT_PORT}:${env.APP_INT_PORT} --name ${env.CONTAINER_NAME} -d ${env.APP_NAME}:${env.IMAGE_TAG}" 
                // Run the Docker container with port mapping
            }
        }
    }

    // Post-build actions, executed after all stages are done.
    post { // Defines actions to take after the pipeline execution
        always { // This block runs regardless of the build result
            echo "Pipeline for ${env.APP_NAME} finished. Status: ${currentBuild.result}"
            echo "Container: ${env.CONTAINER_NAME}, Image Tag: ${env.IMAGE_TAG}"
        }
        success { // This block runs only if the pipeline succeeds
            echo 'Pipeline completed successfully! 🎉'
        }
        failure { // This block runs only if the pipeline fails
            echo 'Pipeline failed! ❌ Please check the logs.'
        }
    }
}
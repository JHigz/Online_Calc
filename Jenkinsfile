pipeline {

  environment {
  PROJECT_DIR = "/app"
  REGISTRY = "jhsparta/new_calc" + ":" + "$BUILD_NUMBER"
  DOCKER_CREDENTIALS = "Docker_Auth"
  DOCKER_IMAGE = ""
  }

  agent any

  options {
    skipStagesAfterUnstable()
  }

  stages{

    stage('Cloning Code From Git') {
      steps{
        git branch: 'main',
        url: 'https://github.com/JHigz/Calc_Full_Infra'
      }

    }

    stage('Build-Image'){
      steps {
        script{
          DOCKER_IMAGE = docker.build REGISTRY
        }
      }
    }

    stage('Testing the code'){
      steps {
        script{
          sh '''docker run -v $PWD/test-results:/reports --workdir $PROJECT_DIR $REGISTRY pytest -v --junitxml=/reports/results.xml'''
        }
      }
      post {
        always {
          junit testResults: '**/test-results/*.xml'
        }
      }
    }

    stage('Deploy to Docker Hub'){
      steps {
        script {
          docker.withRegistry('', DOCKER_CREDENTIALS){
            DOCKER_IMAGE.push()
          }
        }
      }
    }

    stage('Removing the Docker Image'){
      steps {
        sh "docker rmi $REGISTRY"
      }
    }
  }
}

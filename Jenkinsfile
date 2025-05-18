pipeline {
  agent any
  stages {
    stage('Checkout') {
      steps {
        dir('/home/sdpr/projects') {
          checkout scm
        }
      }
    }
    stage('Build Docker') {
      steps {
        sh '''
          docker stop fastapi || true
          docker rm fastapi || true
          docker build -t fastapi /home/sdpr/projects
          docker run -d --name fastapi -p 8000:8000 fastapi
        '''
      }
    }
  }
}

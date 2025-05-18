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
  }
}

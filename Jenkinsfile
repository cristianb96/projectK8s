pipeline {
  agent any
  environment {
    REGISTRY = 'registry.example.com'
    IMAGE_NAME = "${REGISTRY}/pedido-backend"
    GIT_CREDENTIALS_ID = 'git-creds'
    GIT_REPO = 'git@your-git-server:your-org/pedido-app.git'
    GIT_BRANCH = 'main'
  }
  stages {
    stage('Checkout') {
      steps {
        git branch: env.GIT_BRANCH, url: env.GIT_REPO, credentialsId: env.GIT_CREDENTIALS_ID
      }
    }
    stage('Build Image') {
      steps {
        sh 'docker build -t ${IMAGE_NAME}:${BUILD_NUMBER} -f backend/Dockerfile backend'
      }
    }
    stage('Push Image') {
      steps {
        withCredentials([usernamePassword(credentialsId: 'docker-registry-creds', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
          sh 'echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin ${REGISTRY}'
          sh 'docker push ${IMAGE_NAME}:${BUILD_NUMBER}'
        }
      }
    }
    stage('Update values.yaml & Push') {
      steps {
        sh '''
          pip install yq || true
          yq eval -i ".backend.tag = \"${BUILD_NUMBER}\"" charts/pedido-app/values.yaml
          git add charts/pedido-app/values.yaml
          git commit -m "ci: bump backend tag to ${BUILD_NUMBER}"
          git push origin ${GIT_BRANCH}
        '''
      }
    }
  }
}
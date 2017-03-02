node('small') {
    checkout scm
    stage('Build') {
        docker.build('jenkins:syntaxnet')
    }

    stage('Test'){
        withDockerContainer('jenkins:syntaxnet') {
            sh 'python test.py'
        }
    }

    stage('Deploy') {
    	docker.withRegistry("https://565110903685.dkr.ecr.us-west-2.amazonaws.com/jenkins", "ecr:us-west-2:aws") {
  			docker.image("jenkins:syntaxnet").push()
		}
    }
}

node('large') {
    checkout scm
    stage('Build') {
        docker.build('jenkins:syntaxnet')
    }

    stage('Test'){
        withDockerContainer('jenkins:syntaxnet') {
            sh 'py.test .'
        }
    }

    stage('Deploy') {
        
		withCredentials([[$class: 'UsernamePasswordMultiBinding', credentialsId: 'dockerhub', usernameVariable: 'USERNAME', passwordVariable: 'PASSWORD']]) {
			sh "docker login --password=${PASSWORD} --username=${USERNAME}"
            try{
                def now = new Date()
                def key = now.format("yyyyMMdd-HH", TimeZone.getTimeZone('UTC'))
                sh "docker pull gliacloud/syntaxnet"
                sh "docker tag gliacloud/syntaxnet gliacloud/syntaxnet:" + key
                sh "docker push gliacloud/syntaxnet:" + key
            } catch (err) {
            }
			sh "docker tag jenkins:syntaxnet gliacloud/syntaxnet"
			sh "docker push gliacloud/syntaxnet"
		}
    }
}

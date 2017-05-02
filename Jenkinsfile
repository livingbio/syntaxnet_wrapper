library 'common'

node('small'){
    def project='syntaxnet'
    base_build{
        name=project
        test_script = {->
            sh 'py.test pyknp'
        }
        release = {->
            dockerhub.push_image(project, base_build.release_version())
        }
    }
}

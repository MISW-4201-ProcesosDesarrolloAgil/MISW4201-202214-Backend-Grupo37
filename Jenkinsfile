pipeline { 
    agent any
    environment {
        HOME = "${WORKSPACE}"
        GIT_CREDENTIAL_ID = '67fc884e-63ed-47cc-8a49-e91b798c7178'
        GIT_REPO = 'MISW4201-202214-Backend-Grupo37'
        GITHUB_TOKEN_ID = '782f4107-6a99-44c4-88ac-f6bd82b81b1d'
    }
    stages {
        stage('Checkout') { 
            steps {
                scmSkip(deleteBuild: true, skipPattern:'.*\\[ci-skip\\].*')
                git branch: 'Desarrollo',  
                credentialsId: env.GITHUB_TOKEN_ID,
                url: 'https://github.com/MISW-4201-ProcesosDesarrolloAgil/' + env.GIT_REPO
            }
        }
        stage('Gitinspector') {
            steps {
                script {
                    docker.image('gitinspector-isis2603').inside('--entrypoint=""') {
                        sh '''
                            mkdir -p ./reports/
                            gitinspector --file-types="py" --format=html --AxU -w -T -x author:Bocanegra -x author:estudiante > ./reports/index.html
                        '''
                    }
                }
                withCredentials([usernamePassword(credentialsId: env.GITHUB_TOKEN_ID, passwordVariable: 'GIT_PASSWORD', usernameVariable: 'GIT_USERNAME')]) {
                    sh('git config --global user.email "ci-isis2603@uniandes.edu.co"')
                    sh('git config --global user.name "ci-isis2603"')
                    sh('git add ./reports/index.html')
                    sh('git commit -m "[ci-skip] GitInspector report added"')
                    sh('git pull https://${GIT_USERNAME}:${GIT_PASSWORD}@github.com/MISW-4201-ProcesosDesarrolloAgil/${GIT_REPO} Desarrollo')
                    sh('git push https://${GIT_USERNAME}:${GIT_PASSWORD}@github.com/MISW-4201-ProcesosDesarrolloAgil/${GIT_REPO} Desarrollo')
                }  
            }
        }
        stage('Install libraries') {
            steps {
                script {
                    docker.image('python:3.7.6').inside {
                        sh '''
                            pip install --user -r requirements.txt
                        '''
                    }
                }
            }
        }
        stage('Testing') {
            steps {
                script {
                    docker.image('python:3.7.6').inside {
                        sh '''
                            python -m unittest discover -s tests -v
                        '''
                    }
                }
            }
        }
        stage('Coverage') {
            steps {
                script {
                    docker.image('python:3.7.6').inside {
                        sh '''
                            python -m coverage run -m unittest discover -s tests -v
                            python -m coverage html
                        ''' 
                    }
                }
            }
        }
        stage('Report') {
            steps {
                publishHTML (target : [allowMissing: false,
                    alwaysLinkToLastBuild: true,
                    keepAll: true,
                    reportDir: 'htmlcov/',
                    reportFiles: 'index.html',
                    reportName: 'Coverage Report',
                    reportTitles: 'Coverage Report']
                )
            }
        }
    }
    post { 
      always { 
         // Clean workspace
         cleanWs deleteDirs: true
      }
   }
}

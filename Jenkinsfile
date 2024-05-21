import org.jenkinsci.plugins.workflow.steps.FlowInterruptedException
pipeline {
    agent any
    environment {
       tgBot_id = credentials('kin_of_memes_bot_id')
       my_chat_id = credentials('my_chat_id')
    }
    stages {
       stage('get dependencies'){
           try{
            steps {
                sh 'python3 -m venv ./venv'
                sh '. venv/bin/activate'
                sh 'pip install -r requirements.txt'
                   }
           }
    catch (FlowInterruptedException e) {
      // we re-throw as a different error, that would not 
      // cause retry() to fail (workaround for issue JENKINS-51454)
      error 'Timeout!'
           
        }
       stage('runBot'){
            steps {
                sh 'python3 main.py'
                   }
        }
    }

    post {
    failure {
    sh  ("""
        curl -s -X POST https://api.telegram.org/bot${tgBot_id}/sendMessage -d chat_id=${my_chat_id} -d parse_mode=markdown -d text="*${env.JOB_NAME}* FAILED ${env.BUILD_URL}"
    """)
    }
    aborted {
    sh  ("""
        curl -s -X POST https://api.telegram.org/bot${tgBot_id}/sendMessage -d chat_id=${my_chat_id} -d parse_mode=markdown -d text="*${env.JOB_NAME}* ABORTED ${env.BUILD_URL}"
    """)
    }

        }
    }

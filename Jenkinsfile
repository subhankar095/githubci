def sendSlackNotifFn(String buildResult,String channel) {
  if ( buildResult == "SUCCESS" ) {
    slackSend(color: "good", message: "Job: ${env.JOB_NAME} with buildnumber ${env.BUILD_NUMBER} was successful" , channel: channel)
  }
  else if( buildResult == "FAILURE" ) { 
    slackSend(color: "danger", message: "Job: ${env.JOB_NAME} with buildnumber ${env.BUILD_NUMBER} was failed", channel: channel)
  }
  else if( buildResult == "UNSTABLE" ) { 
    slackSend(color: "warning", message: "Job: ${env.JOB_NAME} with buildnumber ${env.BUILD_NUMBER} was unstable" , channel: channel)
  }
  else {
    slackSend(color: "danger", message: "Job: ${env.JOB_NAME} with buildnumber ${env.BUILD_NUMBER} its result was unclear",channel: channel)
  }
}
pipeline {
    agent any
    options {
        // Stop the build early in case of compile or test failures
        skipStagesAfterUnstable()
    }
    stages {
        stage('Get code') {
        steps {
            checkout scm
            echo "getting code"
        }
        }
         stage('test') {
          steps {
            script {
            sh '''
               py.test --junitxml results.xml tests.py
            '''
           }
          }
         }
         stage('publish to github') {
          steps {
            script {
		    withCredentials([string(credentialsId: 'GITHUB_ACCESS_TOKEN', variable: 'GITHUB_ACCESS_TOKEN')]) {
		    sh '''
                    zip -r  artifact.zip .
                    url_without_suffix="${GIT_URL%.*}"
                    echo $url_without_suffix
                    reponame="$(basename \"${url_without_suffix}\")"
                    echo $reponame
                    user=$(echo $url_without_suffix | awk -v FS="(https://github.com|$reponame)" '{print $2}')
                    echo $user
                    tag=$(git describe --tags)
                    echo $tag
                    # Get the full message associated with this tag
                    #message="$(git for-each-ref refs/tags/$tag --format='%(contents)')"
                    API_JSON=$(printf '{"tag_name": "v%s","target_commitish": "master","name": "v%s","body": "Release of version %s","draft": false,"prerelease": true}' $tag $tag $tag)
                    release=$(curl -X POST -H "Authorization:token $GITHUB_ACCESS_TOKEN" --data "$API_JSON" https://api.github.com/repos$user$reponame/releases)
                    echo $release
                    curl -X POST -H "Authorization:token $GITHUB_ACCESS_TOKEN" -H "Content-Type:application/octet-stream" --data-binary @artifact.zip https://uploads.github.com/repos$user$reponame/releases/$id/assets?name=artifact.zip
                    rm -f artifact.zip
                '''
		}
	    }
          }
       }
    }
   post {
    always {
        sendSlackNotifFn(currentBuild.currentResult, "jenkins")
    }
    }
}

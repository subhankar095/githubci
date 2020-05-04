pipeline {
    agent any
    stages {
        stage('Get code') {
        steps {
            checkout scm
            echo "getting code"
        }
        }
         stage('build') {
          steps {
            echo "build step simulation"
           }
         }
         stage('publish to github') {
          steps {
            script {
		    withCredentials([string(credentialsId: 'GITHUB_ACCESS_TOKENS', variable: 'GITHUB_ACCESS_TOKEN')]) {
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
                    release=$(curl -X POST -H "Authorization:token $GITHUB_ACCESS_TOKEN" --data "{\"tag_name\": \"$tag\", \"target_commitish\": \"master\", \"name\": \"$tag\", \"draft\": false, \"prerelease\": true}" https://api.github.com/repos$user$reponame/releases)
                    echo $release
                    curl -X POST -H "Authorization:token $GITHUB_ACCESS_TOKEN" -H "Content-Type:application/octet-stream" --data-binary @artifact.zip https://uploads.github.com/repos$user$reponame/releases/$id/assets?name=artifact.zip
                    rm -f artifact.zip
                '''
		}
	    }
          }
       }
    }
}

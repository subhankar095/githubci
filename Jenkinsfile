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
}

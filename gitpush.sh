#!/bin/bash


function config() {
  git init
  git config --add github.user "dryalcinmehmet"
  git config --add github.email "dryalcinmehmet@gmail.com"
  git config --global credential.helper cache
}

function push() {

  CURRENTDIR=${PWD##*/}
  GITHUBUSER="dryalcinmehmet"
      # Get user input
  echo "Enter name for new repo, or just <return> to make it $CURRENTDIR"
  read REPONAME
  echo "Enter key to make the new repo public, 'x' for private"
  read PRIVATE_ANSWER

  if [ "$PRIVATE_ANSWER" == "x" ]; then
    PRIVACYWORD=private
    PRIVATE_TF=true
  else
    PRIVACYWORD=public
    PRIVATE_TF=false
  fi

  REPONAME=${REPONAME:-${CURRENTDIR}}
  USERNAME=${GITHUBUSER:-${GITHUBUSER}}

  echo "Will create a new *$PRIVACYWORD* repo named $REPONAME"
  echo "on github.com in user account $USERNAME, with this description:"
  echo $DESCRIPTION
  echo "Type 'y' to proceed, any other character to cancel."
  read OK
  if [ "$OK" != "y" ]; then
    echo "User cancelled"
    exit
  fi

  # Curl some json to the github API oh damn we so fancy
  if curl -u $USERNAME https://api.github.com/user/repos -d "{\"name\": \"$REPONAME\", \"description\": \"${DESCRIPTION}\", \"private\": $PRIVATE_TF, \"has_issues\": true, \"has_downloads\": true, \"has_wiki\": false}" || echo "Exist!"]; then
    echo "Repo Create!"
  else
    echo "Repo Exist!"
  fi

  # Set the freshly created repo to the origin and push
  # You'll need to have added your public key to your github account
  git init
  git add .
  git commit -m "Auto Commit!"

  if git remote add origin https://github.com/$USERNAME/$REPONAME.git;
    then
    echo "Repo Create!"
  else
    echo "Repo Exist!"
  fi
  git checkout -b "master"
  git push -u origin master

}



# Check if the function exists (bash specific)
if declare -f "$1" > /dev/null
then
  # call arguments verbatim
  "$@"
else
  # Show a helpful error
  echo "'$1' is not a known function name" >&2
  exit 1
fi







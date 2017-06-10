#!/usr/bin/env bash

# 
# after_success
# deploy gh-pages
#

setup_git() {
    git config --global user.email "zhangt@frib.msu.edu"
    git config --global user.name "Travis CI"
}

add_files() {
    cp -arv docs/build/html/* . \
        | awk -F'->' '{print $2}' \
        | sed "s/[\’\ \‘]//g" > /tmp/filelist
    
    for ifile in `cat /tmp/filelist`
    do
        git add ${ifile}
    done
}

commit_files() {
    git stash
    git checkout -b gh-pages
    add_files
    git commit -m "Update docs by Travis build: $TRAVIS_BUILD_NUMBER"
}

push_files() {
    git remote add pages https://${GITHUB_TOKEN}@github.com/archman/phantasy.git
    git push --quiet --set-upstream pages gh-pages --force
}

setup_git
commit_files
push_files

#!/usr/bin/env bash

# 
# after_success
# deploy gh-pages
#

setup_git() {
    git config --global user.name "Travis CI"
}

add_files() {
    cp -arv docs/build/html/* . \
        | awk -F'->' '{print $2}' \
        | sed "s/[\'\’\ \‘]//g" > /tmp/filelist
    
    for ifile in `cat /tmp/filelist`
    do
        git add ${ifile}
    done
    ! [ -e .nojekyll ] && touch .nojekyll && git add .nojekyll
}

commit_files() {
    git stash
    git config remote.origin.fetch "+refs/heads/*:refs/remotes/origin/*"
    git fetch
    git ls-remote | grep -i "refs/heads/gh-pages"
    if [ $? -ne 0 ]; then
        git checkout --orphan gh-pages
        git rm -rf .
    else
        git checkout -b gh-pages origin/gh-pages
    fi
    add_files
    git commit -m "Update docs by Travis build: $TRAVIS_BUILD_NUMBER"
}

push_files() {
    git remote add pages https://${GITHUB_TOKEN}@github.com/phantasy-project/phantasy.git
    git push --quiet --set-upstream pages gh-pages
}

setup_git
commit_files
push_files

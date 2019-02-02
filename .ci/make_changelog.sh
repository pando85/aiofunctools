#!/bin/bash
set -e

NEW_LOG=$(git log $(git describe --tags --abbrev=0 HEAD^)..HEAD --pretty=format:'- %s'| sort | grep -v Merge | grep -v Release)

echo "# $(git describe --tags --abbrev=0 HEAD)"$'\n'$'\n'"${NEW_LOG}"$'\n'$'\n'"$(cat CHANGELOG.md)" > CHANGELOG.md

if [ ! -z "${TRAVIS_REPO_SLUG}" ]; then
    git config user.name "tracis-ci"
    git config user.email "travis-ci@travis-ci.org"
    git add CHANGELOG.md
    git commit -m 'Update changelog'
    git push "https://$GITHUB_TOKEN@github.com/$TRAVIS_REPO_SLUG" HEAD:$TRAVIS_BRANCH
fi

#!/bin/bash
set -e

check_version_changes(){
    git diff  $(git describe --tags --abbrev=0 HEAD)..HEAD -- aiofunctools/__init__.py | grep --quiet +__version__;
};

if ! check_version_changes; then
    echo "Not version changed"
    exit
fi
VERSION=$(python -c 'import aiofunctools; print(aiofunctools.__version__)')

if [ ! -z "${TRAVIS_REPO_SLUG}" ]; then
    git tag -a $VERSION -m "version $VERSION"
    git push "https://$GITHUB_TOKEN@github.com/$TRAVIS_REPO_SLUG" $VERSION
fi

WORKDIR=$(dirname $(realpath $0))

bash $WORKDIR/make_changelog.sh

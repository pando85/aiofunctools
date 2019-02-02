#!/bin/bash
set -e

if [ -z "${WORKON_HOME}" ]; then
    PIP=.venv/aiofunctools/bin/pip
else
    PIP=$WORKON_HOME/aiofunctools/bin/pip
fi

update_packages(){
    packages=$($PIP list --outdated --local --format=freeze | \
        grep -v '^\-e' | cut -d = -f 1  )

    for package in $(echo $packages);
    do
        $PIP install -U $package;
    done;
};

update_requirements(){
    temp_file=$(mktemp)
    requirements_file=${1:=requirements.txt}
    echo Update $requirements_file
    for i in $(cat $requirements_file);
    do
        package_name=$(echo $i | cut -d'[' -f1 | cut -d= -f1)
        version=$($PIP freeze --local | egrep "^${package_name}" | grep ${package_name}= | cut -d= -f3);
        echo "$(echo $i | cut -d= -f1)==${version}" >> $temp_file;
    done;
    cp $temp_file $requirements_file;
};

echo Update packages
update_packages
update_requirements requirements.txt

if ! git diff --exit-code -- requirements.txt; then
    echo "Updated requirements"
    echo Run unit tests
    make test

    if [ ! -z "${TRAVIS_REPO_SLUG}" ]; then
        git config user.name "tracis-ci"
        git config user.email "travis-ci@travis-ci.org"
        git add requirements.txt
        git commit -m 'Update requirements.txt'
        git push "https://$GITHUB_TOKEN@github.com/$TRAVIS_REPO_SLUG" HEAD:$TRAVIS_BRANCH
    fi
fi

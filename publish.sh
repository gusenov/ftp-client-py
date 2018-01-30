#!/bin/bash
set -x  # echo on

# Usage:
#  $ ./publish.sh
#  $ ./publish.sh --repo=pypi --name=ftpclient
#  $ ./publish.sh -r=testpypi -n=ftpclient

repo="pypi"
package_name="ftpclient"

for i in "$@"
do
case $i in
    -r=*|--repo=*)
        repo="${i#*=}"
        shift # past argument=value
        ;;
    -n=*|--name=*)
        package_name="${i#*=}"
        shift # past argument=value
        ;;
esac
done

read -p "Вы уверены, что хотите провести публикацию $package_name в $repo? " -n 1 -r
echo    # (optional) move to a new line
if [[ $REPLY =~ ^[Yy]$ ]]
then
    pip3 uninstall "$package_name"

    python setup.py sdist upload -r $repo

    if [ "$repo" == "pypi" ]
    then
        pip3 install "$package_name" --user
    elif [ "$repo" == "testpypi" ]
    then
        pip3 install --extra-index-url https://testpypi.python.org/pypi "$package_name" --user
    fi

    pip3 list
    ls ~/.local/lib/python3.5/site-packages/
fi

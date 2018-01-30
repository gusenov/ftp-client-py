# Публикация пакета

```bash
$ cat ~/.pypirc 
[distutils]
index-servers =
    pypi
    testpypi

[pypi]
repository: https://upload.pypi.org/legacy/
username: your username
password: your password

[testpypi]
repository: https://test.pypi.org/legacy/
username: your testpypi username
password: your testpypi password

$ pip3 --version

$ kate setup.py

$ ./publish.sh -r=testpypi -n=ftpclient

$ ./publish.sh --repo=pypi --name=ftpclient
```

# Фиксация изменений

```bash
$ git add .
$ git commit -S -m "0.1"
$ git tag -s v0.1 -m 'signed 0.1 tag'
$ git push --tags com.github.gusenov.ftp-client-py master:master
```

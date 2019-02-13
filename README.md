# pyfmr: a python wrapper for FMR

https://github.com/liuzl/fmr

## how to build

*The cross compiling is done by [xgo](https://github.com/karalabe/xgo).*

### Prerequisites
* Docker
* Golang

### Steps
```sh
# 1. clone the git repo
git clone https://github.com/liuzl/pyfmr && cd pyfmr

# 2. pull xgo docker image
docker pull karalabe/xgo-latest

# 3. install xgo
go get github.com/karalabe/xgo

# 4. build shared libraries
xgo --targets=*/amd64 -buildmode=c-shared -out pyfmr/lib/fmr github.com/liuzl/pyfmr/src

# 5. build wheel
python3 setup.py sdist bdist_wheel

# 6. upload to pypi.org
python3 -m twine upload dist/*
```

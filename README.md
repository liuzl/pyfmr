# pyfmr: a python wrapper for FMR

https://github.com/liuzl/fmr

## how to build

*The cross compiling is done by [xgo](https://github.com/karalabe/xgo).*

### Prerequisites
* Docker
* Golang

### Steps
```sh
# 1. pull xgo docker image
docker pull karalabe/xgo-latest

# 2. install xgo
go get github.com/karalabe/xgo

# 3. build shared libraries
xgo --targets=*/amd64 -buildmode=c-shared -out lib/fmr github.com/liuzl/pyfmr/src
```

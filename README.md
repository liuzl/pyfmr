# pyfmr: a python wrapper for FMR

[https://github.com/liuzl/fmr](https://github.com/liuzl/fmr)

## Usage

[examples](https://github.com/liuzl/pyfmr/tree/master/examples)

### Install pyfmr via pip

```sh
pip install pyfmr
```

### Grammar file

Save the following grammar content to file `sf.grammar`

```fmr
<flight> = <departure> <arrival> {nf.flight($1, $2)};
[flight] = <arrival> <departure> {nf.flight($2, $1)};

<departure> = <from> <city> {nf.I($2)};

<arrival> = <to> <city> {nf.I($2)};
[arrival] = <arrival> {nf.arrival($1)};

<from> = "从" ;

<to> = "到" | "去" | "飞";

<city> = "北京"       {nf.I($@)}
       | "天津"       {nf.I($@)}
       | "上海"       {nf.I($@)}
       | "重庆"       {nf.I($@)}
       | `.(?:城|都)` {nf.I($@)}
       ;

<city_ext> = <city>            {nf.I($1)}
           | (any{1,1}) <city> {nf.I($2)}
           ;

<cities> = "直辖市：" (list<city_ext>) {nf.I($@)};
```

### Python example codes

```py
import pyfmr

p = pyfmr.Parser("./sf.grammar")
strs = [
    "直辖市：北京、上海、天津",
    "直辖市：帝都、津城、魔都",
    "中国现在有四个直辖市：帝都、魔都、天津、重庆。",
    "中国曾经的直辖市：帝都、魔都、天津、重庆、旧都。",
    "天津大学",
]
for l in strs:
    ret = p.extract(l, "cities")
    for item in ret:
        print(item)
    print("="*80)
```

## How to build

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

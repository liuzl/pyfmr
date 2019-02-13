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


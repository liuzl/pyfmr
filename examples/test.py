import pyfmr
import sys


def no_grammar_file():
    p = pyfmr.Parser("./cities.grammarx")
    if p.grammar_index < 0:
        print(p.error_message)
        return

def extractx():
    p = pyfmr.Parser("./sf.grammar")
    if p.grammar_index < 0:
        print(p.error_message)
        return

    strs = [
        "直辖市：北京、上海、天津",
        "直辖市：帝都、津城、魔都",
        "中国现在有四个直辖市：帝都、魔都、天津、重庆。",
        "中国曾经的直辖市：帝都、魔都、天津、重庆、旧都。",
        "天津大学",
    ]

    for l in strs:
        ret = p.extractx(l, "cities")
        print("NL:[%s], LF:[%s]" % (l, ret))
        print("="*80)

def frames():
    p = pyfmr.Parser("./sf.grammar")
    if p.grammar_index < 0:
        print(p.error_message)
        return

    strs = [
        '从上海到天津的机票',
        '到重庆，明天，从北京',
        '到上海去',
    ]

    for l in strs:
        ret = p.frames(l)
        print("NL:[%s], LF:[%s]" % (l, ret))
        print("="*80)

if __name__ == "__main__":
    no_grammar_file()
    extractx()
    frames()

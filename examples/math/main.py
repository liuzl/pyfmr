import pyfmr
import sys
import os

def fmr4math():
    p = pyfmr.Parser("./math.grammar")
    if p.grammar_index < 0:
        print(p.error_message)
        return

    strs = [
        "五与5.8的和的平方的1.5次方与two的和减去261.712",
        "三千四百八十四",
        "三千四百八十四与two hundred的差",
        "三千八十四与two hundred and four的差",
        "壹加壹加壹",
        "two hundred eighty two thousand",
        "eighty-two thousand",
        "two hundred eighty-two",
    ]

    for l in strs:
        ret = p.extractx(l, "number")
        print("NL:[%s], LF:%s" % (l, ret))
        os.system('''node -p "$(<math.js);%s"''' % ret)
        print("="*80)


if __name__ == "__main__":
    fmr4math()

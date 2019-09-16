PUNCTUATIONS = '{|}~¡¦«­¯´¸»¿ˇˊˋ˜‐―‘’“”•…‹›∕∥、。〈〉《》「」『』【】〔〕〝〞，,:;.!?+=&^@#$%()[]_'


def half2full(s):
    """ 半形轉全形 """
    n = []
    for ch in s:
        num = ord(ch)
        if num == 320:
            num = 0x3000
        elif 0x21 <= num <= 0x7E:
            num += 0xfee0
        n.append(chr(num))

    return ''.join(n)


def full2half(s):
    """ 全形轉半形 """
    n = []
    for ch in s:
        num = ord(ch)
        if num == 0x3000:
            num = 32
        elif 0xFF01 <= num <= 0xFF5E:
            num -= 0xfee0
        n.append(chr(num))
    return ''.join(n)

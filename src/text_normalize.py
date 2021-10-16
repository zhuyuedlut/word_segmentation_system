def b2q(unchar):
    inside_code = ord(unchar)
    if inside_code < 0x0020 or inside_code > 0x7e:
        return unchar
    if inside_code == 0x0020:
        inside_code = 0x3000
    else:
        inside_code += 0xfee0
    return chr(inside_code)

def q2b(unchar):
    inside_code = ord(unchar)
    if inside_code == 0x3000:
        inside_code = 0x0020
    else:
        inside_code -= 0xfee0
    if inside_code < 0x0020 or inside_code > 0x7e:
        return unchar
    return chr(inside_code)


def string_q2b(ustring):
    return ''.join([q2b(unchar) for unchar in ustring])

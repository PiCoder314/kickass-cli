def pad(string, length, char):
    if not string:
        return str(string)
    string = string.replace("\n", "")
    l1 = len(string)
    if len(string) >= length:
        return string[:length-3] + '...'
    res = string
    for _ in range(length-l1):
        res += char
    return res

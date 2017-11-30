from pwn import *

context.arch = 'amd64'
local = True
if local:
    r = process('./rop_revenge')
else:
    r = remote('ctf.adl.csie.ncu.edu.tw', 11009)


r.sendline(payload)
r.interactive()

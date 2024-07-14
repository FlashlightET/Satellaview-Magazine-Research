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

new_rom=list(q)


#blank out text table
for i in range(int('A400',16),int('FFAF',16),1):
    new_rom[i]=255

strings=[
    "Massive Yoshi Yokohama",
    "Big ol' yoshi in the street!",
    "Yoshi's here, you will tremble in fear.",
    "Beppins",
    "Ohio beppins",
    "ummmmm that just happened",
    "ok so basically im monky",
    "??????",
    "skibidi rizz",
    "キタキツネ",
    "北狐",
    "Ezo Red Fox",
    "FELLAS?"
    ]

strings_ready=[]
for i in strings:
    strings_ready.extend(i.encode('shift-jis'))
    strings_ready.append(0x0D)  # '\r' in bytes

print(strings_ready)
i2=0
for i in range(int('A400',16),int('FFAF',16),1):
    if i2<len(strings_ready):
        new_rom[i]=strings_ready[i2]
    else:
        new_rom[i]=strings_ready[i2 % len(strings_ready)]
    i2+=1
    




for i in range(int('8C00',16),int('A400',16),32):
    
    data=[int(i2) for i2 in q[i:i+32]]
    #print(' '.join([better_hex(i2) for i2 in data]))
    page_number=data[0]
    displayed_image=data[3]
    image_x=data[5]
    image_y=data[7]
    text_display_mode=data[9]
    heading_text_id=data[10]
    body_text_id=data[12]
    other_text_id=data[14]

    

   # print('------------------------------------------')
    #print('PAGE NUMBER:',page_number)
   # print('DISPLAYED IMAGE:',displayed_image)
    #print('IMAGE X,Y:',image_x,image_y)
    #print('TEXT DISPLAY MODE',text_display_mode)
    #print('')
    actualpointer=get_pointer_to_actual_text(heading_text_id)
    #print('HEADER TEXT\n',read_text(int(actualpointer,16)).replace('\r','\n')) #simply for display
    actualpointer=get_pointer_to_actual_text(body_text_id)
    #print('BODY TEXT\n',read_text(int(actualpointer,16)).replace('\r','\n'))
    actualpointer=get_pointer_to_actual_text(other_text_id)
    #print('BOTTOM TEXT\n',read_text(int(actualpointer,16)).replace('\r','\n'))


with open('new_rom.bs','wb') as f:
    f.write(bytes(new_rom))

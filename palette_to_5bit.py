with open('custom_palette.txt') as f:
    q=f.readlines()

#clean up newlines
q=[i.strip('\r\n') for i in q]
q=[i.strip('\n') for i in q]
q=[i.strip('\r') for i in q]

palette=''


for i in q:
    r=i[0:2]
    g=i[2:4]
    b=i[4:6]
    #print(r,g,b)
    #now convert these to BGR555
    #which is obviously 0BBBBBGGGGGRRRRR
    r_5bit=bin(int(r,16) >> 3)[2:].zfill(5)
    g_5bit=bin(int(g,16) >> 3)[2:].zfill(5)
    b_5bit=bin(int(b,16) >> 3)[2:].zfill(5)
    BGR555='0'+b_5bit+g_5bit+r_5bit
    #print(BGR555)
    color_16bit=hex(int(BGR555,2))[2:].upper().zfill(4)
    #print(color_16bit)
    color_final=color_16bit[2:]+color_16bit[:2]
    print(color_final)
    palette+=color_final
print(palette)

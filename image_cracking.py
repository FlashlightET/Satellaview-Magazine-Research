with open('test_image_in.bin','rb') as f:
    q=f.read()

the_all=''

for i in q:
    the_all+=bin(i)[2:].zfill(8)

woo=[]

for i in range(0,len(the_all),5):
    hah=the_all[i:i+5]
    woo.append(int(hah,2))

with open('ttttt.bin','wb') as f:
    f.write(bytes(woo))
    
    

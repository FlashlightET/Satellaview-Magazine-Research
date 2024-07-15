selected_menu=0
selected_menu_item=0
selected_screen_event=0
import os
import json
import pygame

with open('np_1.bs','rb') as f:
    q=f.read()

text_pointer_start=int('A402',16)
text_pointer_end=int('A4D0',16)

screen_headers_start=int('5400',16)
screen_headers_end=int('7400',16)


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
    try:
        return bytes(tx).decode('shift-jis')
    except:
        return bytes(tx).decode('shift-jis', errors='ignore')
            

def read_text2(offset):
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



def decode_screens():
    screens=[]
    for i in range(screen_headers_start,screen_headers_end,240):
        #5400: what is nintendo power
        #   +00: header xpos
        #	+01: header ypos (note: 18 covers the bottom bar, but it gets overwritten with the prompts)
        #	+02: header width
        #	+03: header height
        #	+04: header border
        #	
        #	+10: body xpos
        #	+11: body ypos
        #	+12: body width
        #	+13: body height
        #	+14: body border
        #	
        #	+28: number of pages
        #	
        #	+30 and so on: page ids ended with FE FF
        
        data=q[i:i+240]
        data_dict={'header': {},'body': {}, 'other': {}, 'page_ids': []}
        data_dict['header']['xpos']=int(data[0])
        data_dict['header']['ypos']=int(data[1])
        data_dict['header']['width']=int(data[2])
        data_dict['header']['height']=int(data[3])
        data_dict['header']['border']=int(data[4])
        
        data_dict['body']['xpos']=int(data[8+0])
        data_dict['body']['ypos']=int(data[8+1])
        data_dict['body']['width']=int(data[8+2])
        data_dict['body']['height']=int(data[8+3])
        data_dict['body']['border']=int(data[8+4])

        data_dict['other']['xpos']=int(data[16+0])
        data_dict['other']['ypos']=int(data[16+1])
        data_dict['other']['width']=int(data[16+2])
        data_dict['other']['height']=int(data[16+3])
        data_dict['other']['border']=int(data[16+4])

        data_dict['page_count']=int(data[32+8])

        for i2 in range(12*8):
            true_i2=48+(i2*2)
            data_dict['page_ids']=data_dict['page_ids']+[[data[true_i2],data[true_i2+1]]]
            
        screens.append(data_dict)
        #print(json.dumps(data_dict,indent=4))
    return screens

    
def decode_pages():
    pages=[]

    for i in range(int('8C00',16),int('A400',16),32):
        data=[int(i2) for i2 in q[i:i+32]]
        page_number=data[0]
        displayed_image=data[3]
        image_x=data[5]
        image_y=data[7]
        text_display_mode=data[9]
        heading_text_id=data[10]
        body_text_id=data[12]
        other_text_id=data[14]

        data_dict={'page_number': page_number, 'display_mode': text_display_mode, 'image': {}}
        data_dict['image']['id']=displayed_image
        data_dict['image']['x']=image_x
        data_dict['image']['y']=image_y
        data_dict['header']=heading_text_id
        data_dict['body']=body_text_id
        data_dict['other']=other_text_id

        pages.append(data_dict)
        #print(json.dumps(data_dict,indent=4))
    return pages

def decode_texts():
    texts={}
    for i in range(text_pointer_start,text_pointer_end,2):
        pt1=q[i]
        pt2=q[i+1]
        pt=int(better_hex(pt2)+better_hex(pt1),16)
        texts[better_hex(pt2)+better_hex(pt1)]=read_text(pt).split('\r')
    return texts

#menus start at 7400H, end at 8C00H, and are 304D (130H) long
menu_start=int('7400',16)
menu_end=int('8C00',16)
menus={}

for i in range(menu_start,menu_end,304):
    data=q[i:i+304]
    pees=[]
    pee=[]
    for i2 in data:
        if i2==00 or i2==255:
            pees.append(bytes(pee).decode('shift-jis'))
            #print(bytes(pee).decode('shift-jis'))
            pee=[]
        else:
            #print(bytes(pee).decode('shift-jis'))
            pee.append(i2)
    #print(pees)
    #menus[str(i)]=pee
    
#print(json.dumps(menus,indent=4))

print('ok')





def update_fps():
    fps = str(int(clock.get_fps()))+' FPS'
    fps_text = font.render(fps, 1, pygame.Color("blue"))
    return fps_text

def int_to_bs_hex(_nm):
    _hx=hex(_nm)[2:].upper().zfill(4)
    return _hx[2:]+_hx[:2]

def save_rom():
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
        with open('edited_bs.bs','wb') as f:
            f.write(bytes(new_file))

menu_headers_start=int('7400',16)
menu_headers_end=int('8C00',16)

def zoop(_tx):
    true_tx=[]
    for _i in _tx:
        if _i==0:
            break
        if _i==255:
            break
        true_tx.append(_i)
    return true_tx

def decode_menus():
    menus=[]
    for i in range(menu_headers_start,menu_headers_end,304):

##        Menus are 304 (decimal, 130 hex) bytes long starting at 7400 (hex) and ending at 8C00 (hex)
##        Each string is terminated with 00.
##
##        MENU HEADER: Offset is $00 and length 38d
##        NUM OPTIONS: Offset is $26 and length 1d
##        MENU OPTIONS: Starting from offset $27, they are 35 bytes long and terminated with 00.
##                Option 1: $27
##                Option 2: $4A
##                Option 3: $6D
##                Option 4: $90
##                Option 5: $B3
##                Option 6: $D6
##                Option 7: $F9
##        OPTION LINKS:
##                $11C: Option 1 links to this screen
##                $11D: Option 2
##                $11E: 3
##                $11F: 4
##                $120: 5
##                $121: 6
##                $122: 7
##        The rest are 00.
        
        data=q[i:i+304]
        data_dict={'header': {},'options': [], 'option_count': 0}
        zooped=zoop(data[1:38])
        zooped=bytes(zooped).decode('shift-jis')
        #print(zooped)
        data_dict['header']=zooped
        data_dict['option_count']=data[int('26',16)]

        for elm in range(7):
            zooped=zoop(data[int('27',16)+(35*elm):int('27',16)+(35*elm)+35])
            zooped=bytes(zooped).decode('shift-jis')
            data_dict['options'].append([zooped,None])

        data_dict['options'][0][1]=data[int('11C',16)]
        data_dict['options'][1][1]=data[int('11D',16)]
        data_dict['options'][2][1]=data[int('11E',16)]
        data_dict['options'][3][1]=data[int('11F',16)]
        data_dict['options'][4][1]=data[int('120',16)]
        data_dict['options'][5][1]=data[int('121',16)]
        data_dict['options'][6][1]=data[int('122',16)]

        
        menus.append(data_dict)
        #print(json.dumps(data_dict,indent=4))
    return menus

#print(decode_menus())
#breakIt



pygame.init()

screen = pygame.display.set_mode((1024, 768))
pygame.scrap.init()
clock = pygame.time.Clock()

font = pygame.font.Font(r'C:\Windows\Fonts\msgothic.ttc', 14)

font2 = pygame.font.Font(r'C:\Windows\Fonts\msgothic.ttc', 12)

#screen.fill("#FFFFFF")

running=True

mode='menus'

selected_page=2
selected_text=0
selected_screen=0

current_column=0
cl_sel=0

text_submode=False

text_editing_line=0
text_editing_char=0

#debug
#current_column=1
#text_submode=True

ref=pygame.image.load('ref_towa.png')

ref=pygame.image.load('preview_background.png')

border_white_empty=pygame.image.load('textback_border_empty.png')
border_orange_empty=pygame.image.load('textback_orange_empty.png')
border_empty_empty=None

border_white_transparent=pygame.image.load('textback_border_transparent.png')
border_orange_transparent=pygame.image.load('textback_orange_transparent.png')
border_empty_transparent=pygame.image.load('textback_transparent.png')

border_white_black=pygame.image.load('textback_border_black.png')
border_orange_black=pygame.image.load('textback_orange_black.png')
border_empty_black=pygame.image.load('textback_black.png')





while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                #print(selected_page)
                #print(len(pages))
                if mode=='pages' and current_column==0: selected_page=min(len(pages)-1,selected_page+1)
                if mode=='texts' and current_column==0: selected_text=min(len(texts)-1,selected_text+1)
                if mode=='screens' and current_column==0: selected_screen=min(len(screens)-1,selected_screen+1)
                if mode=='screens' and current_column==2: selected_screen_event=min(24,selected_screen_event+1)
                if mode=='menus' and current_column==0: selected_menu=min(len(menus),selected_menu+1)
                if mode=='menus' and current_column==2: selected_menu_item=min(7,selected_menu_item+1)
                if current_column==1: cl_sel+=1
                if not text_submode:
                    text_editing_line=0
                    text_editing_char=0
                
            if event.key == pygame.K_UP:
                #print(selected_page)
                #print(len(pages))
                if mode=='pages' and current_column==0: selected_page=max(0,selected_page-1)
                if mode=='texts' and current_column==0: selected_text=max(0,selected_text-1)
                if mode=='screens' and current_column==0: selected_screen=max(0,selected_screen-1)
                if mode=='screens' and current_column==2: selected_screen_event=max(0,selected_screen_event-1)
                if mode=='menus' and current_column==0: selected_menu=max(0,selected_menu-1)
                if mode=='menus' and current_column==2: selected_menu_item=max(0,selected_menu_item-1)
                
                if current_column==1: cl_sel+=-1
                if not text_submode:
                    text_editing_line=0
                    text_editing_char=0

            if event.key == pygame.K_RIGHT:
                #print(selected_page)
                #print(len(pages))
                if mode=='screens': current_column=min(2,current_column+1)
                if mode=='pages': current_column=min(2,current_column+1)
                if not text_submode:
                    if mode=='texts': current_column=min(1,current_column+1)
                if mode=='menus': current_column=min(2,current_column+1)

            if event.key == pygame.K_INSERT:
                if mode=='screens':
                    mode='pages'
                elif mode=='pages':
                    mode='texts'
                elif mode=='menus':
                    mode='screens'
                cl_sel=0
                current_column=0

            if event.key == pygame.K_DELETE:
                if mode=='texts':
                    mode='pages'
                elif mode=='pages':
                    mode='screens'
                elif mode=='screens':
                    mode='menus'
                cl_sel=0
                current_column=0

            
                

            if event.key == pygame.K_LEFT:
                #print(selected_page)
                #print(len(pages))
                if not text_submode: current_column=max(0,current_column-1)


            if event.key == pygame.K_HOME: #bizarrely, this is the key i chose to save the rom...
                save_rom()

            #if event.key == pygame.K_END: #quick swap for proof of concept
            #   mode='texts' if mode=='pages' else 'pages'

            
            if mode=='pages':
                if current_column==1:
                    tochange=None
                    if cl_sel<0: cl_sel=0
                    if cl_sel>3: cl_sel=3
                    if cl_sel==0: tochange=10
                    if cl_sel==1: tochange=12
                    if cl_sel==2: tochange=14
                    if cl_sel==3: tochange=0
                    #change header text id
                    addr=int('8C00',16)+(32*selected_page)+tochange
                    UGH=list(q)
                    if event.key == pygame.K_PAGEUP:   UGH[addr]=min(UGH[addr]+1,255)
                    if event.key == pygame.K_PAGEDOWN: UGH[addr]=max(UGH[addr]-1,  0)
                    q=bytes(UGH)

            if mode=='menus':
                if current_column==1:
                    tochange=None
                    if cl_sel<0: cl_sel=0
                    if cl_sel>1: cl_sel=1
                    if cl_sel==1: tochange=int('26',16)
                    if cl_sel==0:
                        tochange=int('11C',16)+selected_menu_item



                    addr=int('7400',16)+(304*selected_menu)+tochange
                    UGH=list(q)
                    if event.key == pygame.K_PAGEUP:   UGH[addr]=min(UGH[addr]+1,255)
                    if event.key == pygame.K_PAGEDOWN: UGH[addr]=max(UGH[addr]-1,  0)
                    q=bytes(UGH)

            if mode=='screens':
                if current_column==1:
                    tochange=None
                    if cl_sel<0: cl_sel=0
                    if cl_sel== 0: tochange= 0
                    if cl_sel== 1: tochange= 1
                    if cl_sel== 2: tochange= 2
                    if cl_sel== 3: tochange= 3
                    if cl_sel== 4: tochange= 4

                    if cl_sel== 5: tochange= 8
                    if cl_sel== 6: tochange= 9
                    if cl_sel== 7: tochange= 10
                    if cl_sel== 8: tochange= 11
                    if cl_sel== 9: tochange= 12
                    
                    
                    if cl_sel==10: tochange=16
                    if cl_sel==11: tochange=17
                    if cl_sel==12: tochange=18
                    if cl_sel==13: tochange=19
                    if cl_sel==14: tochange=20
                    if cl_sel==15: tochange=int('28',16)
                    
                    if cl_sel==16: tochange=int('30',16)+(selected_screen_event*2)
                    if cl_sel==17: tochange=int('30',16)+(selected_screen_event*2)+1
                    if cl_sel>17: cl_sel=17
                    
                    addr=int('5400',16)+(240*selected_screen)+tochange
                    UGH=list(q)
                    if event.key == pygame.K_PAGEUP:   UGH[addr]=min(UGH[addr]+1,255)
                    if event.key == pygame.K_PAGEDOWN: UGH[addr]=max(UGH[addr]-1,  0)
                    q=bytes(UGH)
                

            if mode=='texts':
                
                if current_column==1:
                    if event.key == pygame.K_RETURN:
                        text_submode=True
                    if event.key == pygame.K_ESCAPE:
                        text_submode=False

                    #hacky way to detect letters pressed without a million if statements
                    key_name=pygame.key.name(event.key)
                    pressed = pygame.key.get_pressed()
                    shifted=False
                    for i in pressed:
                        if 'shift' in pygame.key.name(i): shifted=True
                        
                    if len(key_name)==1:
                        ln=texts_working[selected_text][text_editing_line]
                        texts_working[selected_text][text_editing_line]=ln[:text_editing_char]+(key_name.upper() if shifted else key_name)+ln[text_editing_char+1:]
                        text_editing_char+=1
                    if event.key == pygame.K_SPACE:
                        ln=texts_working[selected_text][text_editing_line]
                        texts_working[selected_text][text_editing_line]=ln[:text_editing_char]+' '+ln[text_editing_char+1:]
                        text_editing_char+=1
                    #print('stop indenting me')

                    #now, insert text back into rom and repoint

                    #copying these for note
                    #text_pointer_start=int('A402',16)
                    #text_pointer_end=int('A4D0',16) -- this is also where the actual texts start.

                    text_data_encoded=[]
                    offsets=[]
                    offset=int('A4D0',16)
                    for text in texts_working:
                        offsets.append(int_to_bs_hex(offset))
                        true_text='\r'.join(text)

                        true_text_encoded=true_text.encode('shift-jis')

                        for i in true_text_encoded:
                            #print(i)
                            #print(int(i))
                            text_data_encoded.append(int(i))
                            offset+=1
                        text_data_encoded.append(0)
                        offset+=1
                        
                        #print(int_to_bs_hex(offset))
                    #print(offsets)
                    #the offsets is a 1:1 match (start with D0A4 end with 7FFC)
                    #in the str output
                    #so thats a good sign

                    offsets_binary=[]
                    for i in offsets:
                        offsets_binary.append(int(i[:2],16))
                        offsets_binary.append(int(i[2:],16))
                    #print(offsets_binary)

                    #now lets insert the data back into rom
                    rom_working=list(q)
                    #insert the pointers
                    offset=text_pointer_start
                    #todo: might break later so check this first if
                    #things start breaking when adding text length
                    #changing
                    for i in offsets_binary:
                        rom_working[offset]=i
                        offset+=1
                    #insert actual text data
                    offset=text_pointer_end
                    for i in text_data_encoded:
                        rom_working[offset]=i
                        offset+=1
                    #propagate working rom back to rom
                    q=bytes(rom_working)
                    
                if text_submode==False:
                    if event.key == pygame.K_d:
                        #dump texts
                        try:
                            os.mkdir('texts')
                        except:
                            pass
                        i2=0
                        for i in texts_working:
                            dat='\r'.join(i)
                            with open(os.path.join('texts',f'{str(i2).zfill(4)}.txt'),'wb') as f:
                                f.write(dat.encode('shift-jis'))
                            i2+=1
                        print('texts dumped')
                    if event.key == pygame.K_l:
                        #load texts
                        loaded_texts=[]
                        i2=0
                        for i in os.listdir('texts'):
                            with open(os.path.join('texts',f'{str(i2).zfill(4)}.txt'),'rb') as f:
                                dat=f.read().decode('shift-jis')
                            loaded_texts.append(dat.split('\r'))
                            i2+=1
                        print('texts loaded into temp')


                        #now, insert text back into rom and repoint

                        #copying these for note
                        #text_pointer_start=int('A402',16)
                        #text_pointer_end=int('A4D0',16) -- this is also where the actual texts start.

                        text_data_encoded=[]
                        offsets=[]
                        offset=int('A4D0',16)
                        for text in loaded_texts:
                            offsets.append(int_to_bs_hex(offset))
                            true_text='\r'.join(text)

                            true_text_encoded=true_text.encode('shift-jis')

                            for i in true_text_encoded:
                                #print(i)
                                #print(int(i))
                                text_data_encoded.append(int(i))
                                offset+=1
                            text_data_encoded.append(0)
                            offset+=1
                            
                            #print(int_to_bs_hex(offset))
                        #print(offsets)
                        #the offsets is a 1:1 match (start with D0A4 end with 7FFC)
                        #in the str output
                        #so thats a good sign

                        offsets_binary=[]
                        for i in offsets:
                            offsets_binary.append(int(i[:2],16))
                            offsets_binary.append(int(i[2:],16))
                        #print(offsets_binary)

                        #now lets insert the data back into rom
                        rom_working=list(q)
                        #insert the pointers
                        offset=text_pointer_start
                        #todo: might break later so check this first if
                        #things start breaking when adding text length
                        #changing
                        for i in offsets_binary:
                            rom_working[offset]=i
                            offset+=1
                        #insert actual text data
                        offset=text_pointer_end
                        for i in text_data_encoded:
                            rom_working[offset]=i
                            offset+=1
                        #propagate working rom back to rom
                        q=bytes(rom_working)

                        print('texts loaded')

            if mode=='menus':
                if text_submode==False:
                    if event.key == pygame.K_d:
                        #dump texts
                        try:
                            os.mkdir('menus')
                        except:
                            pass
                        i2=0
                        for i in menus:
                            dat=i['header']+'\r'+('\r'.join([br[0] for br in i['options']]))
                            with open(os.path.join('menus',f'{str(i2).zfill(4)}.txt'),'wb') as f:
                                f.write(dat.encode('shift-jis'))
                            i2+=1
                        print('menus dumped')
                        
                    if event.key == pygame.K_l:
                        #load texts
                        loaded_menus=[]
                        i2=0
                        for i in os.listdir('menus'):
                            with open(os.path.join('menus',f'{str(i2).zfill(4)}.txt'),'rb') as f:
                                dat=f.read().decode('shift-jis')
                            loaded_menus.append(dat.split('\r'))
                            i2+=1
                        print('menus loaded into temp')


                        #now, insert menus back into rom

                        #copying these for note
                        ##        Menus are 304 (decimal, 130 hex) bytes long starting at 7400 (hex) and ending at 8C00 (hex)
                        ##        Each string is terminated with 00.
                        ##
                        ##        MENU HEADER: Offset is $01 and length 37d
                        ##        NUM OPTIONS: Offset is $26 and length 1d
                        ##        MENU OPTIONS: Starting from offset $27, they are 35 bytes long and terminated with 00.
                        ##                Option 1: $27
                        ##                Option 2: $4A
                        ##                Option 3: $6D
                        ##                Option 4: $90
                        ##                Option 5: $B3
                        ##                Option 6: $D6
                        ##                Option 7: $F9
                        ##        OPTION LINKS:
                        ##                $11C: Option 1 links to this screen
                        ##                $11D: Option 2
                        ##                $11E: 3
                        ##                $11F: 4
                        ##                $120: 5
                        ##                $121: 6
                        ##                $122: 7
                        ##        The rest are 00.

                        rom_working=list(q)
                        menu_num=0
                        offset=int('7400',16)
                        for menu in loaded_menus:
                            offset=int('7400',16)+(304*menu_num)
                            hoo=menu[0].encode('shift-jis')
                            i2=0
                            for i in range(offset+1,offset+1+len(hoo)):
                                rom_working[i]=hoo[i2]
                                i2+=1

                            for opt in range(7):
                                offset=int('7400',16)+(304*menu_num)+int('27',16)+(35*opt)
                                hoo=list(menu[1+opt].encode('shift-jis'))
                                hoo.append(0)
                                hoo=bytes(hoo)
                                i2=0
                                for i in range(offset,offset+len(hoo)):
                                    rom_working[i]=hoo[i2]
                                    i2+=1



                            menu_num+=1





                        q=bytes(rom_working)

                        
                        

                    
                    
                        
        
            
    screen.fill("#FFFFFF")
    screen.blit(update_fps(), (0,0))
    if mode=='texts':
        current_column=min(1,current_column)
        
        #note for later: if i edit the text it will be as simple as repointing
        #so theres the "texts" dict
        #each entry is a list of the lines
        #when inserting back into rom, join those lists via carriage returns
        #so make a list containing the bytes for each entry terminated with 00
        #keep track of their offsets in another list and insert them (byte-swapped) into the pointer table 
        texts=decode_texts()
        texts_working=[]
        
        for i in texts:
            texts_working.append(texts[i])
            #print(texts_working)
        
        scrollamt=0
        if selected_text>20: scrollamt=(selected_text-20)*16

        #render the text list
        i2=0
        for i in texts:
            g=texts[i][0]
            text = font.render(g, 1, pygame.Color("white" if i2==selected_text else "black"))
            if i2==selected_text: pygame.draw.rect(screen, '#0000FF', (16,16+i2*16 - scrollamt,292,16))
            screen.blit(text, (16, 16 + i2*16 - scrollamt ))
            i2+=1


        #render the text preview
        #background
        pygame.draw.rect(screen, '#AFAFAF', (692,16,270,720))
        #texts
        i2=0
        BALLS=list(texts.keys()) #its really stupid that i have to list() it first
        for i in texts_working[selected_text]:
            g=str(i)
            text = font.render(g, 1, pygame.Color("white" if i2==text_editing_line else "black"))
            pygame.draw.rect(screen, '#0000FF' if i2==text_editing_line else '#FFFFFF', (692,16+i2*16,270,16))
            screen.blit(text, (700, 16 + i2*16 ))
            #hacky way to draw cursor
            if i2==text_editing_line:
                #print(g[:text_editing_char]+'_')
                text = font.render(g[:text_editing_char]+'_', 1, pygame.Color("white" if i2==text_editing_line else "black"))
                screen.blit(text, (700, 16 + i2*16 ))

            
            #print(i)
            i2+=1



        #draw frames
        #column 0
        #masking
        pygame.draw.rect(screen, '#FFFFFF', (16,0,292,16))
        pygame.draw.rect(screen, '#FFFFFF', (16,736,292,32))
        #text
        text = font.render('Text Selection', 1, pygame.Color("black"))
        screen.blit(text, (16*7, 0))
        #box
        pygame.draw.rect(screen, '#0000FF' if (current_column==0) else '#000000', (16,16,292,720),width=1+(1*(current_column==0)))

        #column 1
        pygame.draw.rect(screen, '#0000FF' if (current_column==1) else '#000000', (692,16,270,720),width=1+(1*(current_column==1)))

        #draw note
        text = font.render('NOTE:', 1, pygame.Color("black"))
        screen.blit(text, (16*21, 16*1))
        note_text=[
            'I highly recommend dumping and loading',
            'the texts to/from txt files, due to the',
            'fact that this editor does not support',
            'inserting Japanese characters, which is',
            'needed for the fullwidth space character.',
            'Among other quirks with this text editor.',
            '',
            'With the textbox unselected:',
            '  Press D to dump to TXT',
            '  Press L to load from TXT',
            '',
            'This will dump all texts to numbered files.',
            'Remember to keep encoding as Shift-JIS,',
            'with carriage return (0x0D, \\r) as the',
            'newline character.',
            ]
        i2=0
        for line in note_text:
            text = font.render(line, 1, pygame.Color("black"))
            screen.blit(text, (16*21, 16*(2+i2)))
            i2+=1



    if mode=='pages':
        pages=decode_pages()

        
        

        #text = font.render(str(pages[selected_page]), 1, pygame.Color("black"))
        #screen.blit(text, (16, 0 ))

        scrollamt=0
        if selected_page>20: scrollamt=(selected_page-20)*16
        i2=0
        for i in pages:
            actualpointer=int(get_pointer_to_actual_text(i['header']),16)
            g=f'{read_text(actualpointer)} ({str(i["page_number"]).zfill(2)})'
            text = font.render(g, 1, pygame.Color("white" if i2==selected_page else "black"))
            if i2==selected_page: pygame.draw.rect(screen, '#0000FF', (16,16+i2*16 - scrollamt,292,16))
            screen.blit(text, (16, 16 + i2*16 - scrollamt ))
            i2+=1
        #print(pages[selected_page])
        #print('LENGTH OF PAGES IS',len(pages))
        #print('SELECTED PAGE IS',selected_page)
        #print('SELECTED PAGE IS LESS THAN LEN PAGES?',selected_page<len(pages))
        
        actualpointer=int(get_pointer_to_actual_text(pages[selected_page]['header']),16)
        text = font.render(read_text(actualpointer), 1, pygame.Color("black"))
        screen.blit(text, (700, 16 ))
        
        text = font.render('Header text', 1, pygame.Color("black"))
        screen.blit(text, (600, 16 ))

        actualpointer=int(get_pointer_to_actual_text(pages[selected_page]['body']),16)
        text = read_text(actualpointer)
        actualtext=text.split('\r')

        
        
        i2=0

        text = font.render('Body text', 1, pygame.Color("black"))
        screen.blit(text, (600, 48 + i2*16 ))
        
        for i in actualtext:
            #print(i)
            g=i
            text = font.render(g, 1, pygame.Color("black"))
            screen.blit(text, (700, 48 + i2*16 ))
            i2+=1
        i2+=1
        actualpointer=int(get_pointer_to_actual_text(pages[selected_page]['other']),16)
        text = read_text(actualpointer)
        actualtext=text.split('\r')
        
        text = font.render('Other text', 1, pygame.Color("black"))
        screen.blit(text, (600, 48 + i2*16 ))
        
        for i in actualtext:
            #print(i)
            g=i
            text = font.render(g, 1, pygame.Color("black"))
            screen.blit(text, (700, 48 + i2*16 ))
            i2+=1

        text = font.render('Page ID:', 1, pygame.Color("black"))
        screen.blit(text, (340, 16*1 ))
        text = font.render(str(selected_page), 1, pygame.Color("black"))
        screen.blit(text, (340, 16*2 ))

        text = font.render('Header text ID:', 1, pygame.Color("black"))
        screen.blit(text, (340, 16*4 ))
        pygame.draw.rect(screen, '#0000FF' if (current_column==1 and cl_sel==0) else '#000000', (338,16*5,32,16),width=1+(1*(current_column==1 and cl_sel==0)))
        text = font.render(str(pages[selected_page]['header']), 1, pygame.Color("black"))
        screen.blit(text, (340, 16*5 ))

        text = font.render('Body text ID:', 1, pygame.Color("black"))
        screen.blit(text, (340, 16*7 ))
        pygame.draw.rect(screen, '#0000FF' if (current_column==1 and cl_sel==1) else '#000000', (338,16*8,32,16),width=1+(1*(current_column==1 and cl_sel==1)))
        text = font.render(str(pages[selected_page]['body']), 1, pygame.Color("black"))
        screen.blit(text, (340, 16*8 ))

        text = font.render('Footer text ID:', 1, pygame.Color("black"))
        screen.blit(text, (340, 16*10 ))
        pygame.draw.rect(screen, '#0000FF' if (current_column==1 and cl_sel==2) else '#000000', (338,16*11,32,16),width=1+(1*(current_column==1 and cl_sel==2)))
        text = font.render(str(pages[selected_page]['other']), 1, pygame.Color("black"))
        screen.blit(text, (340, 16*11 ))

        text = font.render('Page No:', 1, pygame.Color("black"))
        screen.blit(text, (340, 16*13 ))
        pygame.draw.rect(screen, '#0000FF' if (current_column==1 and cl_sel==3) else '#000000', (338,16*14,32,16),width=1+(1*(current_column==1 and cl_sel==3)))
        text = font.render(str(pages[selected_page]['page_number']), 1, pygame.Color("black"))
        screen.blit(text, (340, 16*14 ))

        
        
        #draw frames
        #column 0
        #masking
        pygame.draw.rect(screen, '#FFFFFF', (16,0,292,16))
        pygame.draw.rect(screen, '#FFFFFF', (16,736,292,32))
        #text
        text = font.render('Page Selection', 1, pygame.Color("black"))
        screen.blit(text, (16*7, 0))
        #box
        pygame.draw.rect(screen, '#0000FF' if (current_column==0) else '#000000', (16,16,292,720),width=1+(1*(current_column==0)))

    if mode=='screens':
        pages=decode_pages()
        screens=decode_screens()
        #print(screens)
        
        scrollamt=0
        if selected_screen>20: scrollamt=(selected_screen-20)*16
        i2=0
        for i in screens:
            grrg=i["page_ids"][0][0]
            #print(pages)
            if grrg<len(pages):
                actualpointer=int(get_pointer_to_actual_text(+pages[grrg]['header']),16)
                g=read_text(actualpointer)+' pg. '+str(pages[grrg]['page_number'])
            else:
                g='OUT OF RANGE'
            #g=str().zfill(2)
            text = font.render(g, 1, pygame.Color("white" if i2==selected_screen else "black"))
            if i2==selected_screen: pygame.draw.rect(screen, '#0000FF', (16,16+i2*16 - scrollamt,292,16))
            screen.blit(text, (16, 16 + i2*16 - scrollamt ))
            i2+=1

        i2=0
        for i in screens[selected_screen]['page_ids']:
            g=str(i)
            try:
                actualpointer=int(get_pointer_to_actual_text(+pages[i[0]]['header']),16)
                g=str(i)+read_text(actualpointer)+' pg. '+str(pages[i[0]]['page_number'])
            except:
                pass
            if i==[0,0] and i2>0: g=str(i)
            #it looks like 16 as the 2nd value loads a menu defined in the first value?
            if i[1]==16:
                g=str(i)+'load menu '+str(i[0])+' after prompt'
            text = font.render(g, 1, pygame.Color("white" if i2==selected_screen_event else "black"))
            pygame.draw.rect(screen, '#0000FF' if i2==selected_screen_event else '#FFFFFF', (692,16+i2*16,270,16))


            
            screen.blit(text, (700, 16 + i2*16 ))
            i2+=1



        text = font.render('Header:', 1, pygame.Color("black"))
        screen.blit(text, (340, 16*1 ))

        sd=0

        text = font.render('X', 1, pygame.Color("black"))
        screen.blit(text, (340+(28*0), 16*2 ))
        pygame.draw.rect(screen, '#0000FF' if (current_column==1 and cl_sel==sd) else '#000000', (338+(28*0),16*3,24,16),width=1+(1*(current_column==1 and cl_sel==sd)))
        text = font.render(str(screens[selected_screen]['header']['xpos']), 1, pygame.Color("black"))
        screen.blit(text, (340+(28*0), 16*3 ))

        sd+=1

        text = font.render('Y', 1, pygame.Color("black"))
        screen.blit(text, (340+(28*1), 16*2 ))
        pygame.draw.rect(screen, '#0000FF' if (current_column==1 and cl_sel==sd) else '#000000', (338+(28*1),16*3,24,16),width=1+(1*(current_column==1 and cl_sel==sd)))
        text = font.render(str(screens[selected_screen]['header']['ypos']), 1, pygame.Color("black"))
        screen.blit(text, (340+(28*1), 16*3 ))

        sd+=1

        text = font.render('W', 1, pygame.Color("black"))
        screen.blit(text, (340+(28*2), 16*2 ))
        pygame.draw.rect(screen, '#0000FF' if (current_column==1 and cl_sel==sd) else '#000000', (338+(28*2),16*3,24,16),width=1+(1*(current_column==1 and cl_sel==sd)))
        text = font.render(str(screens[selected_screen]['header']['width']), 1, pygame.Color("black"))
        screen.blit(text, (340+(28*2), 16*3 ))

        sd+=1

        text = font.render('H', 1, pygame.Color("black"))
        screen.blit(text, (340+(28*3), 16*2 ))
        pygame.draw.rect(screen, '#0000FF' if (current_column==1 and cl_sel==sd) else '#000000', (338+(28*3),16*3,24,16),width=1+(1*(current_column==1 and cl_sel==sd)))
        text = font.render(str(screens[selected_screen]['header']['height']), 1, pygame.Color("black"))
        screen.blit(text, (340+(28*3), 16*3 ))

        sd+=1

        text = font.render('Border', 1, pygame.Color("black"))
        screen.blit(text, (340+(28*4), 16*2 ))
        pygame.draw.rect(screen, '#0000FF' if (current_column==1 and cl_sel==sd) else '#000000', (338+(28*4),16*3,24,16),width=1+(1*(current_column==1 and cl_sel==sd)))
        text = font.render(str(screens[selected_screen]['header']['border']), 1, pygame.Color("black"))
        screen.blit(text, (340+(28*4), 16*3 ))

        sd+=1

        text = font.render('Body:', 1, pygame.Color("black"))
        screen.blit(text, (340, 16*5 ))

        text = font.render('X', 1, pygame.Color("black"))
        screen.blit(text, (340+(28*0), 16*6 ))
        pygame.draw.rect(screen, '#0000FF' if (current_column==1 and cl_sel==sd) else '#000000', (338+(28*0),16*7,24,16),width=1+(1*(current_column==1 and cl_sel==sd)))
        text = font.render(str(screens[selected_screen]['body']['xpos']), 1, pygame.Color("black"))
        screen.blit(text, (340+(28*0), 16*7 ))

        sd+=1

        text = font.render('Y', 1, pygame.Color("black"))
        screen.blit(text, (340+(28*1), 16*6 ))
        pygame.draw.rect(screen, '#0000FF' if (current_column==1 and cl_sel==sd) else '#000000', (338+(28*1),16*7,24,16),width=1+(1*(current_column==1 and cl_sel==sd)))
        text = font.render(str(screens[selected_screen]['body']['ypos']), 1, pygame.Color("black"))
        screen.blit(text, (340+(28*1), 16*7 ))

        sd+=1

        text = font.render('W', 1, pygame.Color("black"))
        screen.blit(text, (340+(28*2), 16*6 ))
        pygame.draw.rect(screen, '#0000FF' if (current_column==1 and cl_sel==sd) else '#000000', (338+(28*2),16*7,24,16),width=1+(1*(current_column==1 and cl_sel==sd)))
        text = font.render(str(screens[selected_screen]['body']['width']), 1, pygame.Color("black"))
        screen.blit(text, (340+(28*2), 16*7 ))

        sd+=1

        text = font.render('H', 1, pygame.Color("black"))
        screen.blit(text, (340+(28*3), 16*6 ))
        pygame.draw.rect(screen, '#0000FF' if (current_column==1 and cl_sel==sd) else '#000000', (338+(28*3),16*7,24,16),width=1+(1*(current_column==1 and cl_sel==sd)))
        text = font.render(str(screens[selected_screen]['body']['height']), 1, pygame.Color("black"))
        screen.blit(text, (340+(28*3), 16*7 ))

        sd+=1

        text = font.render('Border', 1, pygame.Color("black"))
        screen.blit(text, (340+(28*4), 16*6 ))
        pygame.draw.rect(screen, '#0000FF' if (current_column==1 and cl_sel==sd) else '#000000', (338+(28*4),16*7,24,16),width=1+(1*(current_column==1 and cl_sel==sd)))
        text = font.render(str(screens[selected_screen]['body']['border']), 1, pygame.Color("black"))
        screen.blit(text, (340+(28*4), 16*7 ))

        sd+=1

        text = font.render('Footer:', 1, pygame.Color("black"))
        screen.blit(text, (340, 16*9 ))

        text = font.render('X', 1, pygame.Color("black"))
        screen.blit(text, (340+(28*0), 16*10 ))
        pygame.draw.rect(screen, '#0000FF' if (current_column==1 and cl_sel==sd) else '#000000', (338+(28*0),16*11,24,16),width=1+(1*(current_column==1 and cl_sel==sd)))
        text = font.render(str(screens[selected_screen]['other']['xpos']), 1, pygame.Color("black"))
        screen.blit(text, (340+(28*0), 16*11 ))

        sd+=1

        text = font.render('Y', 1, pygame.Color("black"))
        screen.blit(text, (340+(28*1), 16*10 ))
        pygame.draw.rect(screen, '#0000FF' if (current_column==1 and cl_sel==sd) else '#000000', (338+(28*1),16*11,24,16),width=1+(1*(current_column==1 and cl_sel==sd)))
        text = font.render(str(screens[selected_screen]['other']['ypos']), 1, pygame.Color("black"))
        screen.blit(text, (340+(28*1), 16*11 ))

        sd+=1

        text = font.render('W', 1, pygame.Color("black"))
        screen.blit(text, (340+(28*2), 16*10 ))
        pygame.draw.rect(screen, '#0000FF' if (current_column==1 and cl_sel==sd) else '#000000', (338+(28*2),16*11,24,16),width=1+(1*(current_column==1 and cl_sel==sd)))
        text = font.render(str(screens[selected_screen]['other']['width']), 1, pygame.Color("black"))
        screen.blit(text, (340+(28*2), 16*11 ))

        sd+=1

        text = font.render('H', 1, pygame.Color("black"))
        screen.blit(text, (340+(28*3), 16*10 ))
        pygame.draw.rect(screen, '#0000FF' if (current_column==1 and cl_sel==sd) else '#000000', (338+(28*3),16*11,24,16),width=1+(1*(current_column==1 and cl_sel==sd)))
        text = font.render(str(screens[selected_screen]['other']['height']), 1, pygame.Color("black"))
        screen.blit(text, (340+(28*3), 16*11 ))

        sd+=1

        text = font.render('Border', 1, pygame.Color("black"))
        screen.blit(text, (340+(28*4), 16*10 ))
        pygame.draw.rect(screen, '#0000FF' if (current_column==1 and cl_sel==sd) else '#000000', (338+(28*4),16*11,24,16),width=1+(1*(current_column==1 and cl_sel==sd)))
        text = font.render(str(screens[selected_screen]['other']['border']), 1, pygame.Color("black"))
        screen.blit(text, (340+(28*4), 16*11 ))

        sd+=1

        text = font.render('Number of pages:', 1, pygame.Color("black"))
        screen.blit(text, (340, 16*13 ))
        pygame.draw.rect(screen, '#0000FF' if (current_column==1 and cl_sel==sd) else '#000000', (338,16*14,24,16),width=1+(1*(current_column==1 and cl_sel==sd)))
        text = font.render(str(screens[selected_screen]['page_count']), 1, pygame.Color("black"))
        screen.blit(text, (340, 16*14 ))

        sd+=1

        text = font.render('Page, Event', 1, pygame.Color("black"))
        screen.blit(text, (340, 16*16 ))
        pygame.draw.rect(screen, '#0000FF' if (current_column==1 and cl_sel==sd) else '#000000', (338,16*17,24,16),width=1+(1*(current_column==1 and cl_sel==sd)))
        text = font.render(str(screens[selected_screen]['page_ids'][selected_screen_event][0]), 1, pygame.Color("black"))
        screen.blit(text, (340, 16*17 ))
        sd+=1
        pygame.draw.rect(screen, '#0000FF' if (current_column==1 and cl_sel==sd) else '#000000', (338+28,16*17,24,16),width=1+(1*(current_column==1 and cl_sel==sd)))
        text = font.render(str(screens[selected_screen]['page_ids'][selected_screen_event][1]), 1, pygame.Color("black"))
        screen.blit(text, (340+28, 16*17 ))

        sd+=1










        #draw frames
        #column 0
        #masking
        pygame.draw.rect(screen, '#FFFFFF', (16,0,292,16))
        pygame.draw.rect(screen, '#FFFFFF', (16,736,292,32))
        #text
        text = font.render('Screen Selection', 1, pygame.Color("black"))
        screen.blit(text, (16*7, 0))
        #box
        pygame.draw.rect(screen, '#0000FF' if (current_column==0) else '#000000', (16,16,292,720),width=1+(1*(current_column==0)))

         #column 2
        pygame.draw.rect(screen, '#0000FF' if (current_column==2) else '#000000', (692,16,270,720),width=1+(1*(current_column==2)))



        
        #preview
        screen.blit(ref, (374, 512))

        

        #print(screens[0]['other'])
        for text_to_draw in ['header','body','other']:
            try:
                bah=pages[screens[selected_screen]['page_ids'][selected_screen_event][0]][text_to_draw]
            except:
                bah=None


            
            if bah!=0:
                #print(screens[selected_screen])
                try:
                    actualpointer=int(get_pointer_to_actual_text(pages[screens[selected_screen]['page_ids'][selected_screen_event][0]][text_to_draw]),16)
                except:
                    actualpointer=int(get_pointer_to_actual_text(pages[0][text_to_draw]),16)
                g=read_text(actualpointer).split('\r')

                if len('\r'.join(g))>2:

                    if screens[selected_screen][text_to_draw]['border']%int('80',16)==0: border=border_empty_black
                    if screens[selected_screen][text_to_draw]['border']%int('80',16)==1: border=border_white_black
                    if screens[selected_screen][text_to_draw]['border']%int('80',16)==2: border=border_orange_black
                    if screens[selected_screen][text_to_draw]['border']%int('80',16)==3: border=border_empty_black
                    if screens[selected_screen][text_to_draw]['border']%int('80',16)==4: border=None
                    if screens[selected_screen][text_to_draw]['border']%int('80',16)==5: border=border_white_empty
                    if screens[selected_screen][text_to_draw]['border']%int('80',16)==6: border=border_orange_empty
                    if screens[selected_screen][text_to_draw]['border']%int('80',16)==7: border=None
                    if screens[selected_screen][text_to_draw]['border']%int('80',16)==8: border=border_empty_transparent
                    if screens[selected_screen][text_to_draw]['border']%int('80',16)==9: border=border_white_transparent
                    if screens[selected_screen][text_to_draw]['border']%int('80',16)==10: border=border_orange_transparent
                    if screens[selected_screen][text_to_draw]['border']%int('80',16)==11: border=border_empty_transparent
                    if screens[selected_screen][text_to_draw]['border']%int('80',16)==12: border=border_empty_black
                    if screens[selected_screen][text_to_draw]['border']%int('80',16)==13: border=border_white_black
                    if screens[selected_screen][text_to_draw]['border']%int('80',16)==14: border=border_orange_black
                    if screens[selected_screen][text_to_draw]['border']%int('80',16)==15: border=border_empty_black
                    
                    

                    #for reference
    ##                border_white_empty=pygame.image.load('textback_border_empty.png')
    ##                border_orange_empty=pygame.image.load('textback_orange_empty.png')
    ##                border_empty_empty=None
    ##
    ##                border_white_transparent=pygame.image.load('textback_border_transparent.png')
    ##                border_orange_transparent=pygame.image.load('textback_orange_transparent.png')
    ##                border_empty_transparent=pygame.image.load('textback_transparent.png')
    ##
    ##                border_white_black=pygame.image.load('textback_border_black.png')
    ##                border_orange_black=pygame.image.load('textback_orange_black.png')
    ##                border_empty_black=pygame.image.load('textback_black.png')


                    xpos=screens[selected_screen][text_to_draw]['xpos']
                    ypos=screens[selected_screen][text_to_draw]['ypos']
                    width=screens[selected_screen][text_to_draw]['width']
                    height=screens[selected_screen][text_to_draw]['height']

                    if border != None:

                        #Code could be more compact, but pygame sucks.
                        border_tl = pygame.Surface((8, 8), pygame.SRCALPHA)
                        border_tl.blit(border, (0, 0), ( 0,  0, 8, 8))
                        border_tm = pygame.Surface((8, 8), pygame.SRCALPHA)
                        border_tm.blit(border, (0, 0), ( 8,  0, 8, 8))
                        border_tr = pygame.Surface((8, 8), pygame.SRCALPHA)
                        border_tr.blit(border, (0, 0), (16,  0, 8, 8))
                        border_ml = pygame.Surface((8, 8), pygame.SRCALPHA)
                        border_ml.blit(border, (0, 0), ( 0,  8, 8, 8))
                        border_mm = pygame.Surface((8, 8), pygame.SRCALPHA)
                        border_mm.blit(border, (0, 0), ( 8,  8, 8, 8))
                        border_mr = pygame.Surface((8, 8), pygame.SRCALPHA)
                        border_mr.blit(border, (0, 0), (16,  8, 8, 8))
                        border_bl = pygame.Surface((8, 8), pygame.SRCALPHA)
                        border_bl.blit(border, (0, 0), ( 0, 16, 8, 8))
                        border_bm = pygame.Surface((8, 8), pygame.SRCALPHA)
                        border_bm.blit(border, (0, 0), ( 8, 16, 8, 8))
                        border_br = pygame.Surface((8, 8), pygame.SRCALPHA)
                        border_br.blit(border, (0, 0), (16, 16, 8, 8))
                        
                        screen.blit(border_tl,(374+(xpos*8)-4, 512+(ypos*8)-5))
                        screen.blit(border_tr,(374+(xpos*8)+((width-1)*8)+4, 512+(ypos*8)-5))

                        for i in range(width-1):
                            screen.blit(border_tm,(374+(xpos*8)+((i+1)*8)-4, 512+(ypos*8)-5))
                            screen.blit(border_bm,(374+(xpos*8)+((i+1)*8)-4, 512+(ypos*8)+((height-1)*8)+3))

                        for i in range(height-1):
                            screen.blit(border_ml,(374+(xpos*8)-4, 512+(ypos*8)+((i+1)*8)-5))
                            for i2 in range(width-1):
                                screen.blit(border_mm,(374+(xpos*8)+((i2+1)*8)-4, 512+(ypos*8)+((i+1)*8)-5))
                            
                            screen.blit(border_mr,(374+(xpos*8)+((width-1)*8)+4, 512+(ypos*8)+((i+1)*8)-5))

                        
                        screen.blit(border_bl,(374+(xpos*8)-4, 512+(ypos*8)+((height-1)*8)+3))
                        screen.blit(border_br,(374+(xpos*8)+((width-1)*8)+4, 512+(ypos*8)+((height-1)*8)+3))




                    
                    yp=0
                    for g2 in g:
                        text = font2.render(g2, 1, pygame.Color("white"))
                        screen.blit(text, (374+(xpos*8), 512+(ypos*8)+(yp*16)))
                        yp+=1
    if mode=='menus':
        pages=decode_pages()
        screens=decode_screens()
        menus=decode_menus()
        #print(screens)
        
        scrollamt=0
        if selected_menu>20: scrollamt=(selected_menu-20)*16
        i2=0
        for i in menus:
            g=i['header']
            #g=str().zfill(2)
            text = font.render(g, 1, pygame.Color("white" if i2==selected_menu else "black"))
            if i2==selected_menu: pygame.draw.rect(screen, '#0000FF', (16,16+i2*16 - scrollamt,292,16))
            screen.blit(text, (16, 16 + i2*16 - scrollamt ))
            i2+=1

        #render the text preview
        #background
        pygame.draw.rect(screen, '#AFAFAF', (692,16,270,720))
        #texts
        i2=0
        #print(menus[selected_menu])
        for i in menus[selected_menu]['options']:
            g=i[0]+' links to '+str(i[1])
            text = font.render(g, 1, pygame.Color("white" if i2==selected_menu_item else "black"))
            pygame.draw.rect(screen, '#0000FF' if i2==selected_menu_item else '#FFFFFF', (692,16+i2*16,270,16))
            screen.blit(text, (700, 16 + i2*16 ))

            
            #print(i)
            i2+=1



        #draw frames
        #column 0
        #masking
        pygame.draw.rect(screen, '#FFFFFF', (16,0,292,16))
        pygame.draw.rect(screen, '#FFFFFF', (16,736,292,32))
        #text
        text = font.render('Menu Selection', 1, pygame.Color("black"))
        screen.blit(text, (16*7, 0))
        #box
        pygame.draw.rect(screen, '#0000FF' if (current_column==0) else '#000000', (16,16,292,720),width=1+(1*(current_column==0)))

        #column 1
        pygame.draw.rect(screen, '#0000FF' if (current_column==2 and cl_sel==0) else '#000000', (692,16,270,720),width=1+(1*(current_column==2 and cl_sel==0)))

        if selected_menu<0: selected_menu=0
        if selected_menu>=len(menus): selected_menu=len(menus)-1
        if selected_menu_item<0: selected_menu_item=0
        if selected_menu_item>6: selected_menu_item=6
        

        text = font.render('This page links to this screen:', 1, pygame.Color("black"))
        screen.blit(text, (340, 16*18 ))
        pygame.draw.rect(screen, '#0000FF' if (current_column==1 and cl_sel==0) else '#000000', (338,16*19,24,16),width=1+(1*(current_column==1 and cl_sel==0)))
        try:
            opt=menus[selected_menu]['options'][selected_menu_item][1]
        except IndexError:
            pass
        try:
            prv=pages[screens[opt]['page_ids'][0][0]]['header']
            actualpointer=int(get_pointer_to_actual_text(prv),16)
            g=read_text(actualpointer).split('\r')[0]
        except IndexError:
            pass
        text = font.render(str(opt), 1, pygame.Color("black"))
        
        screen.blit(text, (340, 16*19 ))

        text = font.render(str(g), 1, pygame.Color("black"))
        
        screen.blit(text, (340, 16*20 ))


        text = font.render('Number of options in menu:', 1, pygame.Color("black"))
        screen.blit(text, (340, 16*22 ))
        pygame.draw.rect(screen, '#0000FF' if (current_column==1 and cl_sel==1) else '#000000', (338,16*23,24,16),width=1+(1*(current_column==1 and cl_sel==1)))
        text = font.render(str(menus[selected_menu]['option_count']), 1, pygame.Color("black"))
        
        screen.blit(text, (340, 16*23 ))

        

        #draw note
        text = font.render('NOTE:', 1, pygame.Color("black"))
        screen.blit(text, (16*21, 16*1))
        note_text=[
            'I require dumping and loading',
            'the menus to/from txt files, due to the',
            'fact that its just better to edit.',
            '',
            'With the textbox unselected:',
            '  Press D to dump to TXT',
            '  Press L to load from TXT',
            '',
            'This will dump all menu texts to numbered files.',
            'Remember to keep encoding as Shift-JIS,',
            'with carriage return (0x0D, \\r) as the',
            'newline character.',
            ]
        i2=0
        for line in note_text:
            text = font.render(line, 1, pygame.Color("black"))
            screen.blit(text, (16*21, 16*(2+i2)))
            i2+=1
    
    pygame.display.flip()
    clock.tick(60)
    #screen.fill("#FFFFFF")










    
    

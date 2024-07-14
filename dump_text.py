from tqdm import tqdm
import os

string='é»éaé¦é¦' #should resolve to "けもみみ"

if True:##$for file in os.listdir('test.bs'):
    filep='nintendo_hp.bs'#os.path.join('X:/mega/Satellaview+ Emulator/Satellaview+/satdata',file)


    with open(filep,'rb') as f:
        rawtext=f.read()
        

    encodings=["ascii",
                "big5",
                "big5hkscs",
                "cp037",
                "cp273",
                "cp424",
                "cp437",
                "cp500",
                "cp720",
                "cp737",
                "cp775",
                "cp850",
                "cp852",
                "cp855",
                "cp856",
                "cp857",
                "cp858",
                "cp860",
                "cp861",
                "cp862",
                "cp863",
                "cp864",
                "cp865",
                "cp866",
                "cp869",
                "cp874",
                "cp875",
                "cp932",
                "cp949",
                "cp950",
                "cp1006",
                "cp1026",
                "cp1125",
                "cp1140",
                "cp1250",
                "cp1251",
                "cp1252",
                "cp1253",
                "cp1254",
                "cp1255",
                "cp1256",
                "cp1257",
                "cp1258",
                "cp65001",
                "euc_jp",
                "euc_jis_2004",
                "euc_jisx0213",
                "euc_kr",
                "gb18030",
                "gbk",
                "gb2312",
                "hz",
                "iso2022_jp",
                "iso2022_jp_1",
                "iso2022_jp_2",
                "iso2022_jp_2004",
                "iso2022_jp_3",
                "iso2022_jp_ext",
                "iso2022_kr",
                "latin_1",
                "iso8859_2",
                "iso8859_3",
                "iso8859_4",
                "iso8859_5",
                "iso8859_6",
                "iso8859_7",
                "iso8859_8",
                "iso8859_9",
                "iso8859_10",
                "iso8859_11",
                "iso8859_12",
                "iso8859_13",
                "iso8859_14",
                "iso8859_15",
                "iso8859_16",
                "johab",
                "koi8_r",
                "koi8_t",
                "koi8_u",
                "kz1048",
                "mac_cyrillic",
                "mac_greek",
                "mac_iceland",
                "mac_latin2",
                "mac_roman",
                "mac_turkish",
                "ptcp154",
                "shift_jis",
                "shift_jis_2004",
                "shift_jisx0213",
                "utf_32",
                "utf_32_be",
                "utf_32_le",
                "utf_16",
                "utf_16_be",
                "utf_16_le",
                "utf_7",
                "utf_8",
                "utf_sig"]




    for input_encoding in ['shift-jis']:
        #print('---------')
        #print('encoded with',input_encoding)
        poop=''
        for brap in range(0,len(rawtext),4):
            
            try:
                input_string=rawtext[brap:brap+4].decode(input_encoding)
                works=True
                #print(input_string)
                poop+=input_string
            except:
                pass
        with open(input_encoding+'_out.txt','w',encoding='utf-8') as f:
            f.write(poop)

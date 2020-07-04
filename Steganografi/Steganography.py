from PIL import Image
import binascii
import optparse

from pip._vendor.distlib.compat import raw_input


def rgbToHex(r,g,b):
    return '#{:02x}{:02x}{:02x}'.format(r,g,b)

def hexToRgb(hexcode):
    return tuple(map(ord,hexcode[1:].decode('hex')))

def stringToBinary(mesaj):
    binary = bin(int(binascii.hexlify(mesaj),16))
    return binary[2:]

def binaryToString(binary):
    mesaj = binascii.unhexlify('%x' % (int('0b' + binary,2)))
    return mesaj

def encode(hexcode,digit):
    if hexcode[-1] in ('0','1','2','3','4','5'):
        hexcode = hexcode[:-1] + digit
        return hexcode
    else:
        return None
    
def decode(hexcode):
    if hexcode[-1] in ('0','1'):
        return hexcode[-1]
    else:
        return None
    
def hide(fileName,mesaj):
    img = Image.open(fileName)
    binary = stringToBinary(mesaj) + '1111111111111110'
    if img.mode in ('RGBA'):
        img = img.convert('RGBA')
        datas = img.getdata()
        
        newData = []
        digit = 0
        temp =''
        
        for piksel in datas:
            if(digit < len(binary)):
                newPix = encode(rgbToHex(piksel[0],piksel[1],piksel[2]),binary[digit])
                if newPix == None:
                    newData.append(piksel)
                else:
                    r,g,b = hexToRgb(newPix)
                    newData.append((r,g,b,255))
                    digit +=1

            else:
                newData.append(piksel)

        img.putdata(newData)
        img.save(fileName,"PNG")
        return "Completed!"
    return "Yanlış görüntü modu, metin saklanamadı"

def retr(fileName):
    img = Image.open(fileName)
    binary =''

    if img.mode in ('RGBA'):
        img =img.convert('RGBA')
        datas = img.getdata()

        for piksel in datas:
            digit = decode(rgbToHex(piksel[0],piksel[1],piksel[2]))
            if digit == None:
                pass
            else:
                binary = binary + digit
                if (binary[-16] == '1111111111111110' ):
                    print( 'Tamamlandı')
                    return binaryToString(binary[:-16])
        return binaryToString(binary)
    return "Yanlış görüntü modu,geri alma işlemi tamamlanamadı"

def Main():
    parser = optparse.OptionParser('usage %prog' +\
                                   '-e/-d <target file>')
    parser.add_option('-e',dest = 'hide',type ='string',\
                      help='metni saklayacağınız resmin dosya yolu')
    parser.add_option('-d',dest ='retr',type ='string' ,\
                      help ='metin saklanan resimden texti geri alma : ')
    (options,args) = parser.parse_args()
    if (options.hide != None):
        metin = raw_input("Saklamak istediğiniz metni girin: ")
        print(hide(options.hide,metin))
    elif (options.retr !=None):
        print(retr(options.retr))
    else:
        print (parser.usage)
        exit(0)

if __name__=='__main__':
    Main()
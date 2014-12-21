import argparse
import binascii
from PIL import Image


def getArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument('imageFile')
    parser.add_argument('fileForHiding', nargs = '?')
    return parser.parse_args()	


def writeFile(fname, code):
    try:
        with open(fname, 'wb') as f:
		    f.write(''.join(code))
    except IOError:
        exit('No such file or directory ' + fname)

	
def readFile(fname):
    try:
        with open(fname, 'rb') as f:
            data = f.read()
    except IOError:
        exit('No such file or directory ' + fname)
    return data	


def rgb2hex(r, g, b):
    return '#{:02x}{:02x}{:02x}'.format(r, g, b)
	
	
def hex2rgb(hexcode):
    return tuple(map(ord, hexcode[1:].decode('hex')))
	

def str2bin(message):
    binary = bin(int(binascii.hexlify(message), 16))
    return binary[2:]
	
	
def bin2str(binary):
    message = binascii.unhexlify('%x' % (int('0b'+binary,2)))
    return message
	
	
def encode(hexcode, digit):
    if hexcode[-1] in ('0','1', '2', '3', '4', '5'):
        hexcode = hexcode[:-1] + digit
        return hexcode
    else:
        return None

		
def decode(hexcode):
    if hexcode[-1] in ('0', '1'):
        return hexcode[-1]
    else:
        return None

		
def Hiding(fname, message):
    img = Image.open(fname)
    width, height = img.size
    mode = img.mode
    binary = str2bin(message) + '1111111111111110'

    if len(binary) > (width * height):
        raise Exception ("Oops! Size of image too small - choose a larger image")
    if mode in ('RGBA'):
        img = img.convert('RGBA')
        data = img.getdata()
        new_data = []
        digit = 0
        for item in data:
            if(digit < len(binary)):
                newpix = encode(rgb2hex(item[0],item[1],item[2]),binary[digit])
                if newpix == None:
                    new_data.append(item)
                else:
                    r, g, b = hex2rgb(newpix)
                    new_data.append((r,g,b,255))
                    digit +=1
            else:
                 new_data.append(item)
        img.putdata(new_data)
        img.save(fname + '_txt_hiding.png', 'png')
	
	
def Extracting(fname):
    img = Image.open(fname)
    mode = img.mode
    binary = ''
    if mode in ('RGBA'):
        img.convert('RGBA')
        data = img.getdata()
        for item in data:
            digit = decode(rgb2hex(item[0],item[1],item[2]))
            if digit == None:
                pass
            else:
                binary = binary + digit
                if(binary[-16:] == '1111111111111110'):
                    return bin2str(binary[:-16])
        return bin2str(binary)
    return  None
	
	
def main():
    print"StegoLSB"
    
    args = getArgs()
    if args.fileForHiding:
        print('Hiding')
        data = readFile(args.fileForHiding)
        try:
            Hiding(args.imageFile, data)
        except Exception as err:
            exit("Error: {0}".format(err)) 
    else:
        print('Extracting') 
        res = ''		
        res = Extracting(args.imageFile)
        writeFile(args.imageFile + ".txt", res)
if __name__ == "__main__":
    main()
   

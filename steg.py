import sys
import argparse
from PIL import Image

def printUsage():
    print"Enter the input parameters:"
    print"<name of program> <image_file> <file_out> <file_for_hiding>"
    sys.exit(-1)

	
def getArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument('imageFile')
    parser.add_argument('outFile')
    parser.add_argument('fileForHiding')
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
	
	
if __name__ == "__main__":
    print"StegoLSB"
    
    if len(sys.argv) < 4 or len(sys.argv) > 4:
        printUsage()
    args = getArgs()
    if args.fileForHiding:
		# сокрытие информации в изображении
        print('Hiding')
		readFile(args.imageFile)
    else:
		print('Recovery')
		# извлечение информации из изображения
   

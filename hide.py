from PIL import Image
import binascii
import optparse

from pip._vendor.distlib.compat import raw_input


def rgbToHex(r,g,b):
    return '#{:02x}{:02x}{:02x}'.format(r, g, b)


def hexTorgb(hexcode):
    return tuple(map(ord, hexcode[1:].decode('hex')))


def strtobin(message):
    binary = bin(int(binascii.hexlify(message), 16))
    return binary[2:]


def bintostr(binary):
    message = binascii.unhexlify('%x' % (int('0b' +binary, 2)))
    return message


def encode(hexcode, digit):
    if hexcode[-1] in ('0', '1', '2', '3', '4', '5'):
        hexcode = hexcode[:-1]+digit
        return hexcode
    else:
        return None


def decode(hexcode):
    if hexcode[-1] in ('0', '1'):
        return hexcode[-1]
    else:
        return None


def hide(filename, message):
    img = Image.open(filename)
    binary = strtobin(message) + '1111111111111110'
    if img.mode in ('RGBA'):
        img = img.convert('RGBA')
        datas = img.getdata()
        newData = []
        digit = 0
        temp = ''
        for item in datas:
            if digit < len(binary):
                newPix = encode(rgbToHex(item[0], item[1], item[2]),binary[digit])
                if newPix is None:
                    newData.append(item)
                else:
                    r, g, b = hexTorgb(newPix)
                    newData.append((r, g, b, 255))
                    digit += 1
            else:
                newData.append(item)
        img.putdata(newData)
        img.save(filename, "PNG")
        return "Completed!"
    return "Error"


def retr(fileName):
    img = Image.open(fileName)
    binary = ''
    if img.mode in ('RGBA'):
        img = img.convert('RGBA')
        datas = img.getdata()
        for item in datas:
            digit = decode(rgbToHex(item[0], item[1], item[2]))
            if digit is None:
                pass
            else:
                binary = binary + digit
                if binary[-16:] == '1111111111111110':
                    print("Sucess")
                    return bintostr(binary[:-16])
        return bintostr(binary)
    return "Incorrect image mode"


def Main():
    parser = optparse.OptionParser('usage % prog ' +\
                                   '-e/-d <target file>')
    parser.add_option('-e', dest='hide', type='string', help='target picture to hide text')
    parser.add_option('-d', dest='retr', type='string', help='target picture to retrieve text')
    (options, args) = parser.parse_args()
    if options.hide is not None:
        text = raw_input('Enter a message to hide: ')
        print(hide(options.hide, text))
    elif options.retr is not None:
        print(retr(options.retr))
    else:
        print(parser.usage)
        exit(0)


if __name__ == '__main__':
    Main()


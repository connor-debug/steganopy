#based on stepic (2007 Lenny Domnitser)


#stepic, stenopy uses PIL library to encode messages in images


#Connor Flynn <http://connorflynn.org/>'



import warnings
try:
    import Image
except:
    warnings.warn('Could not find PIL. Only encode_imdata and decode_imdata will work.',
                  ImportWarning, stacklevel=2)


__all__ = ('encode_imdata','encode_inplace', 'encode',
           'decode_imdata', 'decode',
           'Steganographer')


def encode_imdata(imdata, data):
    '''given a sequence of pixels, returns an iterator of pixels with
    encoded data'''

    datalen = len(data)
    if datalen == 0:
        raise ValueError('data is empty')
    if datalen * 3 > len(imdata):
        raise ValueError('data is too large for image')

    imdata = iter(imdata)

    for i in range(datalen):
        pixels = [value & ~1 for value in
                  imdata.__next__()[:3] + imdata.__next__()[:3] + imdata.__next__()[:3]]
        byte = ord(data[i])
        for j in range(7, -1, -1):
            pixels[j] |= byte & 1
            byte >>= 1
        if i == datalen - 1:
            pixels[-1] |= 1
        pixels = tuple(pixels)
        yield pixels[0:3]
        yield pixels[3:6]
        yield pixels[6:9]


def encode_inplace(image, data):
    '''hides data in an image'''

    w = image.size[0]
    (x, y) = (0, 0)
    for pixel in encode_imdata(image.getdata(), data):
        image.putpixel((x, y), pixel)
        if x == w - 1:
            x = 0
            y += 1
        else:
            x += 1


def encode(image, data):
    '''generates an image with hidden data, starting with an existing
    image and arbitrary data'''

    image = image.copy()
    encode_inplace(image, data)
    return image


def decode_imdata(imdata):

    imdata = iter(imdata)
    while True:
        pixels = list(imdata.__next__()[:3] + imdata.__next__()[:3] + imdata.__next__()[:3])
        byte = 0
        for c in range(7):
            byte |= pixels[c] & 1
            byte <<= 1
        byte |= pixels[7] & 1
        yield chr(byte)
        if pixels[-1] & 1:
            break


def decode(image):

    return ''.join(decode_imdata(image.getdata()))


class Steganographer:
    'deprecated'
    def __init__(self, image):
        self.image = image
        warnings.warn('Steganographer class is deprecated, and will be removed before 1.0',
                      DeprecationWarning, stacklevel=2)
    def encode(self, data):
        return encode(self.image, data)
    def decode(self):
        return decode(self.image)

import cv2
import numpy as np

class SteganographyException(Exception):
    pass

class LSBSteg:
    def __init__(self, im):
        self.image = im
        self.height, self.width, self.nbchannels = im.shape
        self.size = self.width * self.height

        self.maskONEValues = [1, 2, 4, 8, 16, 32, 64, 128]
        self.maskONE = self.maskONEValues.pop(0)

        self.maskZEROValues = [254, 253, 251, 247, 239, 223, 191, 127]
        self.maskZERO = self.maskZEROValues.pop(0)

        self.curwidth = 0
        self.curheight = 0
        self.curchan = 0

    def put_binary_value(self, bits):
        for c in bits:
            val = list(self.image[self.curheight, self.curwidth])
            if int(c) == 1:
                val[self.curchan] = int(val[self.curchan]) | self.maskONE
            else:
                val[self.curchan] = int(val[self.curchan]) & self.maskZERO

            self.image[self.curheight, self.curwidth] = tuple(val)
            self.next_slot()

    def next_slot(self):
        if self.curchan == self.nbchannels - 1:
            self.curchan = 0
            if self.curwidth == self.width - 1:
                self.curwidth = 0
                if self.curheight == self.height - 1:
                    self.curheight = 0
                    if self.maskONE == 128:
                        raise SteganographyException("No available slot remaining (image filled)")
                    else:
                        self.maskONE = self.maskONEValues.pop(0)
                        self.maskZERO = self.maskZEROValues.pop(0)
                else:
                    self.curheight += 1
            else:
                self.curwidth += 1
        else:
            self.curchan += 1

    def read_bit(self):
        val = self.image[self.curheight, self.curwidth][self.curchan]
        val = int(val) & self.maskONE
        self.next_slot()
        if val > 0:
            return "1"
        else:
            return "0"

    def read_byte(self):
        return self.read_bits(8)

    def read_bits(self, nb):
        bits = ""
        for _ in range(nb):
            bits += self.read_bit()
        return bits

    def byteValue(self, val):
        return self.binary_value(val, 8)

    def binary_value(self, val, bitsize):
        binval = bin(val)[2:]
        if len(binval) > bitsize:
            raise SteganographyException("binary value larger than the expected size")
        while len(binval) < bitsize:
            binval = "0" + binval
        return binval

    # Add print statements to debug
    def encode_text(self, txt):
        print(f"Encoding text: {txt}")
        l = len(txt)
        binl = self.binary_value(l, 16)
        self.put_binary_value(binl)
        for char in txt:
            c = ord(char)
            self.put_binary_value(self.byteValue(c))
        print("Text encoded successfully")
        return self.image
    

    
    def decode_text(self):
        ls = self.read_bits(16)
        l = int(ls, 2)
        i = 0
        unhideTxt = ""
        while i < l:
            tmp = self.read_byte()
            i += 1
            unhideTxt += chr(int(tmp, 2))
        return unhideTxt

    def encode_image(self, imtohide):
        w = imtohide.width
        h = imtohide.height
        if self.width * self.height * self.nbchannels < w * h * imtohide.channels:
            raise SteganographyException("Carrier image not big enough to hold all the data to steganography")
        binw = self.binary_value(w, 16)
        binh = self.binary_value(h, 16)
        self.put_binary_value(binw)
        self.put_binary_value(binh)
        for h in range(imtohide.height):
            for w in range(imtohide.width):
                for chan in range(imtohide.channels):
                    val = imtohide[h, w][chan]
                    self.put_binary_value(self.byteValue(int(val)))
        return self.image

    def decode_image(self):
        width = int(self.read_bits(16), 2)
        height = int(self.read_bits(16), 2)
        unhideimg = np.zeros((width, height, 3), np.uint8)
        for h in range(height):
            for w in range(width):
                for chan in range(unhideimg.channels):
                    val = list(unhideimg[h, w])
                    val[chan] = int(self.read_byte(), 2)
                    unhideimg[h, w] = tuple(val)
        return unhideimg

    def encode_binary(self, data):
        l = len(data)
        if self.width * self.height * self.nbchannels < l + 64:
            raise SteganographyException("Carrier image not big enough to hold all the data to steganography")
        self.put_binary_value(self.binary_value(l, 64))
        for byte in data:
            byte = byte if isinstance(byte, int) else ord(byte)
            self.put_binary_value(self.byteValue(byte))
        return self.image

    def decode_binary(self):
        l = int(self.read_bits(64), 2)
        output = b""
        for _ in range(l):
            output += bytearray([int(self.read_byte(), 2)])
        return output

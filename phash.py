#-*- coding: utf-8 -*-

"""
Usage: phash.py <IMAGE>
       phash.py -h | --help
       phash.py --version
Options:
       -h --help    show this screen
       --version    show version
"""

from docopt import docopt
import sys
import cv2
import numpy as np
from scipy import fftpack

RESIZE_W = 32
RESIZE_H = 32


def main():
    opts = docopt(__doc__, version='1.0')
    img_file = opts['<IMAGE>']
    if not img_file:
        print 'Not found: %s' % img_file
        sys.exit(1)

    # read the image
    img = cv2.imread(img_file)

    # Reduce size
    img = cv2.resize(img, (RESIZE_W, RESIZE_H))

    # Reduce color
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    img = np.array(img,
                   dtype=np.float).reshape((RESIZE_W, RESIZE_H))

    # Compute the DCT(Type2)
    img = fftpack.dct(img)

    # Reduce the DCT (low frequency)
    img = img[:8, 1:9]

    # Compute the average value
    img_mean = cv2.mean(img)[0]

    # Further reduce the DCT
    bits = img > img_mean

    # Construct the hash
    h = 0
    phash = []
    for i, v in enumerate(bits.flatten()):
        if v:
            h += 2**(i % 8)
        if (i % 8) == 7:
            phash.append(hex(h)[2:].rjust(2, '0'))
            h = 0

    print 'phash = %s' % ''.join(phash)

if __name__ == '__main__':
    main()

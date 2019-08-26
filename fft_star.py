import numpy as np
from astropy.io import fits
from numpy.fft import fft2, fftshift
import matplotlib
matplotlib.use('Qt5Agg') 
import matplotlib.pyplot as plt
from os import system

# ===============================================================
# Plots 1darray and 2darray
# ===============================================================
def plot(ary):
    ary_dimen = len(ary.shape)
    if ary_dimen == 1:
        plt.plot(ary)

    elif ary_dimen == 2:
        plt.imshow(ary) 
    else:
        print("Not implemented for this dimension")
    plt.show()
# ===============================================================


# ===============================================================
# Creates disk in a 2darray
# ===============================================================
def circle(array,radius,value,cross=""):
    size = array.shape[0]
    center = size//2

    for y in range(size):
        for x in range(size):
            # see if we're close to (x-a)**2 + (y-b)**2 == r**2
            if ((x-center)**2 + (y-center)**2 - radius**2) <=0:
                array[y][x] = value

    # Create diameter chords
    thickness = int(radius*0.03)
    if cross=="+":
        array[center-thickness:center+thickness,center-radius:center+radius] = 0
        array[center-radius:center+radius,center-thickness:center+thickness] = 0
    elif cross=="-":
        array[center-thickness:center+thickness,center-radius:center+radius] = 0
    elif cross=="|":
        array[center-radius:center+radius,center-thickness:center+thickness] = 0
    else:
        pass

    return array
# ===============================================================


# ===============================================================
# swaps 2,4 and 1,3 quadrants of a square matix
# ===============================================================
def transform(a):
    quar = a.shape[0]//2

    for i in range(quar):
        for j in range(quar):
            a[i][j],a[i+quar][j+quar] =  a[i+quar][j+quar],a[i][j]
            a[i+quar][j], a[i][j+quar] = a[i][j+quar],a[i+quar][j]
    a = np.rot90(a)

    return a
# ===============================================================

if __name__ == "__main__":
    mask = np.zeros(shape=(2000,2000))
    mask = circle(mask,100,1,"|")
    mask = circle(mask,5,0)

    fits.writeto("image.fits",mask,overwrite=True)

    # fft = np.abs(fft2(fftshift(mask))
    fft = np.abs(fft2(mask))
    fft = transform(fft)

    fits.writeto("fft.fits",fft,overwrite=True)

    system("sudo ds9 ./image.fits &")
    system("sudo ds9 ./fft.fits &")
    # plot(fft[fft.shape[0]//2])

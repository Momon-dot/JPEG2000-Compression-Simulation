from math import floor

def quant_im(im, quan_val):
    m = 0
    n = 0
    for i in im:
        for j in i:
            im[m][n] = floor(j/quan_val)
            n += 1
        n=0
        m+=1
    return im

def dequant_im(im, quan_val):
    im = im*quan_val
    return im




import matplotlib.pyplot as plt  
import numpy as np               
from imageio import imwrite, imread, core      
import sys
from PIL import Image
from os import path
sys.path.insert(0, 'nt_toolbox')
from nt_toolbox.general import *
from nt_toolbox.signal import *
from nt_toolbox.compute_wavelet_filter import *
import entropy_decode
import entropty_encode
from collections import Counter
import scalar_de_qua as sq

#GUI

def display(im):  # Define a new Python routine
    """
    Displays an image using the methods of the 'matplotlib' library.
    """
             # Square blackboard
    plt.imshow( im)  # Display 'im' using a gray colormap,
                                                  #         from 0 (black) to 1 (white)

def display_2(im_1, title_1, im_2, title_2):
    """
    Displays two images side by side; typically, an image and its Fourier transform.
    """                 # Rectangular blackboard
    plt.subplot(1,2,1) ; plt.title(title_1)       # 1x2 waffle plot, 1st cell
    plt.imshow(im_1)                 # Auto-equalization
    plt.subplot(1,2,2) ; plt.title(title_2)  # 1x2 waffle plot, 2nd cell
    plt.imshow(im_2)

def display_3(im_1, title_1, im_2, title_2,im_3, title_3,im_4, title_4,im_5, title_5,im_6, title_6):
    """
    Displays two images side by side; typically, an image and its Fourier transform.
    """                 # Rectangular blackboard
    plt.subplot(3,2,1) ; plt.title(title_1)       # 1x2 waffle plot, 1st cell
    plt.imshow(npti(im_1))                 # Auto-equalization
    ax = plt.gca()
    ax.get_xaxis().set_visible(False)
    plt.subplot(3,2,2) ; plt.title(title_2)  # 1x2 waffle plot, 2nd cell
    plt.imshow(npti(im_2),cmap='gray', vmin=-1,vmax=1)
    ax = plt.gca()
    ax.get_xaxis().set_visible(False)
    plt.subplot(3,2,3) ; plt.title(title_3)       # 1x2 waffle plot, 1st cell
    plt.imshow(npti(im_3))                 # Auto-equalization
    ax = plt.gca()
    ax.get_xaxis().set_visible(False)
    plt.subplot(3,2,4) ; plt.title(title_4)  # 1x2 waffle plot, 2nd cell
    plt.imshow(npti(im_4), vmin=-1,vmax=1)
    ax = plt.gca()
    ax.get_xaxis().set_visible(False)
    plt.subplot(3,2,5) ; plt.title(title_5)       # 1x2 waffle plot, 1st cell
    plt.imshow(npti(im_5))                 # Auto-equalization
    plt.subplot(3,2,6) ; plt.title(title_6)  # 1x2 waffle plot, 2nd cell
    plt.imshow(npti(im_6), vmin=-1,vmax=1)
    ax = plt.gca()
    ax.get_xaxis().set_visible(False)

def wavelet_bandpass_res(im):
    la = imread("temp/output_band.png")
    display_2(im,"Original Image",la,"Reconstructed Wavelet Transform Image")


def wavelet_threshold_res(im):
    la = imread("temp/output_tresh.png")
    display_2(im,"Original Image",la,"Reconstructed Wavelet Transform Image")


#Processing Function

def wavelet_transform(I, h1=8, Jmin=1) :
    h = compute_wavelet_filter("Daubechies",h1)
    wI = perform_wavortho_transf(I, Jmin, + 1, h)
    return wI


def iwavelet_transform(wI, h1=8, Jmin=1) :
    h = compute_wavelet_filter("Daubechies",h1)
    I = perform_wavortho_transf(wI, Jmin, - 1, h)
    return I

     # Compute the wavelet transform

def npti(img):
    return core.util.Array(img)

def make_square(im, min_size=256, fill_color=(0, 0, 0, 0)):
    x, y = im.size
    size = max(min_size, x, y)
    new_im = Image.new('RGBA', (size, size), fill_color)
    new_im.paste(im, (int((size - x) / 2), int((size - y) / 2)))
    return new_im

def arithmetic_en(arr_raw, block_size = 1):
    pixels = np.array(arr_raw.flatten())
    n = arr_raw.shape[0]
    m = arr_raw.shape[1]
    # append zeros to be divisible by the block_size
    additional_pixels = 0
    while pixels.shape[0] % block_size != 0:
        pixels = np.append(pixels, 0)
        additional_pixels += 1

    length = pixels.shape[0]
    freq = Counter(pixels)
    probs = {}
    for key in freq.keys():
        probs[key] = freq[key]/length

    start = 0
    probs_limits = {}
    for key in probs.keys():
        probs_limits[key] = start, start+probs[key]
        start += probs[key]

    np.save("temp/probabilities.npy", probs_limits)
    print("Processing input and calculating probabilities: Done!")
    return [entropty_encode.encode_image(pixels, block_size, probs_limits, "float32"), n,m, block_size, probs_limits, additional_pixels]
    # additonal pixels is zeros to make the array divisible 

def Wavelet_bandpass(wI, depthMin, depthMax) :
    wI_band = wI.copy()             
    # Remove the low frequencies:
    wI_band[ :int(2**(depthMin-1)), :int(2**(depthMin-1))] = 0
    wI_band[ 2**depthMax:, :] = 0  # Remove the high frequencies
    wI_band[ :, 2**depthMax:] = 0  # Remove the high frequencies
    I_band = iwavelet_transform(wI_band)
    
    return [I_band,wI_band]

def Wavelet_threshold(wI, threshold,i) :     # Re-implement a thresholding routine
    wI_thresh = wI.copy()                  # Create a copy of the Wavelet transform
    wI_thresh[ abs(wI) < threshold ] = 0   # Remove all the small coefficients
    I_thresh = iwavelet_transform(wI_thresh)   # Invert the new transform...
    if i == 1:
        return [I_thresh,wI_thresh]
    else :
        return I_thresh


#Looping Function for Displaying Result

def Waveband_loop(im, depthMin, depthMax):
    y, cb, cr= im.convert('YCbCr').split()
    y = core.util.Array(np.array(y, dtype=np.float32))
    cb = core.util.Array(np.array(cb, dtype=np.float32))
    cr = core.util.Array(np.array(cr, dtype=np.float32))
    wI_Y = wavelet_transform(y)
    I_y,wI_Y = Wavelet_bandpass(wI_Y, depthMin, depthMax)
    wI_Cb = wavelet_transform(cb)
    I_Cb, wI_Cb = Wavelet_bandpass(wI_Cb, depthMin, depthMax)
    wI_Cr = wavelet_transform(cr)
    I_Cr,wI_Cr = Wavelet_bandpass(wI_Cr, depthMin,depthMax)

    zerosa = np.ones((256,256),dtype = np.float32)*127

    I_yB = Image.fromarray(I_y).convert('L')
    I_CbB = Image.fromarray(I_Cb).convert('L')
    I_CrB = Image.fromarray(I_Cr).convert('L')
    wI_CbB = Image.fromarray(wI_Cb).convert('L')
    wI_CrB = Image.fromarray(wI_Cr).convert('L')
    I_zers = Image.fromarray(zerosa).convert('L')
    I_ya = Image.merge('YCbCr',(I_yB,I_zers,I_zers)).convert('RGB')
    I_Cba = Image.merge('YCbCr',(I_zers,I_CbB,I_zers)).convert('RGB')
    I_Cra = Image.merge('YCbCr',(I_zers,I_zers,I_CrB)).convert('RGB')
    wI_Cba = Image.merge('YCbCr',(I_zers,wI_CbB,I_zers)).convert('RGB')
    wI_Cra = Image.merge('YCbCr',(I_zers,I_zers,wI_CrB)).convert('RGB')


    ycbcr_inv = Image.merge('YCbCr',(Image.fromarray(I_y).convert('L'),Image.fromarray(I_Cb).convert('L'),Image.fromarray(I_Cr).convert('L')))
    ycbcr_inv = ycbcr_inv.convert('RGB')
    display_3(np.array(I_ya),"Y Image", wI_Y, "Y Wavelet Transform", np.array(I_Cba), "Cb Image", np.array(wI_Cba), "Cb Wavelet Transform", np.array(I_Cra), "Cr image", np.array(wI_Cra), "Cr Wavelet Transform")    
    imwrite("temp/output_band.png", np.array(ycbcr_inv))
    outputband = path.getsize("temp/output_band.png")
    return outputband

def WaveTresh_loop(im,threshold):
    y, cb, cr= im.convert('YCbCr').split()
    y = core.util.Array(np.array(y, dtype=np.float32))
    cb = core.util.Array(np.array(cb, dtype=np.float32))
    cr = core.util.Array(np.array(cr, dtype=np.float32))
    wI_Y = wavelet_transform(y)
    I_y, wI_Y = Wavelet_threshold(wI_Y, threshold,1)
    wI_Cb = wavelet_transform(cb)
    I_Cb, wI_Cb = Wavelet_threshold(wI_Cb, threshold,1)
    wI_Cr = wavelet_transform(cr)
    I_Cr, wI_Cr = Wavelet_threshold(wI_Cr, threshold,1)
    zerosa = np.ones((256,256),dtype = np.float32)*127

    I_yB = Image.fromarray(I_y).convert('L')
    I_CbB = Image.fromarray(I_Cb).convert('L')
    I_CrB = Image.fromarray(I_Cr).convert('L')
    wI_CbB = Image.fromarray(wI_Cb).convert('L')
    wI_CrB = Image.fromarray(wI_Cr).convert('L')
    I_zers = Image.fromarray(zerosa).convert('L')
    I_ya = Image.merge('YCbCr',(I_yB,I_zers,I_zers)).convert('RGB')
    I_Cba = Image.merge('YCbCr',(I_zers,I_CbB,I_zers)).convert('RGB')
    I_Cra = Image.merge('YCbCr',(I_zers,I_zers,I_CrB)).convert('RGB')
    wI_Cba = Image.merge('YCbCr',(I_zers,wI_CbB,I_zers)).convert('RGB')
    wI_Cra = Image.merge('YCbCr',(I_zers,I_zers,wI_CrB)).convert('RGB')


    ycbcr_inv = Image.merge('YCbCr',(Image.fromarray(I_y).convert('L'),Image.fromarray(I_Cb).convert('L'),Image.fromarray(I_Cr).convert('L')))
    ycbcr_inv = ycbcr_inv.convert('RGB')
    display_3(np.array(I_ya),"Y Image", wI_Y, "Y Wavelet Transform", np.array(I_Cba), "Cb Image", np.array(wI_Cba), "Cb Wavelet Transform", np.array(I_Cra), "Cr image", np.array(wI_Cra), "Cr Wavelet Transform")    
    imwrite("temp/output_tresh.png", np.array(ycbcr_inv))
    outputband = path.getsize("temp/output_tresh.png")
    return outputband

def scalar_quantization(im, quan_size):
    y, cb, cr= im.convert('YCbCr').split()
    y = core.util.Array(np.array(y, dtype=np.float32))
    cb = core.util.Array(np.array(cb, dtype=np.float32))
    cr = core.util.Array(np.array(cr, dtype=np.float32))

    Y_quan = sq.quant_im(y, quan_size)
    Cb_quan = sq.quant_im(cb, quan_size)
    Cr_quan = sq.quant_im(cr, quan_size)
    Y_quan = sq.dequant_im(Y_quan, quan_size)
    Cb_quan = sq.dequant_im(Cb_quan, quan_size)
    Cr_quan = sq.dequant_im(Cr_quan, quan_size)

    ycbcr_inv = Image.merge('YCbCr',(Image.fromarray(Y_quan).convert('L'),Image.fromarray(Cb_quan).convert('L'),Image.fromarray(Cr_quan).convert('L')))
    imgfor = ycbcr_inv.convert('RGB')
    imwrite("temp/quan.png", np.array(imgfor))
    outputquan = path.getsize("temp/quan.png")
    ori_img = imread("temp/intermediate.png")
    display_2( ori_img, "Original Image",          # And display
               imgfor, "Reconstructed Scalar Quantization Image")
    return outputquan

def arithmetic_encode(im, block_size):
    y, cb, cr= im.convert('YCbCr').split()
    y = core.util.Array(np.array(y, dtype=np.float32))
    cb = core.util.Array(np.array(cb, dtype=np.float32))
    cr = core.util.Array(np.array(cr, dtype=np.float32))

    encoded_array_y, n_y, m_y, block_size_y, probs_limits_y, additional_pixels_y = arithmetic_en(np.array(y), block_size)
    encoded_array_cb, n_cb, m_cb, block_size_cb, probs_limits_cb, additional_pixels_cb = arithmetic_en(np.array(cb), block_size)
    encoded_array_cr, n_cr, m_cr, block_size_cr, probs_limits_cr, additional_pixels_cr = arithmetic_en(np.array(cr), block_size)

    I_y = entropy_decode.decode_image(encoded_array_y, n_y, m_y, block_size_y,
                            probs_limits_y, additional_pixels_y)
    I_Cb = entropy_decode.decode_image(encoded_array_cb, n_cb, m_cb, block_size_cb,
                            probs_limits_cb, additional_pixels_cb)
    I_Cr = entropy_decode.decode_image(encoded_array_cr, n_cr, m_cr, block_size_cr,
                            probs_limits_cr, additional_pixels_cr)

    ycbcr_inv = Image.merge('YCbCr',(Image.fromarray(I_y).convert('L'),Image.fromarray(I_Cb).convert('L'),Image.fromarray(I_Cr).convert('L')))
    imgfor = ycbcr_inv.convert('RGB')
    imwrite("temp/enc.png", np.array(imgfor))
    outputen = path.getsize("temp/enc.png")
    ori_img = imread("temp/intermediate.png")
    display_2( ori_img, "Original Image",          # And display
               imgfor, "Reconstructed Arithmetic Coding Image" )
    return outputen

def JPEG2000(im, quan_val,threshold, block_size):
    y, cb, cr= im.convert('YCbCr').split()
    y = core.util.Array(np.array(y, dtype=np.float32))
    cb = core.util.Array(np.array(cb, dtype=np.float32))
    cr = core.util.Array(np.array(cr, dtype=np.float32))

    #Wavelet Transform
    I_y = wavelet_transform(y)
    I_Cb = wavelet_transform(cb)
    I_Cr = wavelet_transform(cr)
    wI_y = Wavelet_threshold(I_y, threshold,2)
    wI_Cb = Wavelet_threshold(I_Cb, threshold,2)
    wI_Cr = Wavelet_threshold(I_Cr, threshold,2)

    #Scalar Quantization
    wI_Y_quan = sq.quant_im(wI_y, quan_val)
    wI_Cb_quan = sq.quant_im(wI_Cb, quan_val)
    wI_Cr_quan = sq.quant_im(wI_Cr, quan_val)
    wI_Y_dequan = sq.dequant_im(wI_Y_quan,quan_val)
    wI_Cb_dequan = sq.dequant_im(wI_Cb_quan,quan_val)
    wI_Cr_dequan = sq.dequant_im(wI_Cr_quan,quan_val)

    #Arithmetic Coding
    encoded_array_y, n_y, m_y, block_size_y, probs_limits_y, additional_pixels_y = arithmetic_en(np.array(wI_Y_dequan), block_size)
    encoded_array_cb, n_cb, m_cb, block_size_cb, probs_limits_cb, additional_pixels_cb = arithmetic_en(np.array(wI_Cb_dequan), block_size)
    encoded_array_cr, n_cr, m_cr, block_size_cr, probs_limits_cr, additional_pixels_cr = arithmetic_en(np.array(wI_Cr_dequan), block_size)
    res_y = entropy_decode.decode_image(encoded_array_y, n_y, m_y, block_size_y,
                            probs_limits_y, additional_pixels_y)
    res_Cb = entropy_decode.decode_image(encoded_array_cb, n_cb, m_cb, block_size_cb,
                            probs_limits_cb, additional_pixels_cb)
    res_Cr = entropy_decode.decode_image(encoded_array_cr, n_cr, m_cr, block_size_cr,
                            probs_limits_cr, additional_pixels_cr)


    

    img_Ori = imread("temp\intermediate.png")
    ycbcr_inv = Image.merge('YCbCr',(Image.fromarray(res_y).convert('L'),Image.fromarray(res_Cb).convert('L'),Image.fromarray(res_Cr).convert('L')))
    res = ycbcr_inv.convert('RGB')
    imwrite("temp/output.png", res)
    outputres = path.getsize("temp/output.png")
    outputcom = path.getsize("temp/encoded_array.npy")
    display_2( img_Ori, "Original Image",          # And display
               res, "Reconstructed JPEG2000 Image" )
    return outputres

   


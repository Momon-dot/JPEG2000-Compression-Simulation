import PySimpleGUI as sg
import os.path
from PIL import Image
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import backend
import numpy as np

#Initiate Variable

inputsize = 0
outputtresh = 0
outputband = 0
outputen = 0
outputquan = 0
outputres = 0
i = 0
j = 0
k = 0
l = 0
m = 0
n = 0
wa = 1
wb = 1
r = 0
u = 0
blocksize_arr = [1,2,4]


#Initiation Function
dirName = 'temp'
try:
    os.mkdir(dirName)
    print("Directory " , dirName ,  " Created ") 
except FileExistsError:
    print("Directory " , dirName ,  " already exists")

def convert_to_bytes(file_or_bytes):
    global inputsize
    img = Image.open(file_or_bytes)
    img = backend.make_square(img)
    img.resize((256,256),Image.Resampling.LANCZOS).save("temp/intermediate.png", quality = 95)    
    inputsize = os.path.getsize("temp/intermediate.png")
    I = Image.open("temp/intermediate.png")
    return I


#Graphical Stuff

_VARS = {'window': False,
         'fig_agg_encode': False,
         'pltFig_encode': False,
         'fig_agg_quan': False,
         'pltFig_quan': False,
         'fig_agg_wavebanddec': False,
         'pltFig_wavebanddec': False,
         'fig_agg_wavebandres': False,
         'pltFig_wavebandres': False,
         'fig_agg_wavetreshdec': False,
         'pltFig_wavetreshdec': False,
         'fig_agg_wavetreshres': False,
         'pltFig_wavetreshres': False,
         'figCanvas_display': False,
         'pltFig_display': False,
         'fig_agg_res': False,
         'pltFig_res': False,
        }

def draw_figure(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg

def delete_fig_agg(fig_agg):
    fig_agg.get_tk_widget().forget()
    plt.close('all')

#Displaying Result for each processes
def drawChart_display(I):
    global outputband, l
    if l:
        delete_fig_agg(_VARS['fig_agg_display'])
        l = 0 

    _VARS['pltFig_display'] = plt.figure()
    backend.display(np.array(I))
    _VARS['fig_agg_display'] = draw_figure(
        _VARS['window']['figCanvas_display'].TKCanvas, _VARS['pltFig_display'])

def drawChart_wavebandres(im):
    global n
    if n:
        delete_fig_agg(_VARS['fig_agg_wavebandres'])
        n = 0

    _VARS['pltFig_wavebandres'] = plt.figure(figsize=(12,12))
    backend.wavelet_bandpass_res(im)
    _VARS['fig_agg_wavebandres'] = draw_figure(
        _VARS['window']['figCanvas_wavebandres'].TKCanvas, _VARS['pltFig_wavebandres'])

def drawChart_waveband(I, n = 0, m = 4):
    global outputband, j
    if j:
        delete_fig_agg(_VARS['fig_agg_wavebanddec'])
        j = 0
    _VARS['pltFig_wavebanddec'] = plt.figure(figsize=(12,12))
    outputband = backend.Waveband_loop(I,n,m)
    _VARS['fig_agg_wavebanddec'] = draw_figure(
        _VARS['window']['figCanvas_wavebanddec'].TKCanvas, _VARS['pltFig_wavebanddec'])
    drawChart_wavebandres(I)

def drawChart_wavetreshres(I):
    global m
    if m:
        delete_fig_agg(_VARS['fig_agg_wavetreshres'])
        m = 0

    _VARS['pltFig_wavetreshres'] = plt.figure(figsize=(12,12))
    backend.wavelet_threshold_res(I)
    _VARS['fig_agg_wavetreshres'] = draw_figure(
        _VARS['window']['figCanvas_wavetreshres'].TKCanvas, _VARS['pltFig_wavetreshres'])

def drawChart_wavetresh(I,n=50):
    global outputtresh, k
    if k:
        delete_fig_agg(_VARS['fig_agg_wavetreshdec'])
        k = 0

    _VARS['pltFig_wavetreshdec'] = plt.figure(figsize=(12,12))
    outputtresh = backend.WaveTresh_loop(I,n)
    _VARS['fig_agg_wavetreshdec'] = draw_figure(
        _VARS['window']['figCanvas_wavetreshdec'].TKCanvas, _VARS['pltFig_wavetreshdec'])
    drawChart_wavetreshres(I)

def drawChart_quan(I,quantization_size):
    global outputquan, r
    if r:
        delete_fig_agg(_VARS['fig_agg_quan'])
        r = 0
    _VARS['pltFig_quan'] = plt.figure(figsize=(12,12))
    outputquan = backend.scalar_quantization(I,quantization_size)
    _VARS['fig_agg_quan'] = draw_figure(
        _VARS['window']['figCanvas_quan'].TKCanvas, _VARS['pltFig_quan'])

def drawChart_enc(I,block_size=1):
    global outputen, i
    if i:
        delete_fig_agg(_VARS['fig_agg_encode'])
        i = 0
    if block_size < 1:
        block_size = 1
    _VARS['pltFig_encode'] = plt.figure(figsize=(12,12))
    outputen = backend.arithmetic_encode(I,block_size)
    _VARS['fig_agg_encode'] = draw_figure(
        _VARS['window']['figCanvas_encode'].TKCanvas, _VARS['pltFig_encode'])
        
def drawChart_result(I,quantize_size,n=50,block_size=1):
    global outputres, u
    if u:
        delete_fig_agg(_VARS['fig_agg_res'])
        u = 0
    if block_size < 1:
        block_size = 1
    _VARS['pltFig_res'] = plt.figure(figsize=(12,12))
    outputres = backend.JPEG2000(I,quantize_size,n,block_size)
    _VARS['fig_agg_res'] = draw_figure(
        _VARS['window']['figCanvas_res'].TKCanvas, _VARS['pltFig_res'])

AppFont = 'Any 16'
sg.theme('DarkTeal12')

left_col = [[sg.Text('Cara Simulasi:',font=("Helvetica",11))],
          [sg.Text('1. Tekan tombol "Browse" dan pilih folder berisi foto',font=("Helvetica",9))],
          [sg.Text('2. Klik nama file foto yang ingin diproses(TUNGGU PROSES SELESAI)',font=("Helvetica",9))],
          [sg.Text('(JANGAN HIRAUKAN "Not Responding")',font=("Helvetica",9))],
          [sg.Text('3. Klik tab di atas, sesuai hasil proses yang ingin dilihat',font=("Helvetica",9))],
          [sg.Text('Folder'), sg.In(size=(25,1), enable_events=True ,key='-FOLDER-'), sg.FolderBrowse()],
            [sg.Listbox(values=[], enable_events=True, size=(40,20),key='-FILE LIST-')],
]


images_col = [[sg.Text('You choose from the list:',font=("Helvetica",9))],
              [sg.Text(size=(40,1), key='-TOUT-')],
              [sg.Canvas(key='figCanvas_display')]]

image_layout = [[sg.Column(left_col), sg.VSeperator(),sg.Column(images_col, element_justification='c')]]

graph_layout_waveband = [[sg.Column([
          [sg.Text('Teori:',font=("Helvetica",11))],
          [sg.Text('Pada tab ini, ditentukan Max Depth sebagai jumlah maks dekomposisi',font=("Helvetica",9))],
          [sg.Text('berfrekuensi tinggi dan Min Depth sebagai jumlah pengurangan dekomposisi',font=("Helvetica",9))],
          [sg.Text('berfrekuensi rendah. Kedua nilai dapat dianalogikan sebagai threshold dari',font=("Helvetica",9))],
          [sg.Text('sebuah bandpass filter',font=("Helvetica",9))],
          [sg.HSeparator()],
          [sg.Text('Cara Simulasi:',font=("Helvetica",11))],
          [sg.Text('1. Atur slider Max Depth untuk menaikkan/menurunkan jumlah dekomposisi',font=("Helvetica",9))],
          [sg.Text('gambar berfrekuensi tinggi',font=("Helvetica",9))],
          [sg.Text('2. Atur slider Min Depth untuk menaikkan/menurunkan jumlah dekomposisi',font=("Helvetica",9))],
          [sg.Text('gambar berfrekuensi rendah',font=("Helvetica",9))],
          [sg.Text('3. Tekan tombol "Run!!" untuk memulai proses transformasi',font=("Helvetica",9))],
          [sg.Text('(TUNGGU PROSES HINGGA SELESAI)',font=("Helvetica",9))],
          [sg.Text('4. Tekan tombol "Decomposition/Result" untuk melihat transformasi',font=("Helvetica",9))],
          [sg.Text('per layer Y, Cb, Cr atau melihat hasil transformasi',font=("Helvetica",9))],
          [sg.HSeparator()],
          [sg.Text('Wavelet Bandpass Max Depth:',font=("Helvetica",9))],
          [sg.T('0',size=(4,1), key='-LEFTmaxband-'),
           sg.Slider((0,10),default_value=2, key='-SLIDERmaxband-', orientation='h', enable_events=True, disable_number_display=True),
           ],
          [sg.Text('Wavelet Bandpass Min Depth:')],
          [sg.T('0',size=(4,1), key='-LEFTminband-'),
           sg.Slider((0,10),default_value=0, key='-SLIDERminband-', orientation='h', enable_events=True, disable_number_display=True),
           ],
           [sg.HSeparator()],
          [sg.Text(text = "Original Size: {} bit".format(inputsize), key = '-INPUTSIZEBAND-',font=("Helvetica",9))],
          [sg.Text(text = "Wavelet Transform Reconstruction Size: {} bit".format(outputband), key = '-OUTPUTBAND-',font=("Helvetica",9))],
          [sg.Column([[sg.Button('Run!!', font=AppFont, key='-ProceedBand-')],[sg.Button(button_text='Decomposition/Result', font=AppFont, key='-ProceedBanddec-')]])]]),
          sg.VSeperator(),
          sg.Column([[sg.Canvas(key='figCanvas_wavebandres')]],visible=True,key='banddec'),
            sg.Column([[sg.Canvas(key='figCanvas_wavebanddec')]],visible=False,key='bandres')]]

graph_layout_wavetresh = [[sg.Column([
         [sg.Text('Teori:',font=("Helvetica",11))],
          [sg.Text('Pada tab ini, ditentukan nilai threshold yang menentukan nilai minimum',font=("Helvetica",9))],
          [sg.Text('per pixel dari hasil wavelet transform. Apabila nilai hasil wavelet transform',font=("Helvetica",9))],
          [sg.Text('kurang dari nilai threshold, maka nilai pixel hasil transform-nya akan',font=("Helvetica",9))],
          [sg.Text('bernilai nol',font=("Helvetica",9))],
          [sg.HSeparator()],
         [sg.Text('Cara Simulasi:',font=("Helvetica",11))],
          [sg.Text('1. Atur slider Treshold untuk menaikkan/menurunkan treshold hasil',font=("Helvetica",9))],
          [sg.Text('transformasi wavelet',font=("Helvetica",9))],
          [sg.Text('2. Tekan tombol "Run!!" untuk memulai proses transformasi',font=("Helvetica",9))],
          [sg.Text('(TUNGGU PROSES HINGGA SELESAI)',font=("Helvetica",9))],
          [sg.Text('3. Tekan tombol "Decomposition/Result" untuk melihat transformasi per',font=("Helvetica",9))],
          [sg.Text('layer Y, Cb, Cr atau melihat hasil transformasi',font=("Helvetica",9))],
          [sg.HSeparator()],
          [sg.Text('Wavelet Treshold:')],
          [sg.T('0',size=(4,1), key='-LEFTtresh-'),
           sg.Slider((0,100),default_value=0, key='-SLIDERtresh-', orientation='h', enable_events=True, disable_number_display=True),
           ],
           [sg.HSeparator()],
           [sg.Text(text = "Original Size: {} bit".format(inputsize), key = '-INPUTSIZETRESH-',font=("Helvetica",9))],
          [sg.Text(text = "Wavelet Transform Reconstruction Size: {} bit".format(outputtresh), key = '-OUTPUTTRESH-',font=("Helvetica",9))],
          [sg.Column([[sg.Button('Run!!', font=AppFont, key='-ProceedTresh-')],[sg.Button(button_text='Decomposition/Result', font=AppFont, key='-ProceedTreshdec-')]])]]),
          sg.VSeperator(),
          sg.Column([[sg.Canvas(key='figCanvas_wavetreshres')]],visible=True, key='treshdec'),
            sg.Column([[sg.Canvas(key='figCanvas_wavetreshdec')]],visible=False,key='treshres'),]]

graph_layout_quan = [[sg.Column([
        [sg.Text('Teori:',font=("Helvetica",11))],
          [sg.Text('Scalar Quantization adalah proses memetakan nilai data ke sebuah',font=("Helvetica",9))],
          [sg.Text('nilai lain dengan menggunakan sebuah satuan skalar. Pada tab ini',font=("Helvetica",9))],
          [sg.Text('ditentukan quantization value yang merupakan nilai skalar yang',font=("Helvetica",9))],
          [sg.Text('digunakan untuk membagi nilai data gambar dan membulatkannya. Proses',font=("Helvetica",9))],
          [sg.Text('selanjutnya adalah de-quantization dengan mengalikan kembali hasil',font=("Helvetica",9))],
          [sg.Text('kuantisasi dengan quantization value. Akibat pembulatan, proses',font=("Helvetica",9))],
          [sg.Text('kuantisasi yang dilakukan akan menghasilkan error pada gambar hasil',font=("Helvetica",9))],
          [sg.Text('Cara Simulasi:',font=("Helvetica",11))],
          [sg.Text('1. Atur slider quantization size untuk menaikkan/menurunkan',font=("Helvetica",9))],
          [sg.Text('nilai quantization dalam proses Scalar Quantization',font=("Helvetica",9))],
          [sg.Text('2. Tekan tombol "Run!!" untuk memulai proses',font=("Helvetica",9))],
          [sg.Text('transformasi(TUNGGU PROSES HINGGA SELESAI)',font=("Helvetica",9))],
          [sg.Text('(JANGAN HIRAUKAN "Not Responding")',font=("Helvetica",9))],
          [sg.HSeparator()],
           [sg.Text('Quantization Size for Scalar Quantization:',font=("Helvetica",9))],
           [sg.T('0',size=(4,1), key='-LEFTquan-'),
           sg.Slider((1,100),default_value=0, key='-SLIDERquan-', orientation='h', enable_events=True, disable_number_display=True),
           ],
           [sg.HSeparator()],
           [sg.Text(text = "Original Size {} bit".format(inputsize), key = '-INPUTSIZEQUAN-',font=("Helvetica",9))],
          [sg.Text(text = "Scalar Quantization Reconstruction Size: {} bit".format(outputen), key = '-OUTPUTQUAN-',font=("Helvetica",9))],
          [sg.Button('Go!!', font=AppFont, key="-Proceedquan-")]],visible=True),
          sg.Column([[sg.Canvas(key='figCanvas_quan')]]),
          sg.VSeperator()]]

graph_layout_enc = [[sg.Column([
        [sg.Text('Teori:',font=("Helvetica",11))],
          [sg.Text('Arithmetic Coding adalah proses coding yang memetakan data',font=("Helvetica",9))],
          [sg.Text('gambar ke simbol-simbol dengan menggunakan tabel frekuensi.',font=("Helvetica",9))],
          [sg.Text('Pada tab ini ditentukan nilai block size yang menunjukkan',font=("Helvetica",9))],
          [sg.Text('seberapa banyak block pixel yang direpresentasikan oleh simbol',font=("Helvetica",9))],
          [sg.Text('Cara Simulasi:',font=("Helvetica",11))],
          [sg.Text('1. Atur slider block size untuk menaikkan/menurunkan',font=("Helvetica",9))],
          [sg.Text('jumlah block dalam proses Aritmetic Encoding',font=("Helvetica",9))],
          [sg.Text('2. Tekan tombol "Run!!" untuk memulai proses',font=("Helvetica",9))],
          [sg.Text('transformasi(TUNGGU PROSES HINGGA SELESAI)',font=("Helvetica",9))],
          [sg.Text('(JANGAN HIRAUKAN "Not Responding")',font=("Helvetica",9))],
          [sg.HSeparator()],
           [sg.Text('Block Size for Arithmetic Coding:')],
           [sg.T('0',size=(4,1), key='-LEFTblock-'),
           sg.Slider((0,2),default_value=0, key='-SLIDERblock-', orientation='h', enable_events=True, disable_number_display=True),
           ],
           [sg.HSeparator()],
           [sg.Text(text = "Original Size {} bit".format(inputsize), key = '-INPUTSIZEENC-',font=("Helvetica",9))],
          [sg.Text(text = "Arithmetic Coding Reconstruction Size: {} bit".format(outputen), key = '-OUTPUTENC-',font=("Helvetica",9))],
          [sg.Button('Go!!', font=AppFont, key="-ProceedEnc-")]],visible=True),
          sg.Column([[sg.Canvas(key='figCanvas_encode')]]),
          sg.VSeperator()]]

graph_layout_res = [[sg.Column([
        [sg.Text('Teori:',font=("Helvetica",11))],
          [sg.Text('Proses kompresi JPEG2000 memiliki tiga proses utama yaitu Wavelet',font=("Helvetica",9))],
          [sg.Text('Transform, Scalar Quantization, dan Arithmetic Coding. Pada tab',font=("Helvetica",9))],
          [sg.Text('ini, dilakukan ketiga proses tersebut dengan input parameter-parameter ',font=("Helvetica",9))],
          [sg.Text('yang dapat mengubah kualitas hasil kompresi',font=("Helvetica",9))],
          [sg.Text('Cara Simulasi:',font=("Helvetica",11))],
          [sg.Text('1. Atur slider Treshold untuk menaikkan/menurunkan',font=("Helvetica",9))],
          [sg.Text('treshold hasil transformasi wavelet',font=("Helvetica",9))],
          [sg.Text('2. Atur slider quantization size untuk menaikkan/menurunkan',font=("Helvetica",9))],
          [sg.Text('nilai quantization dalam proses Scalar Quantization',font=("Helvetica",9))],
          [sg.Text('3. Atur slider block size untuk menaikkan/menurunkan',font=("Helvetica",9))],
          [sg.Text('jumlah block dalam proses Aritmetic Encoding',font=("Helvetica",9))],
          [sg.Text('4. Tekan tombol "Run!!" untuk memulai proses',font=("Helvetica",9))],
          [sg.Text('transformasi(TUNGGU PROSES HINGGA SELESAI)',font=("Helvetica",9))],
          [sg.Text('(JANGAN HIRAUKAN "Not Responding")',font=("Helvetica",9))],
          [sg.HSeparator()],
          [sg.Text('Wavelet Treshold:')],
            [sg.T('0',size=(4,1), key='-LEFTtreshres-'),
           sg.Slider((0,100),default_value=0, key='-SLIDERtreshres-', orientation='h', enable_events=True, disable_number_display=True),
           ],
           [sg.Text('Quantization Size for Scalar Quantization:')],
           [sg.T('0',size=(4,1), key='-LEFTquanres-'),
           sg.Slider((1,255),default_value=0, key='-SLIDERquanres-', orientation='h', enable_events=True, disable_number_display=True),
           ],
            [sg.Text('Block Size for Arithmetic Coding:')],
           [sg.T('0',size=(4,1), key='-LEFTblockres-'),
           sg.Slider((0,2),default_value=0, key='-SLIDERblockres-', orientation='h', enable_events=True, disable_number_display=True),
           ],
           [sg.HSeparator()],
           [sg.Text(text = "Original Size {} bit".format(inputsize), key = '-INPUTSIZERES-',font=("Helvetica",9))],
          [sg.Text(text = "JPEG2000 Reconstruction Size: {} bit".format(outputres), key = '-OUTPUTRES-',font=("Helvetica",9))],
          [sg.Button('Go!!', font=AppFont, key="-Proceedres-")]],visible=True),
          sg.Column([[sg.Canvas(key='figCanvas_res')]]),
          sg.VSeperator()]]

tab_group = [
                [sg.TabGroup(
                    [
                        [
                            sg.Tab('Browse Image', image_layout),
                            sg.Tab("Wavelet Bandpass", graph_layout_waveband),
                            sg.Tab("Wavelet Tresholding", graph_layout_wavetresh),
                            sg.Tab('Scalar Quantization', graph_layout_quan,),
                            sg.Tab('Arithmetic Coding', graph_layout_enc,),
                            sg.Tab('Complete JPEG2000 Compression', graph_layout_res,),
                        ]
                    ], 
                    
                    tab_location='centertop',
                    border_width=5, size=(1500,1200), key='BRUHH'), 
                ]                      
            ]

welcome_page = [[sg.VPush()],
          [sg.Push(), sg.Text('JPEG2000 Process Simulation', font=("Helvetica",25)), sg.Push()],
          [sg.Push(), sg.Text('Program yang mensimulasikan proses kompresi gambar berformat JPEG2000. Program akan mensimulasikan tiga proses kompresi JPEG2000 yaitu Wavelet Transform, Scalar Quantization, dan Arithmetic Encoding', font=("Helvetica",15), size=(100,5), justification='c'), sg.Push()],
          [sg.Text('Dibuat oleh Kelompok 8:', font=("Helvetica",18))],
          [sg.Push(), sg.Column([[sg.Image('asset/PrimayogaBudyprawira.png')],[sg.Text(" Nama : Primayoga Budyprawira", font=("Helvetica",11))],[sg.Text(" NPM : 1906379491", font=("Helvetica",11))]]),sg.VSeperator(),sg.Column([[sg.Image('asset/Jeremy.png')],[sg.Text(" Nama : Jeremy Filbert Baskoro", font=("Helvetica",11))],[sg.Text(" NPM : 1906299811", font=("Helvetica",11))]]), sg.Push()],
          [sg.Push(), sg.Button('Start!!',size=(30,5)), sg.Push()],
          [sg.VPush()]]

layouta = [[sg.Column(welcome_page,visible=True ,key='welcome'),sg.Column(tab_group,visible=False, key='tab_group', )]]

window = sg.Window('JPEG2000 Process Simulation',layouta ,resizable=True, finalize=True,element_justification='c', size = (1500,1000))

_VARS['window']=window
window.Maximize()

while True:

    event, values = window.read()
    if event in (sg.WIN_CLOSED, 'Exit'):
        break
    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    if event == 'Start!!':
        window['welcome'].update(visible=False)
        window['tab_group'].update(visible=True)
    
    window['-LEFTtresh-'].update(int(values['-SLIDERtresh-']))
    window['-LEFTblock-'].update(blocksize_arr[int(values['-SLIDERblock-'])])
    window['-LEFTquan-'].update(int(values['-SLIDERquan-']))
    window['-LEFTtreshres-'].update(int(values['-SLIDERtreshres-']))
    window['-LEFTblockres-'].update(blocksize_arr[int(values['-SLIDERblockres-'])])
    window['-LEFTquanres-'].update(int(values['-SLIDERquanres-']))

    if int(values['-SLIDERmaxband-'])<int(values['-SLIDERminband-']) :
        window['-LEFTmaxband-'].update(1)
        window['-LEFTminband-'].update(1)

    else :
        window['-LEFTmaxband-'].update(int(values['-SLIDERmaxband-']))
        window['-LEFTminband-'].update(int(values['-SLIDERminband-']))    
    if event == '-ProceedTresh-':
        drawChart_wavetresh(inp_image,int(values['-SLIDERtresh-']))
        window['-OUTPUTTRESH-'].update("Wavelet Transform Reconstruction Size: {} bit".format(outputtresh),font=("Helvetica",9))
        k=1
        m=1
        window.Refresh()
    if event == '-ProceedBand-':
        drawChart_waveband(inp_image,int(values['-SLIDERminband-']),int(values['-SLIDERmaxband-']))
        window['-OUTPUTBAND-'].update("Wavelet Transform Reconstruction Size: {} bit".format(outputband),font=("Helvetica",9))
        j=1
        n=1
        window.Refresh()
    if event == '-ProceedEnc-':
        drawChart_enc(inp_image,blocksize_arr[int(values['-SLIDERblock-'])])
        window['-OUTPUTENC-'].update("Entropy Coding Reconstruction Size: {} bit".format(outputen),font=("Helvetica",9))
        i=1
    if event == '-Proceedquan-':
        drawChart_quan(inp_image,int(values['-SLIDERquan-']))
        window['-OUTPUTQUAN-'].update("Entropy Coding Reconstruction Size: {} bit".format(outputquan),font=("Helvetica",9))
        r=1
    if event == '-Proceedres-':
        drawChart_result(inp_image,int(values['-SLIDERquanres-']),int(values['-SLIDERtreshres-']),blocksize_arr[int(values['-SLIDERblockres-'])])
        window['-OUTPUTRES-'].update("JPEG2000 Reconstruction Size: {} bit".format(outputres),font=("Helvetica",9))
        u = 1
    if event == '-ProceedBanddec-':
        if wa == 0: 
            window['banddec'].update(visible=True)
            window['bandres'].update(visible=False)
            wa = 1
        elif wa == 1: 
            window['banddec'].update(visible=False)
            window['bandres'].update(visible=True)
            wa = 0
    if event == '-ProceedTreshdec-':
        if wb == 0: 
            window['treshdec'].update(visible=True)
            window['treshres'].update(visible=False)
            wb = 1
        elif wb == 1: 
            window['treshdec'].update(visible=False)
            window['treshres'].update(visible=True)
            wb = 0    
    if event == '-FOLDER-':                         # Folder name was filled in, make a list of files in the folder
        folder = values['-FOLDER-']
        try:
            file_list = os.listdir(folder)         # get list of files in folder
        except:
            file_list = []
        fnames = [f for f in file_list if os.path.isfile(
            os.path.join(folder, f)) and f.lower().endswith((".png", ".jpg", "jpeg", ".tiff", ".bmp"))]
        window['-FILE LIST-'].update(fnames)
    elif event == '-FILE LIST-':    # A file was chosen from the listbox
         
        try:
            filename = os.path.join(values['-FOLDER-'], values['-FILE LIST-'][0])
            window['-TOUT-'].update(filename)
            image = convert_to_bytes(filename)
            drawChart_display(image)
            l = 1
            window['-INPUTSIZEBAND-'].update("Original Size: {} bit".format(inputsize),font=("Helvetica",9))
            window['-INPUTSIZETRESH-'].update("Original Size: {} bit".format(inputsize),font=("Helvetica",9))
            window['-INPUTSIZEENC-'].update("Original Size: {} bit".format(inputsize),font=("Helvetica",9))
            window['-INPUTSIZEQUAN-'].update("Original Size: {} bit".format(inputsize),font=("Helvetica",9))
            window['-INPUTSIZERES-'].update("Original Size: {} bit".format(inputsize),font=("Helvetica",9))
            inp_image = convert_to_bytes(filename)
            window.Refresh()
        except Exception as E:
            print(f'** Error {E} **')
            pass        # something weird happened making the full filename
# --------------------------------- Close & Exit ---------------------------------

window.close()
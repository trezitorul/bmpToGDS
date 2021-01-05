from PIL import Image
import numpy as np 
import gdspy


def bmpToGDS(bmp, width, height, layer, datatype, black=0):
    """
    Args:
        bmp: A string refering to the file location of the BMP file
        width: Physical Width (X) of the bmp image specified in micrometers
        height: Physical Height (Y) of the bmp image 
        layer: Layer the bmp file should be placed in the GDS file
        datatype: datatype of the layer 
        black: Pixel value that refers to black, all other pixel values are rendered white
    Returns: 
        gdspy polygon
    """
    origIm=Image.open(bmp)
    origArr=np.asarray(origIm.convert("L")).copy()
    bwArr=BWConverter(origArr,black=black)
    print(len(bwArr[bwArr==0]))
    gdsPoly=bwToGDS(width, height, bwArr, layer, datatype)
    return gdsPoly
    #return origArr

def BWConverter(ImArr,black=0):
    """
    Args:
        ImArr: Numpy Array Holding 
        black: The value of the pixels that should be considered Black
    Returns:
        bw: A numpy array representation of the image, can be converted back to a BMP will Image.fromArray(bw)
    """
    bw=ImArr.copy()
    print(len(bw[bw==black]))
    bw[bw!=black]=255
    bw[bw==black]=0

    return bw

def bwToGDS(Width, Height, bwArray, layer, datatype):
    #Converts a black and white 
    """
    Args:
        Width: The width of the bmp in the GDSPY base units (1 unit = 1um by default)
        Height: The height of the bmp in the GDSPY base unit (1 unit = 1um by default)
        bwArray: The black and white image for layout
        layer: Layer the BMP should be placed on in the GDS Layout
        datatype: The datatype of the bmp when placed in the GDS Layout
    Returns:
        A GDSPY polygon
    """
    black=0
    YRes=len(bwArray)
    XRes=len(bwArray[0])
    pX=Width/XRes
    pY=Height/YRes
    rects=[]
    for i in range(len(bwArray)):
        for j in range(len(bwArray[0])):
            #print(bwArray[i][j])
            if bwArray[i][j]==black:
               # print("Adding Rect")
                #print((pX*i, pY*j))
                rects.append(gdspy.Rectangle((pX*j,-pY*i),(pX*(j+1), -pY*(i+1)), layer, datatype))

    patt=None
    try:
        patt=gdspy.boolean(rects[0], rects[1:], "or", max_points=0)
    except:
        None
    return patt

def getBMPVals(ImArr):
    uniqueVals=[]
    for i in range(len(ImArr)):
        for j in range(len(ImArr[0])):
            if ImArr[i][j] not in uniqueVals:
                uniqueVals.append(ImArr[i][j])
    return uniqueVals
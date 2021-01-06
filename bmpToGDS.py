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
    gdsPoly=bwToGDS(width, height, bwArr, layer, datatype)
    return gdsPoly

def BWConverter(ImArr,black=0):
    """
    Args:
        ImArr: Numpy Array Holding 
        black: The value of the pixels that should be considered Black
    Returns:
        bw: A numpy array representation of the image, can be converted back to a BMP will Image.fromArray(bw)
    """
    bw=ImArr.copy()
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
        A GDSPY polygonset
    """
    black=0 #We assume that the material is already converted to a black only version.
    YRes=len(bwArray)
    XRes=len(bwArray[0])
    pX=Width/XRes
    pY=Height/YRes
    rects=[]
    for i in range(len(bwArray)):
        for j in range(len(bwArray[0])):
            if bwArray[i][j]==black:
                rects.append(gdspy.Rectangle((pX*j,-pY*i),(pX*(j+1), -pY*(i+1)), layer, datatype))

    patt=None
    try:
        patt=gdspy.boolean(rects[0], rects[1:], "or", max_points=0)
        print("Polygonset Successfully Generated")
    except:
        print("Polygonset is Empty! Check black value and try again")
        None
    return patt

def getBMPVals(ImArr):
    #Utility for reading unique values in a bmp array, useful for identifying black color if image is not BW.
    """
    Args:
        ImArr: Numpy Array holding the bmp image
    Returns:
        List with unique values found in the bmp
    """
    uniqueVals=[]
    for i in range(len(ImArr)):
        for j in range(len(ImArr[0])):
            if ImArr[i][j] not in uniqueVals:
                uniqueVals.append(ImArr[i][j])
    return uniqueVals
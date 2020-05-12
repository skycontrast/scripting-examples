
# Intro to gdal raster mipulation and processing
# R Del Bello
# 05-2020

# Simple Open Raster and GetInfo

fn = "C:/temp/filename.tif"     #file name & location
ds = gdal.open(fn)              #create raster dataset

# print basic raster infon
print(ds.RasterXsize, dz.RasterYsize)       # (X size, Ysize)
print(ds.Getprojection())                   # projection info, authority, metrics
print(ds.GetGeoTransform())                 # top left x, cell width, top left y, cell height(negative for North Up Rasters)   
print("Raster Bands:", ds.RasterCount)      # get raster info

# get no data value from raster band, min, max....

band1 - ds.GetRasterBand(1)
print("No Data value", band1.GetNoDataValue())
print("min value", band1.GetMinimum())
print("max value", band1.GetMaximum())
print("datatype", band1.GetUnitType())

# Read Raster as Numpy Arrays
fn = "C:/temp/filename.tif"
ds = gdal.Open(fn())

band1 = ds.GetRasterBand(1).ReasAsArray()                        # read raster as Numpy Arrays
print(band1.shape)                                               # (row, columns)
print(band1)                                                     # prints first values of first rows and last values with , and last rows
print(band1.max), print(band1.min()), print(band1.mean())        # basic stats

# Substract raster function
fn1 = "C:/raster1.tif"
fn2 = "C:/raster2.tif"
fnout = "C:/substraction.tif"

def openRaster(fn, access=0):
    ds = gdal.Open(fn, access)
    if ds is None:
        print("Error opening raster dataset")
    return ds

def getRasterBand(fn, band=1, access=0)
    ds = openRaster(fn, access)
    band = ds.GetRasterBand(1).ReasAsArray()
    return band


 # filename for new raster, ds to copy from, data to write, driver (tiff-jpeg-etc)
def createRasterFromCopy(fn, ds, data, driverFmt="Gtiff"):    
    driver = gdal.GetDriverByName(driverFmt)                 #
    outds = driver.CreateCopy(fn, ds, strict=0)              # create outpiut dataset - new file name, ds to copy, strict  
    outds.GetRasterBand(1).WriteArray(data)                  # 
    ds = None                                                # close data source
    outds = none                                             # close the file
    

dat1 = getRasterBand(fn1)       #raster1 , raster 2, diff
dat2 = getRasterBand(fn2)
datout = dat2-dat1
createRasterFromCopy(fnout, gdal.Open(fn1))


# Clip Raster to Poly Extent using gdal.Warp
import gdal
gdal.UseExceptions()

rasterin = ""     
shpin  = ".shp"
rasterout = ""

result =  gdal.Warp(rasout, rasin, cutlineDSName=shpin, cropToCutline=True)
iface.addRasterLayer(rasout)   #add to qgis

# Reprojection
import gdal
fn =
fout =
gda.Warp(out, fn, dstSRS='ESPG:4326, width=, height= / xRes=, yRes)    # resample
iface.addRasterLayer(out)


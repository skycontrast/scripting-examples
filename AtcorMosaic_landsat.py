#  Automating   mosaicking  using PCI Geomatica and Python 
#  By R Del Bello, 02-2020                                                                                                      
#  Automatically find raw landsat 8 imagery (no limit on number) in working directory ( d:/mosaic - could use CWD too) and perform the folling actions:              
#  Haze removal from MTL(RAW) file (hazerem); atmospheric correction (atcor); mosaic (automos)     
#  see offical PCI Documentation                                                                                                                                                                                                                          =
                                                                                                                         
from pci.hazerem import *                 # Haze removal module
from pci.atcor import *                   # Atmospheric correction module
from pci.automos import*                  # Mosaic module
from pci.fexport import *                 # File export module
import sys, os, shutil, fnmatch           # File manipulation modules
from datetime import *                    # Time stamp module
import winsound, ctypes                   # Sound module/Popup
   
# ------------------------------------------------------------------------------------------------
# Warning/Prompt for user interface - Optional
#--------------------------------------------------------------------------------------------------
print(" This script will overwrite files in the working directory. Please backup before proceeding")
if not input(" Continue? (y/n): ").lower().strip()[:1] == "y": sys.exit(1)

# -------------------------------------------------------------
# Step1. Setting up working directories
# --------------------------------------------------------------
print("="*70)
print("\t\tSTEP 1. Working directories and path initilization")
print("="*70)

working_dir = r'd:\delbello_mosaic'                           #set working directory
haze_out    = os.path.join(working_dir, 'hazerem')            #set output directory for hazerem
atcor_out   = os.path.join(working_dir, 'atcor')              #set output directory for atcor
mosaic_out  = os.path.join(working_dir, 'mosaic')             #set output directory for automos
shp_out     = os.path.join(working_dir, mosaic_out, 'shp')    #set output directory for cutlines
print(" ...Working directory initalized : %s, %s, %s, %s" % (haze_out, atcor_out, mosaic_out, shp_out))


# Clearing working directories
print(" ...Clearing all directories")
def foldz(FolderPath):
    if os.path.exists(FolderPath):                              #if path exits
        print(" ...Removing %s" % FolderPath)
        shutil.rmtree(FolderPath,ignore_errors=True)            #remote directory/ignore errors
    if not os.path.isdir(FolderPath):                           #if path does not exist   
        print(" ...Creating %s" % FolderPath)
        os.mkdir(FolderPath)                                    #create directory

   
#delete/create haze_out, atcour_out, mosaic_out, shp_out
foldz(haze_out)
foldz(atcor_out)
foldz(mosaic_out)
foldz(shp_out)


# Scan for Landsat 8 imagery and populate a list
print(" ...Scanning for Landsat8 Imagery ")
input_files = []                                          #create empty list to populate with imput files
for r, d, f in os.walk(working_dir):                      #iterate through folder
    for infile in fnmatch.filter(f, '*MTL.txt'):          #filter out all but *MTL.txt file
        input_files.append(os.path.join(r, infile))       #append to input_files 

tot = len(input_files)                                    #create tot variable for total files to process
print(" ..."+str(tot)+" images found")
print(" ...STEP 1 COMPLETED")

# -----------------------------------------------------------------------------
# Step 2. HAZE REMOVAL - Iterate on the list of files and perform  haze removal 
# Parameters : hazecov[0-100] , the percentage of haze removal to apply 
# -----------------------------------------------------------------------------
print("\t\tSTEP 2. Haze Removal : This will take a few minutes")
startTime = datetime.now()                                                      #set timer
num = 0                                                                      
for image in input_files:                                                       #for images in input_files list hazerem
    try:
        hazerem(fili    ='-'.join([image, 'MS']),                               #join "image" path with MS using "-"
                hazecov = [40],
                filo    = haze_out + "/hazerem" + str(num) + ".pix")            #create file name for hazerem files
        num +=1
        print(" ...Processing haze removal for image %d of %d" % (num,tot))
    except PCIException as e:                                                   #print error type for troubleshooting
        print (e)
    except Exception as e:
        print (e)
print(" ...STEP 2 COMPLETED." + ""*15 + "Time Taken:" + str(datetime.now() - startTime))

# --------------------------------------------------------------------------
# Step 3. Atmospheric Correction : find pix files, proceed with Atcor
# ---------------------------------------------------------------------------
startTime = datetime.now()                                #set timer
print("="*70)
print("\t\tSTEP 3. : ATMOSPHERIC CORRECTION : Please be patient...")
print("="*70)

haze_rem = []                                             #create empty list to populate with imput files
for r, d, f in os.walk(haze_out):                         #walk dir-folder-files
    for infile in fnmatch.filter(f, '*.pix'):             #filter out all but  *.pix files
        haze_rem.append(os.path.join(r, infile))          #append them to input_files list

# -------------------------------------------------------------------------------
# Iterate for every image in haze_rem and apply atcor
# mosaic_start = pix file to start the mosaic with * Optional


saz_angle = [(90-18.00963096),160.40005952]             # SAZANGL = [<zenith>, <azimuth>] and Solar zenith = 90 degrees - solar_elevation (in degrees)
num = 0
for image in (haze_rem):
    try:
        atcor(fili     = image
             ,atmdef   ="desert"
             ,atmcond  ="winter"
             ,cfile =  r'D:\mosaic\landsat8_oli_template.cal'                    #sensor calibration file for landsat8
             ,outunits ="Scaled_Reflectance,10.00"
             ,sazangl = saz_angle
             ,meanelev = [400]                                                   #mean elevation of scene set to 400 
             ,filo     = atcor_out + "/atcor" + str(num) + ".pix")               #output files
             
        num += 1
        print(" ...Processing atmospheric correction for image %d of %d" % (num,tot))
            
    except PCIException as e:
         print (e)
    except Exception as e:
         print (e)
print("...ATCOR COMPLETED. Time taken:"+ str(datetime.now() - startTime))

# ----------------------------------------------------
# Step 4 Mosaicking tiles
# -----------------------------------------------------
print("\t\tSTEP 4. : MOSAICKING : Please be patient")
automos(     mfile    = atcor_out
            ,dbiclist = "4,3,2"                               # bands to process
            ,mostype  = 'full'
            ,filo     = mosaic_out + "/" + "mosaic.pix"
            #startimg = mos_start,                            # by default number one / refer to line 101 to modify
            ,radiocor = 'adaptive'
            ,balmthd  = 'overlay'                             
            ,cutmthd  = 'mindiff'
            ,filvout  = shp_out + "/" + "cutlines.shp")       # output for cutlines

# -----------------------------------------------------            
# Step 5 Export Pix to Tif/PNG
# -----------------------------------------------------
fexport(       fili  = mosaic_out + "/" + "mosaic.pix"        # Input pix
              ,filo  = mosaic_out + "/" + "mosaic.tif"
              ,dbic  = [1,2,3]                                # Channels
              ,ftype ="TIF" )

winsound.MessageBeep()
ctypes.windll.user32.MessageBoxW(0, "Sucess! All Landsat 8 Imagering sucessfully mosaicked. Don't forget to save your files before executing again", "Message", 1)

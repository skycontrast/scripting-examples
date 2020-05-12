# --------------------------------------------------------------------------------------------------------
# Author: DelBello, R | February 2020
# Script: Landsat7_MTL_PCA.py
# This script will:
# Locate metadata from Landsat7, locate the clip file (must be shp), perform clipping,
# Add raster channels to clipped image,  perform PCA and place Eigien channels, export report, pix and tif
#----------------------------------------------------------------------------------------------------------


from pci.fimport import *                                 # Used to import shp as pix
from pci.fexport import *                                 # Export files to new fomats
import sys, os, shutil, fnmatch                           # File manipulation modules
from pci.pcimod import *                                  # Add channels to pix
from pci.clip import *                                    # clip an image
from pci.pca import *                                     # PCA  module
from pci.nspio import Report, enableDefaultReport         # Enables pca report export
from pci.exceptions import*                               # PCI exceptions for trouble shooting


# ------------------------------------------------------------------------------------------
# Set up working directory: raw imagery(MTL.txt), clip region(shp), and sript must live here 

working_dir = r'D:\pci_pc_lab3'
#do not touch the rest
clip_pix    = os.path.join(working_dir, 'clip_pix')    #dir containting pixfile with clip shp
clip_scene  = os.path.join(working_dir, 'clip_scene')  #dir containing the clipped scene
report_dir  = os.path.join(working_dir, 'report')      #dir containing report
final_dir   = os.path.join(working_dir, 'PCA')

rep_file = report_dir + "/" + "report.txt"             #this is the name of the PCA report file

#clear folder function for rerunability
def folderz(FolderPath):
    if os.path.exists(FolderPath):                              #if path exits
        print(" ...Removing %s" % FolderPath)
        shutil.rmtree(FolderPath,ignore_errors=True)            #remote directory/ignore errors
    if not os.path.isdir(FolderPath):                           #if path does not exist   
        print(" ...Creating %s" % FolderPath)
        os.mkdir(FolderPath)

#make list funcion to place specific files in a list within a specified  directory
def makelist(rootdir='.', suffix=''):
    return [os.path.join(looproot, filename)
            for looproot, _, filenames in os.walk(rootdir)
            for filename in filenames if filename.endswith(suffix)]

#---------------------------------------------
# Part 1: Clear working directories
#---------------------------------------------

#user prompt y/n
print(" ="*18+"Please Read Carefully"+" ="*18)
print(" This script will overwrite files in the working directory. (clip_pix, clip_scene, report, PCA) Please backup before proceeding")
if not input(" Continue? (y/n): ").lower().strip()[:1] == "y": sys.exit(1)

print(' ...Part 1 : Setting up directories')
folderz(clip_pix)
folderz(clip_scene)
folderz(report_dir)
folderz(final_dir)
print(' ...Part 1 completed')

#------------------------------------------
# Part2: Clip Imagery with SHP file 
#------------------------------------------

print("... Part 2: Clipping Scene")
#make a list for shp file of clipping area                                        
input_shp  = (makelist(rootdir =working_dir, suffix = '.shp'))
#import shp file as pix with one vector layer
for shp in input_shp:
    try:
        fili = shp
        filo = working_dir + "/" + "clip_pix" + "/" +"clip.pix"
        fimport(fili, filo)
    except PCIException as e:
         print (e)
    except Exception as e:
         print (e)

# clip scene using pix file with the vector layer
input_meta = (makelist(rootdir = working_dir, suffix = 'MTL.txt'))
for image in input_meta:
    try:
        fili ='-'.join([image, 'MS'])
        dbic = [1,2,3,4,5,6]                            
        dbsl = []
        sltype = ""
        filo = clip_scene + '/' + "scene_clipped.pix"
        ftype = "PIX"
        foptions = ""
        clipmeth = "FILE"
        clipfil = clip_pix + "/" + "clip.pix"
        cliplay = [1]
        laybnds = "SHAPES"
        coordtyp = ""
        clipul = ""
        cliplr = ""
        clipwh = ""
        initvalu = [0]
        setnodat = "Y"
        oclipbdy = "Y"

        clip (fili, dbic, dbsl, sltype, filo, ftype, \
        foptions, clipmeth, clipfil, cliplay, \
        laybnds, coordtyp, clipul, cliplr, \
        clipwh, initvalu, setnodat, oclipbdy )
        
   
    except PCIException as e:
         print (e)
    except Exception as e:
         print (e)

print("... Part 2: Clipping Scene Completed")


#-----------------------------------------------
# Part 3 : Add Raster Channels and Perform PCA
#-----------------------------------------------

print(" ...Part 3 : Adding Raster Channels and Performing PCA")

#find clipped scene and place in a list
input_pix = (makelist(rootdir = clip_scene, suffix = '.pix'))

#add raster channels to clipped scene
for image in input_pix:
    try:     
        file = image
        pciop = "ADD"
        pcival = [6]                         # add 6 8-bit channels -->must match raw imagery 
        pcimod(file, pciop, pcival)
        
    except PCIException as e:
        print (e)
    except Exception as e:
        print (e)
print(" ...raster channels added ")



# report_dir has already been defined at the start
#rep_file = report_dir + "/" + "report.txt"
try:
    Report.clear()
    enableDefaultReport(rep_file)

    pca(file= clip_scene + "/" + "scene_clipped.pix",
        dbic=[1,2,3,4,5,6],                             #import channels
        eign=[1,2,3,4,5,6],                             #eigen channels
        dboc=[7,8,9,10,11,12],                          #where to place them (on newly created channel)
        rtype="long")
except PCIException as e:
         print (e)
except Exception as e:
         print (e)
finally:
    enableDefaultReport('Term')

#export only the channels you want to have a smaller pix file
#place the out file in folder PCA


#set location of infile and outfile for fexport
#******************************IMPORTANT : dbic [9,6,10] was chosen randomly. Choose appropriate channels for your work
pix_12band = clip_scene + "/" + "scene_clipped.pix"
pix_3band = final_dir + "/" + "halifax_pca.pix" 
channel2export = [7,8,9,10,11,12]              #choose channel here
try:
    fexport(fili = pix_12band, filo =pix_3band, dbic = channel2export)  
except PCIException as e:
    print (e)
except Exception as e:
    print (e)

tiff_3band = final_dir + "/" + "halifac_pca.tif"

try:
    fexport(fili=pix_12band, filo = tiff_3band, dbic = channel2export, ftype = "TIF" )
except PCIException as e:
    print (e)
except Exception as e:
    print (e)

#open the directory to view final image    
os.startfile(final_dir)

print("... THE END...Scripped has Sucessfully RAN ") 
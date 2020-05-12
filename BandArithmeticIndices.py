# Add channels, perform band arithmetic, band ratioing or spectral indices. Images are atmospherically corrected pix files
# by R. Del Bello - 03-2020
# dependencies include python 3.5x and PCI Geomatica(BANF)

#import libraries

from pci.fexport import *               
from datetime import *                  
from pci.pcimod import *
from pci.model import *
from pci.exceptions import*
import sys, os, shutil, fnmatch          

# Some fucntions
# Clearing working directories
print(" ...Clearing all directories")
def folderz(FolderPath):
    if os.path.exists(FolderPath):                              #if path exits
        print(" ...Removing %s" % FolderPath)
        shutil.rmtree(FolderPath,ignore_errors=True)            #remote directory/ignore errors
    if not os.path.isdir(FolderPath):                           #if path does not exist   
        print(" ...Creating %s" % FolderPath)
        os.mkdir(FolderPath)                                    #create directory

#create list from files with specifc suffix in rootdir
def fileinlist(rootdir='.', suffix=''):
    return [os.path.join(looproot, filename)
            for looproot, _, filenames in os.walk(rootdir)
            for filename in filenames if filename.endswith(suffix)]


# Step1. Setting up working directories
print("\t\tSTEP 1. Working directories and path initilization")


#####################################################
# Set working directories here
#####################################################
working_dir = r'E:\adip_script' 
atcor_out = os.path.join(working_dir, 'atcor')              
input_dir = os.path.join(working_dir, 'correctedpix')
ratio_dir = os.path.join(working_dir, 'band_ratio')
####################################################
####################################################




# clear folder 
folderz(ratio_dir)

# create working copy
src_dir="E:\\adip_script\\correctedpix\\l8_atcor_clip_sonoma.pix"
dst_dir="E:\\adip_script\\band_ratio\\sonoma_bandratio.pix"
shutil.copy(src_dir,dst_dir)

# initiate list , look in rootio_dir for pix files
pixlist = []
pixlist = (fileinlist(rootdir = ratio_dir, suffix ='.pix'))

for image in pixlist:
    try:     
        file = image
        pciop = "ADD"
        pcival = [0,0,0,5]   #add 5 32bit-real channel
        pcimod(file, pciop, pcival)
        
    except PCIException as e:
         print (e)
    except Exception as e:
         print (e)

for image in pixlist:
    try:
        file = image
        source =  "%9=(%7+%6)/(%5+%2);%10=(%4+%2)/(%5-%2);%11=10*%7-9.8*%6+2"     # enter band ratio or band math here
        print("...Applied arithmatic : "+ source)
    except PCIException as e:
        print (e)
    except Exception as e:
        print (e)   
 
# open file
os.startfile(ratio_dir)

# end 
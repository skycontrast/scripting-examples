# OBIA - Object Based Image Analysis : SVM Segmentation Batch Processing 
# R. Del Bello 03-2020
# Purpose : Batch classification using Object Oriented Image Analysis - Suport Vector Machine
# Notes   : Applied on NAIP imagery (0.6m resolution, USA aerial photography)
# Versions: Python 3.5 ; PCI Geomatica Banff 2020
# Imagery source:  https://earthexplorer.usgs.gov/

# script should be located in ..\delbello_OBIA\Python
# initial image and segmentation file should be located in ..\delbello_OBIA\Python\svm_classif
# file naming  initial image = "init_image.pix" and  initial image segmentation = "init_image_seg.pix"
# easily modify at your own needs

from pci import algo
import os
import glob
import shutil
from pci.exceptions import *

# set working directory as current working directory
work_dir = os.getcwd()
svm_dir = os.path.join(work_dir, "svm_classif")
out_dir = os.path.join(work_dir, "output_folder")

# function to delete/create directory for script re runability
def dir_initialize(FolderPath):
    if os.path.exists(FolderPath):                              #if path exits
        print("...Removing %s" % FolderPath)
        shutil.rmtree(FolderPath,ignore_errors=True)            #remote directory/ignore errors
    if not os.path.isdir(FolderPath):                           #if path does not exist
        print("...Creating %s" % FolderPath)
        os.mkdir(FolderPath)

#user prompt y/n
print("="*18+"Please Read Carefully"+"="*18)
print("This script will overwrite files in the working directory. (clip_pix, clip_scene, report, PCA) Please backup before proceeding")
if not input("Continue? (y/n): ").lower().strip()[:1] == "y": sys.exit(1)

dir_initialize(out_dir)

# # Input Variables - Pre-Existing
# # Initial Image - This image will be used to generate the training model
init_image = os.path.join(svm_dir,"init_image.pix")

# # Intial segmentation containing the training sites - *Created tions\June2015_seg.pix"
init_seg = os.path.join(svm_dir, "init_image_seg.pix")

# # Additional Images - The batch classification will be run on these images
add_images = os.path.join(work_dir, "images_to_classify")

# # Output Variables
# # Output file location
output_folder = out_dir

# # Text file containing exported attribute names
fld = os.path.join(out_dir, "att_fld.txt")

# # Training model
training_model = os.path.join(out_dir, "training_model.txt")

# # Export fields, save training model and classify initial image
print("Processing initial image:", os.path.basename(init_image))

# # OAFLDNMEXP - Export names of attribute fields from Focus Object Analyst to a text file
algo.oafldnmexp(filv=init_seg, dbvs=[2], fldnmflt="ALL_OA", tfile=fld)

# # OASVMTRAIN - Object-based SVM training
algo.oasvmtrain(filv=init_seg, dbvs=[2], tfile=fld, kernel="RBF", trnmodel=training_model)

# # OASVMCLASS - Object-based SVM classifier
algo.oasvmclass(filv=init_seg, dbvs=[2], tfile=fld, trnmodel=training_model, filo=init_seg, dbov=[2])

# # Apply training model and classify additional image in batch
print("Processing additional images in batch...")
file_list = glob.glob(os.path.join(add_images, "*.pix"))

for image in file_list:
    try:
        print("Currently processing:", os.path.basename(image))
        add_seg = os.path.join(output_folder, os.path.basename(os.path.splitext(image)[0]) + '_seg.pix')

        # OASEG (OASEGSAR) - Segment an image
        print("OASEG: Segmenting Image")
        algo.oaseg(fili=image, filo=add_seg, segscale=[16], segshape=[0.5], segcomp=[0.5])

        # OACALCATT (OACALCATTSAR) - Calculate object attributes
        print("OACALCATT: Calculating Attributes")
        algo.oacalcatt(fili=image,
                       dbic=[1,2,3,4],
                       chnalias="B01, B02, B03, B04",
                       filv=add_seg,
                       dbvs=[2],
                       filo=add_seg,
                       dbov=[2],
                       statatt="MEAN, STD",
                       geoatt="ELO, CIR, COM, REC, MJR",
                       )

        # OASVMCLASS - Object-based SVM classifier
        print("OASVMCLASS: Run Supervised Classification")
        algo.oasvmclass(filv=add_seg, dbvs=[2], tfile=fld, trnmodel=training_model, filo=add_seg, dbov=[2])

    except PCIException as e:
        print(e)
    except Exception as e:
        print(e)

#open directory
os.startfile(out_dir)

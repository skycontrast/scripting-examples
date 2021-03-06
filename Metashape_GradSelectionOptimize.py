# Script  : GradualSelectionOptimization.py
# Author  : Del Bello, Rafael
# Date    : May 2020
# Purpose : Apply a gradual selection of the sparse point cloud with iterative bundle adjustment optimization

# This script was written for the Applied Geomatics Research Group as part of a student search project investigating
# the use UAV for deformation analysis. The goal was develop the manual gradual selection SfM workflow by automating
# the iterations for point selection, bnundle adjustment(optimization) and error reduction within Agisoft Metashape Pro.

# Aknowledgements: This work was supported by Applied Geomatics Research Group who provided the data, the hardware, and
# advice throughout the project. The author would like to thank Stephen Escarzaga from NPS AKRO Natural Resources for
# the help with writing this script.

import Metashape
import math, sys

doc = Metashape.app.document  # specifies open document
chunk = doc.chunk  # specifies active chunk
T = chunk.transform.matrix
crs = chunk.crs  # coordinate reference system
pc = chunk.point_cloud  # point cloud object of sparse cloud
pc_init = len(pc.points)  # returns the amount of points in cloud

# # SET PARAMETERS HERE # #

# Reconstruction Uncertainty as RU

RU_ThreshIter = 15  # percentage of cloud removal per iteration
RU_ThreshMax = 50  # stop iteration if this percentage of points is removed
RU_Value = 15  # or stop iteration if this RU value is reached

# Projection Accuracy as PA

PA_ThreshIter = 15  # percentage of cloud removal per iteration
PA_ThreshMax = 50  # stop iteration if this percentage of points is removed
PA_Value = 2.5  # or stop iteration if this PA value is reached

# Reprojection Error

RE_Iterations = 1   # max iterations
RE_ThreshIter = 10  # percentage of clouds removal per iteration
RE_Value = 0.3  # reprojection error value

print("****Number of starting points:", pc_init)  # prints initial point number in raw sparse cloud

# Below starts the gradual selection, filtering and optimization process

# Reconstruction Uncertainty - RU
RU_init = len(pc.points)  # obtain initial count of points
total_removed = 0  # set count for points removed

# initialize boolean while loop
RU_refined = False
while RU_refined == False:

    # if values[-1] <= RU_Value:
    #    refined = True
    #    print("***Reconstruction uncertainty already filtered. Target value of",RU_Value," reached")
    #    break
    f = Metashape.PointCloud.Filter()  # initialise cloud filter based on criteria
    f.init(pc, criterion=Metashape.PointCloud.Filter.ReconstructionUncertainty)
    values = f.values.copy()
    values.sort()  # sort points for selection
    thresh = values[int(len(values) * (1 - RU_ThreshIter / 100))]  # define the selection
    f.selectPoints(thresh)  # apply selection of points
    nselected = len([p for p in pc.points if p.selected])  # fetch the amount of points selected in filter
    pc.removeSelectedPoints()  # remove points from the cloud
    print("****", nselected, " points removed during reconstruction uncertainty filtering")

    # camera optimization
    chunk.optimizeCameras(fit_f=True, fit_cx=True, fit_cy=True, fit_b1=False, fit_b2=False, fit_k1=True,
                          fit_k2=True, fit_k3=True, fit_k4=False, fit_p1=True, fit_p2=True, fit_p3=False,
                          fit_p4=False, adaptive_fitting=False, tiepoint_covariance=False)

    total_removed += nselected  # add selected points to count
    if total_removed >= RU_init * (RU_ThreshMax / 100):
        refined = True  # break loop 1
        print("***Reconstruction uncertainty filtering complete. 50% of sparse cloud removed")
        # break
    if values[-1] <= RU_Value:
        refined = True  # break loop 2
        print("***Reconstruction uncertainty filtering complete. Target value of", RU_Value, " reached")
        break

# Report Total Camera Error
sums = 0
num = 0
for camera in chunk.cameras:
    if not camera.transform:
        continue
    if not camera.reference.location:
        continue
    estimated_geoc = chunk.transform.matrix.mulp(camera.center)
    error = chunk.crs.unproject(camera.reference.location) - estimated_geoc
    error = error.norm()
    sums += error ** 2
    num += 1
print("****Total Camera Error: ", round(math.sqrt(sums / num), 3))
doc.save()

# Projection Accuracy

PA_pts_removed = 0  # tracking pts removed
PA_init = len(pc.points)  # initial points in cloud
PA_refined = False
while PA_refined == False:

    f = Metashape.PointCloud.Filter()
    f.init(pc, criterion=Metashape.PointCloud.Filter.ProjectionAccuracy)
    values = f.values.copy()
    values.sort()
    thresh = values[int(len(values) * (1 - PA_ThreshIter / 100))]
    f.selectPoints(thresh)
    nselected = len([p for p in pc.points if p.selected])
    pc.removeSelectedPoints()
    print("****", nselected, " points removed during projection accuracy filtering")
    # Camera optimization
    chunk.optimizeCameras(fit_f=True, fit_cx=True, fit_cy=True, fit_b1=False, fit_b2=False, fit_k1=True,
                          fit_k2=True, fit_k3=True, fit_k4=False, fit_p1=True, fit_p2=True, fit_p3=False,
                          fit_p4=False, adaptive_fitting=False, tiepoint_covariance=False)

    PA_pts_removed += nselected  # add points removed to count

    if PA_pts_removed >= PA_init * (PA_ThreshMax / 100):
        PA_refined = True
        print("***Projection Accuracy filtering complete. 50% of sparse cloud removed")
        break
    if values[-1] <= PA_Value:
        PA_refined = True
        print("***Projection Accuracy filtering complete. Threshold value reached")
        break

# Report Total Camera Error
sums = 0
num = 0
for camera in chunk.cameras:
    if not camera.transform:
        continue
    if not camera.reference.location:
        continue

    estimated_geoc = chunk.transform.matrix.mulp(camera.center)
    error = chunk.crs.unproject(camera.reference.location) - estimated_geoc
    error = error.norm()
    sums += error ** 2
    num += 1
print("****Total Camera Error: ", round(math.sqrt(sums / num), 3))
doc.save()


RE_refined = False
while RE_refined == False:

    threshold = RE_ThreshIter
    f = Metashape.PointCloud.Filter()
    f.init(pc, criterion=Metashape.PointCloud.Filter.ReprojectionError)
    values = f.values.copy()
    values.sort()
    thresh = values[int(len(values) * (1 - threshold / 100))]
    f.selectPoints(thresh)
    nselected = len([p for p in pc.points if p.selected])
    pc.removeSelectedPoints()
    print("****", nselected, " points removed during re-projection error filtering")
    # Camera optimization
    chunk.optimizeCameras(fit_f=True, fit_cx=True, fit_cy=True, fit_b1=True, fit_b2=True, fit_k1=True,
                          fit_k2=True, fit_k3=True, fit_k4=True, fit_p1=True, fit_p2=True, fit_p3=True,
                          fit_p4=True, adaptive_fitting=True, tiepoint_covariance=True)

    # Report Total Camera Error
    sums = 0
    num = 0
    for camera in chunk.cameras:
        if not camera.transform:
            continue
        if not camera.reference.location:
            continue

        estimated_geoc = chunk.transform.matrix.mulp(camera.center)
        error = chunk.crs.unproject(camera.reference.location) - estimated_geoc
        error = error.norm()
        sums += error ** 2
        num += 1
    print("****Total Camera Error: ", round(math.sqrt(sums / num), 3))


    if values[-1] <= RE_Value:
        RE_refined = True
        print("***Reprojection refinement achieved value of", RE_Value, "Gradual Selection and Optimization Complete")
doc.save()

# for i in range(4):
#     if (round(math.sqrt(sums / num), 3)) <= 0.20:
#         print('****Camera error has reached ~20cm')
#         doc.save()
#     else:
#         threshold = RE_ThreshIter
#         f = Metashape.PointCloud.Filter()
#         f.init(pc, criterion=Metashape.PointCloud.Filter.ReprojectionError)
#         values = f.values.copy()
#         values.sort()
#         thresh = values[int(len(values) * (1 - threshold / 100))]
#         f.selectPoints(thresh)
#         nselected = len([p for p in pc.points if p.selected])
#         pc.removeSelectedPoints()
#         print("****", nselected, " points removed during reprojection error filtering")
#         # Camera optimization
#         chunk.optimizeCameras(fit_f=True, fit_cx=True, fit_cy=True, fit_b1=True, fit_b2=True, fit_k1=True,
#                               fit_k2=True, fit_k3=True, fit_k4=True, fit_p1=True, fit_p2=True, fit_p3=True,
#                               fit_p4=True, adaptive_fitting=True, tiepoint_covariance=True)
#
#         # Report Total Camera Error
#         sums = 0
#         num = 0
#         for camera in chunk.cameras:
#             if not camera.transform:
#                 continue
#             if not camera.reference.location:
#                 continue
#
#             estimated_geoc = chunk.transform.matrix.mulp(camera.center)
#             error = chunk.crs.unproject(camera.reference.location) - estimated_geoc
#             error = error.norm()
#             sums += error ** 2
#             num += 1
#         print("****Total Camera Error: ", round(math.sqrt(sums / num), 3))
#
# doc.save()

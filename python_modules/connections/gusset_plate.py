# -*- coding: utf-8 -*-
''' Naive gusset plate model.'''

from __future__ import division
from __future__ import print_function

import xc_base
import geom
from import_export import block_topology_entities as bte

class GussetPlate(object):
    ''' Naive gusset plate model.

    :ivar gussetTip: intersection of the gusset plate with the
                      axis of its attached member.
    :ivar halfChamfer: half portion of the chamfer.
    :ivar direction: direction of the attached member.
    :ivar boltedPlateTemplate: bolted plate dimensions and bolt type and 
                                arrangement.
    :ivar contour: list of 3D points defining the gusset contour.
    '''
    def __init__(self, boltedPlateTemplate, gussetTip, halfChamfer, direction):
        ''' Constructor.

        :param boltedPlateTemplate: bolted plate dimensions and bolt type and 
                                    arrangement.
        :param gussetTip: intersection of the gusset plate with the
                          axis of its attached member.
        :param halfChamfer: half portion of the chamfer.
        :param direction: direction of the attached member.
        '''
        self.gussetTip= gussetTip
        self.halfChamfer= halfChamfer
        self.direction= direction
        self.boltedPlateTemplate= boltedPlateTemplate

    def getThickness(self):
        ''' Return the plate thickess.'''
        return self.boltedPlateTemplate.thickness
    
    def getHorizontalTopLeg(self, origin):
        '''Return the points of an horizontal top leg.

        :param origin: connection origin.
        '''
        p1= self.gussetTip+self.halfChamfer
        p2= geom.Pos3d(origin.x,origin.y,p1.z) # Horizontal leg.
        return p1, p2
        
    def getSlopedTopLeg(self, slope, legLength):
        '''Return the points of a sloped top leg.

        :param legLength: length of the returned leg.
        '''
        p1= self.gussetTip+self.halfChamfer
        halfChamferVector= self.halfChamfer.normalized()
        p2= p1-legLength*(self.direction-slope*halfChamferVector).normalized() # Sloped leg.
        return p1, p2

    def getSlopedBottomLeg(self, slope, legLength):
        '''Return the points of a sloped top leg.

        :param legLength: length of the returned leg.
        '''
        p1= self.gussetTip-self.halfChamfer
        halfChamferVector= self.halfChamfer.normalized()
        p2= p1-legLength*(self.direction+slope*halfChamferVector).normalized() # Sloped leg.
        return p1, p2
    
    def getVerticalBottomLeg(self, origin):
        '''Return the points of a verticol bottom leg.

        :param origin: connection origin.
        '''
        p1= self.gussetTip-self.halfChamfer
        p2= geom.Pos3d(p1.x,p1.y,origin.z) # Vertical leg.
        return p1, p2
    
    def getToColumnBottomLeg(self, p0, cutKnifePoint= 1.0):
        '''Return the points of a verticol bottom leg.

        :param p0: intersection of the member axis with the column.
        :param cutKnifePoint: if <1 cuts the point of the knife at
                              the contact of the leg with the column
                              surface.
        '''
        p1= self.gussetTip-self.halfChamfer
        tmp= p0-geom.Vector3d(0.0,0.0,p0.z) # vertical of the intersection
                                            # with the column.
        if(cutKnifePoint==1.0):
            p2= tmp
            p3= None
        else:
            knifeEdge= geom.Segment3d(p1, tmp)
            p3= p0-geom.Vector3d(0.0,0.0,cutKnifePoint*p0.z)
            # Horizontal plane through p3
            planeP3= geom.Plane3d(p3, geom.Vector3d(1,0,0), geom.Vector3d(0,1,0))
            # Cut the point
            p2= planeP3.getIntersection(knifeEdge)
        return p1, p2, p3

    def setContour(self, pointList):
        ''' Set the points that define the contour of the gusset plate.

        :param pointList: list of 3D points defining the gusset contour.
        '''
        self.contour= pointList

    def getBoltRefSys(self):
        ''' Return the reference system for the bolt array.'''
        boltCenter= self.gussetTip-self.direction*(self.boltedPlateTemplate.length/2.0)
        halfChamferVector= self.halfChamfer.normalized()
        return geom.Ref3d3d(boltCenter, self.direction, halfChamferVector)

    def getBoltPositions(self):
        ''' Return the positions of the bolts.'''
        boltRefSys= self.getBoltRefSys()
        return self.boltedPlateTemplate.boltArray.getPositions(boltRefSys)

    def getWeldLinesIndexes(self, verticalWeldLegSize, horizontalWeldLegSize):
        ''' Return the indexes of the points in the contour
            that define the lines that must be welded to the structure.

        :param verticalWeldLegSize: leg size for the vertical welds.
        :param horizontalWeldLegSize: leg size for the horizontal welds.
        '''
        retval= list()
        retval.append((1, 2, verticalWeldLegSize)) # vertical weld
        retval.append((2, 3, horizontalWeldLegSize)) # horizontal weld.
        return retval

    def getHoleBlocks(self, ownerId, labels= None):
        ''' Return the blocks representing the holes for the bolts.

        :param ownerId: identifier of the face with the holes.
        :param lbls: labels to assign to the newly created blocks.
        '''
        holeOwnerId= 'hole_'+ownerId # Hole owner id.
        holeLabels= labels+['holes',holeOwnerId]
        boltRefSys= self.getBoltRefSys()
        return self.boltedPlateTemplate.boltArray.getHoleBlocks(boltRefSys,holeLabels)
    
    def getWeldBlocks(self, ownerId, kPointIds, verticalWeldLegSize, horizontalWeldLegSize, labels= None):
        ''' Return the blocks representing the welds.

        :param ownerId: identifier of the face with the welds.
        :param kPointIds: identifiers of the points at weld ends.
        :param verticalWeldLegSize: leg size for the vertical welds.
        :param horizontalWeldLegSize: leg size for the horizontal welds.
        :param lbls: labels to assign to the newly created blocks.
        '''
        retval= bte.BlockData()
        weldOwnerId= 'weld_'+ownerId # weld owner id.
        weldLabels= labels+['welds',weldOwnerId]
        weldLinesIndexes= self.getWeldLinesIndexes(verticalWeldLegSize, horizontalWeldLegSize)
        for l in weldLinesIndexes:
            pA= kPointIds[l[0]]
            pB= kPointIds[l[1]]
            weldLegSize= l[2]
            weldLegSizeLabel= 'weld_leg_size_'+str(weldLegSize)
            weldBlk= bte.BlockRecord(id= -1, typ= 'line', kPoints= [pA, pB], labels= weldLabels+[weldLegSizeLabel], thk= None)
            retval.appendBlock(weldBlk)
        return retval
        
    def getBlocks(self, verticalWeldLegSize, horizontalWeldLegSize, lbls= None):
        ''' Return the blocks that define the gusset for the
            diagonal argument.

        :param verticalWeldLegSize: leg size for the vertical welds.
        :param horizontalWeldLegSize: leg size for the horizontal welds.
        :param lbls: labels to assign to the newly created blocks.
        '''
        retval= bte.BlockData()
        labels= ['gusset_plate']
        if(lbls):
            labels.extend(lbls)
        blk= retval.blockFromPoints(self.contour, labels= labels, thickness= self.boltedPlateTemplate.thickness, matId= self.boltedPlateTemplate.steelType.name)
        ownerId= 'owr_f'+str(blk.id) # owner identifier.
        blk.holes= self.getHoleBlocks(ownerId, labels) # Get the hole blocks for the new plate
        retval.extend(blk.holes)
        kPointIds= blk.getKPointIds()
        blk.weldBlocks= self.getWeldBlocks(ownerId, kPointIds, verticalWeldLegSize, horizontalWeldLegSize, labels) # Get the weld blocks for the new plate
        retval.extend(blk.weldBlocks)
        return retval

    def getBoltedPlateBlocks(self, boltedPlate, diagonal, origin, labels, side= 1):
        ''' Return the blocks corresponding to the plate
            bolted to the gusset plate.

        :param boltedPlateTemplate: bolted plate that will be attached 
                                    to this one.
        :param diagonal: element that provide the internal forces in the
                         bolted plate edge.
        :param labels: labels to put in the blocks to create.
        :param side: if side==1 put the plate at the positive side of the
                     gusset plate reference system, if side==-1 put the
                     plate at the negative side.

        :return: return the distance between the plates midplanes
                 and the blocks corresponding to the bolted plate.
        '''
        # Move the reference system.
        boltedPlateRefSys= self.getBoltRefSys()
        distBetweenPlates= (self.getThickness()+boltedPlate.thickness)*0.5*side
        vMove= boltedPlateRefSys.getKVector()*distBetweenPlates
        boltedPlateRefSys.Org+= vMove
        # Get loads on the plate edge.
        loadTag= 'loadTag_'+str(diagonal.eTag)
        diagonalOrientation= diagonal.getOrientation(origin)
        loadDirI= 'loadDirI_'+str(diagonalOrientation*diagonal.iVector)
        loadDirJ= 'loadDirJ_'+str(diagonalOrientation*diagonal.jVector)
        loadDirK= 'loadDirK_'+str(diagonalOrientation*diagonal.kVector)
        # Create blocks.
        return distBetweenPlates, boltedPlate.getBlocks(boltedPlateRefSys, labels, loadTag, loadDirI, loadDirJ, loadDirK)

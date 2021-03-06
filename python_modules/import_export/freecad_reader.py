# -*- coding: utf-8 -*-
''' Read block topology data from FreeCAD files.'''

from __future__ import division
from __future__ import print_function

__author__= "Luis C. Pérez Tato (LCPT) and Ana Ortega (AO_O)"
__copyright__= "Copyright 2020, LCPT and AO_O"
__license__= "GPL"
__version__= "3.0"
__email__= "l.pereztato@gmail.com" "ana.ortega.ort@gmail.com"

import sys
import reader_base
from scipy.spatial.distance import cdist
from misc_utils import log_messages as lmsg

# path to FreeCAD.so
FREECADPATH = '/usr/lib/freecad-daily-python2/lib/' 
if(sys.version_info.major == 3):
    FREECADPATH = '/usr/lib/freecad-daily-python3/lib/'
sys.path.append(FREECADPATH)

# import FreeCAD
import FreeCAD

class FreeCADImport(reader_base.ReaderBase):
    '''Import FreeCAD geometric entities.

     :ivar groupsToImport: list of regular expressions to be tested.
    '''
    def __init__(self,fileName,groupsToImport, getRelativeCoo, threshold= 0.01,importLines= True, importSurfaces= True):
        ''' Constructor.

           :param fileName: file name to import.
           :param grouptsToImport: list of regular expressions to be tested.
           :param getRelativeCoo: coordinate transformation to be applied to the
                                  points.
           :param importLines: if true import lines.
           :param importSurfaces: if true import surfaces.
        '''
        super(FreeCADImport, self).__init__(fileName, getRelativeCoo, threshold, importLines, importSurfaces)
        self.document= FreeCAD.openDocument(self.fileName)
        self.groupsToImport= self.getObjectsToImport(groupsToImport)
        if(len(self.groupsToImport)):
            self.kPointsNames= self.selectKPoints()
            self.importPoints()
            if(self.impLines):
                self.importLines()
            if(self.impSurfaces):
                self.importFaces()
        else:
            self.kPoints= None
        
    def getObjectsToImport(self, namesToImport):
        '''Return the object names that will be imported according to the
           regular expressions contained in the second argument.

           :param namesToImport: list of regular expressions to be tested.
        '''
        retval= []
        for obj in self.document.Objects:
            if(reader_base.nameToImport(obj.Label, namesToImport)):
                retval.append(obj.Label)
        if(len(retval)==0):
            lmsg.warning('No layers to import (names to import: '+str(namesToImport)+')')
        return retval
    
    def extractPoints(self):
        '''Extract the points from the entities argument.'''
        retval_pos= []
        retval_labels= []
        def append_point(pt, groupName, pointName, objLabels):
            '''Append the point to the lists.'''
            retval_pos.append(self.getRelativeCoo(pt))
            # group name as label.
            ptLabels= [groupName]
            # xdata as label.
            for l in objLabels:
                ptLabels.append(l)
            retval_labels.append((pointName, ptLabels))
        def append_points(vertexes, objName, groupName, objLabels):
            '''Append the points to the list.'''
            ptCount= 0
            for v in vertexes:
                pointName= objName+'.'+str(ptCount)
                append_point([v.X, v.Y, v.Z], grpName, pointName, objLabels)
                ptCount+= 1
                
        for grpName in self.groupsToImport:
            grp= self.document.getObjectsByLabel(grpName)[0]
            if(hasattr(grp,'Shape')): # Object has shape.
                objName= grp.Name
                shape= grp.Shape
                shapeType= shape.ShapeType
                objLabels= [grp.Label]
                if(shapeType=='Shell'):
                    fCount= 0
                    for f in shape.SubShapes:
                        thisFaceName= objName+'.'+str(fCount)
                        append_points(f.OuterWire.OrderedVertexes, thisFaceName, grpName, objLabels)

                        fCount+= 1                        
                else:
                    append_points(grp.Shape.Vertexes, objName, grpName, objLabels)
            elif(len(grp.OutList)>0): # Object is a group
                for obj in grp.OutList: 
                    if(hasattr(obj,'Shape')): # Object has shape.
                        objType= obj.Shape.ShapeType
                        objName= obj.Name
                        objLabels= [obj.Label]
                        if(objType=='Face'):
                            append_points(obj.Shape.Vertexes, objName, grpName, objLabels)
                
        return retval_pos, retval_labels
    
    def importPoints(self):
        ''' Import points from FreeCAD.'''
        self.points= dict()
        for obj in self.document.Objects:
            if(hasattr(obj,'Shape')):
                objType= obj.Shape.ShapeType
                pointName= obj.Name
                labelName= obj.Label
                if((objType=='Vertex') and (labelName in self.groupsToImport)):
                    vertices= [-1]
                    p= self.getRelativeCoo([float(obj.X), float(obj.Y), float(obj.Z)])
                    vertices[0]= self.getIndexNearestPoint(p)
                    self.points[pointName]= vertices
                    self.labelDict[pointName]= [labelName]
                    
    def importLines(self):
        ''' Import lines from FreeCAD file.'''
        self.lines= {}
        for obj in self.document.Objects:
            if(hasattr(obj,'Shape')):
                objType= obj.Shape.ShapeType
                lineName= obj.Name
                labelName= obj.Label
                if((objType=='Wire') and (labelName in self.groupsToImport)):
                    vertices= [-1,-1]
                    v0= obj.Shape.Vertexes[0]
                    v1= obj.Shape.Vertexes[1]
                    p1= self.getRelativeCoo([float(v0.X), float(v0.Y), float(v0.Z)])
                    p2= self.getRelativeCoo([float(v1.X), float(v1.Y), float(v1.Z)])
                    length= cdist([p1],[p2])[0][0]
                    # Try to have all lines with the
                    # same orientation.
                    idx0, idx1= self.getOrientation(p1, p2, length/1e4)
                    # end orientation.
                    vertices[0]= idx0
                    vertices[1]= idx1
                    if(vertices[0]==vertices[1]):
                        lmsg.error('Error in line '+lineName+' vertices are equal: '+str(vertices))
                    if(length>self.threshold):
                        self.lines[lineName]= vertices
                        objLabels= [labelName]
                        # # groups
                        # if(lineName in self.entitiesGroups):
                        #     objLabels.extend(self.entitiesGroups[lineName])
                        self.labelDict[lineName]= objLabels
                    else:
                        lmsg.error('line too short: '+str(p1)+','+str(p2)+str(length))

                        
    def importFaces(self):
        ''' Import faces from FreeCAD file.'''
        self.facesTree= {}
        for name in self.groupsToImport:
            self.facesTree[name]= dict()

        def import_face(faceShape, faceName, labelName):
            ''' Add the face argument to the dictionary.'''
            vertices= list()
            objPoints= list()
            for v in faceShape.OuterWire.OrderedVertexes:                    
                objPoints.append([float(v.X), float(v.Y), float(v.Z)])
            for pt in objPoints:
                p= self.getRelativeCoo(pt)
                idx= self.getIndexNearestPoint(p)
                vertices.append(idx)
            self.labelDict[faceName]= [labelName]
            facesDict[faceName]= vertices

        def import_shell(shapeContainer, faceName, labelName):
            ''' Import shell objects from the container argument.'''
            fCount= 0
            for f in shapeContainer:
                thisFaceName= faceName+'.'+str(fCount)
                import_face(f, thisFaceName, labelName)
                fCount+= 1

        def import_shape(shape, faceName, labelName):
            ''' Import simple shape.'''
            shapeType= shape.ShapeType
            if(shapeType=='Face'):
                import_face(shape, faceName, labelName)
            elif(shapeType=='Shell'):
                for s in shape.SubShapes:
                    import_shape(s, faceName, labelName)
            elif(shapeType=='Compound'):
                cCount= 0
                for ss in obj.Shape.SubShapes:
                    ssType= ss.ShapeType
                    ssName= faceName+'.'+str(cCount)
                    import_shape(ss, ssName, labelName)
                    cCount+= 1          
            elif(shapeType in ['Wire']):
                count= 0 # Nothing to do with those.
            else:
                lmsg.log('Entity with shape of type: '+shapeType+' ignored.')      
            

        for obj in self.document.Objects:
            if(hasattr(obj,'Shape')):
                shapeType= obj.Shape.ShapeType
                faceName= obj.Name
                labelName= obj.Label
                if(labelName in self.groupsToImport):
                    facesDict= self.facesTree[labelName]
                    import_shape(obj.Shape, faceName, labelName)

              
    def getNamesToImport(self):
        ''' Return the names of the objects to import.'''
        return self.groupsToImport

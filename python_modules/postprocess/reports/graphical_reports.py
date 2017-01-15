# -*- coding: utf-8 -*-

__author__= "Ana Ortega (AO_O) "
__copyright__= "Copyright 2016, AO_O" 
__license__= "GPL"
__version__= "3.0"
__email__= " ana.Ortega@ciccp.es "

import xc_base
import geom
import xc
from xcVtk.malla_ef import vtk_grafico_ef
from xcVtk.malla_ef import Fields
from postprocess import utils_display
from model.grid_based import GridModel

class RecordLoadCaseDisp(object):
  '''Generation of graphic files and adding to report-tex files for a load case
  
  :ivar loadCaseName:  name of the load case to be depicted
  :ivar loadCaseDescr: description text of the load case
  :ivar loadCaseExpr:  mathematical expression to define the load case (ex:
                   '1.0*GselfWeight+1.0*DeadLoad')
  :ivar setsToDispLoads: ordered list of sets of elements to display loads
  :ivar unitsScaleLoads: factor to apply to loads if we want to change
                   the units (defaults to 1).
  :ivar unitsLoads: text to especify the units in which loads are 
                   represented (defaults to 'units:[m,kN]')
  :ivar vectorScaleLoads: factor to apply to the vectors length in the 
                   representation of loads (defaults to 1).
  :ivar multByElemAreaLoads: boolean value that must be True if we want to 
                   represent the total load on each element 
                   (=load multiplied by element area) and False if we 
                   are going to depict the value of the uniform load 
                   per unit area (defaults to False)
  :ivar listDspRot: ordered list of displacement or rotations to be displayed
                   available components: 'uX', 'uY', 'uZ', 'rotX', rotY', 'rotZ'
                   (defaults to ['uX', 'uY', 'uZ'])
  :ivar setsToDispDspRot: ordered list of sets of elements to display displacements 
                   or rotations
  :ivar unitsScaleDispl: factor to apply to displacements if we want to change
                   the units (defaults to 1).
  :ivar unitsDispl: text to especify the units in which displacements are 
                   represented (defaults to '[m]'
  :ivar listIntForc: ordered list of internal forces to be displayed
                   as scalar field over «shell» elements
                   available components: 'N1', 'N2', 'M1', 'M2', 'Q1', 'Q2'
                   (defaults to ['N1', 'N2', 'M1', 'M2', 'Q1', 'Q2'])
  :ivar setsToDispIntForc: ordered list of sets of elements  (of type «shell»)
                   to display internal forces
  :ivar listBeamIntForc: ordered list of internal forces to be displayed 
                 as diagrams on lines for «beam» elements
                 available components: 'N', 'My', 'Mz', 'Qy', 'Qz','T'
                 (defaults to ['N', 'My', 'Mz', 'Qy', 'Qz','T'])
  :ivar setsToDispBeamIntForc: ordered list of sets of elements (of type «beam»)
                    to display internal forces (defaults to [])
  :ivar scaleDispBeamIntForc: scale to apply to displays of beam  internal 
                   forces (defaults to 1.0)
  :ivar unitsScaleForc: factor to apply to internal forces if we want to change
                   the units (defaults to 1).
  :ivar unitsForc: text to especify the units in which forces are 
                   represented (defaults to '[kN/m]')
  :ivar unitsScaleMom: factor to apply to internal moments if we want to change
                   the units (defaults to 1).
  :ivar unitsMom:  text to especify the units in which bending moments are 
                   represented (defaults to '[kN.m/m]')
  :ivar viewName:  name of the view  that contains the renderer (possible
                   options: "XYZPos", "XPos", "XNeg","YPos", "YNeg",
                   "ZPos", "ZNeg") (defaults to "XYZPos")

  '''

  def __init__(self,loadCaseName,loadCaseDescr,loadCaseExpr,setsToDispLoads,setsToDispDspRot,setsToDispIntForc):
    self.loadCaseName=loadCaseName
    self.loadCaseDescr=loadCaseDescr
    self.loadCaseExpr=loadCaseExpr
    self.setsToDispLoads=setsToDispLoads
    self.unitsScaleLoads=1.0
    self.unitsLoads='units:[m,kN]'
    self.vectorScaleLoads=1.0
    self.multByElemAreaLoads=False
    self.listDspRot=['uX', 'uY', 'uZ']
    self.setsToDispDspRot=setsToDispDspRot
    self.unitsScaleDispl=1.0
    self.unitsDispl='[m]'
    self.listIntForc=['N1', 'N2', 'M1', 'M2', 'Q1', 'Q2']
    self.setsToDispIntForc=setsToDispIntForc
    self.listBeamIntForc=['N', 'My', 'Mz', 'Qy', 'Qz','T']
    self.setsToDispBeamIntForc=[]
    self.scaleDispBeamIntForc=1.0
    self.unitsScaleForc=1.0
    self.unitsForc='[kN/m]'
    self.unitsScaleMom=1.0
    self.unitsMom='[kN.m/m]'
    self.viewName="XYZPos"

  def loadReports(self,gridmodl,pathGr,texFile,grWdt):
    '''Creates the graphics files of loads for the load case and insert them in
    a LaTex file
    
    :param gridmodl:   object of type GridModel
    :param pathGr:     directory to place figures (ex: 'text/graphics/loads/')
    :param texFile:    laTex file where to include the graphics 
                       (e.g.:'text/report_loads.tex')
    :param grWdt:      width to be applied to graphics
    '''
    labl=self.loadCaseName
    for st in self.setsToDispLoads:
      grfname=pathGr+self.loadCaseName+st.elSet.name
      capt=self.loadCaseDescr + ', ' + st.genDescr + ', '  + self.unitsLoads
      gridmodl.displayLoad(setToDisplay=st.elSet,loadCaseNm=self.loadCaseName,unitsScale=self.unitsScaleLoads,vectorScale=self.vectorScaleLoads, multByElemArea=self.multByElemAreaLoads,viewNm=self.viewName,caption= capt,fileName=grfname+'.jpg')
      gridmodl.displayLoad(setToDisplay=st.elSet,loadCaseNm=self.loadCaseName,unitsScale=self.unitsScaleLoads,vectorScale=self.vectorScaleLoads, multByElemArea=self.multByElemAreaLoads,viewNm=self.viewName,caption= capt,fileName=grfname+'.eps')
      insertGrInTex(texFile=texFile,grFileNm=grfname,grWdt=grWdt,capText=capt,labl=labl) 
    return

  def simplLCReports(self,gridmodl,pathGr,texFile,grWdt,capStdTexts):
    '''Creates the graphics files of displacements and internal forces 
    calculated for a simple load case and insert them in a LaTex file
    
    :param gridmodl:   object of type GridModel
    :param pathGr:     directory to place figures (ex: 'text/graphics/loads/')
    :param texFile:    laTex file where to include the graphics 
                       (e.g.:'text/report_loads.tex')
    :param grWdt:      width to be applied to graphics
    :param capStdTexts:dictionary with the standard captions
    '''
    lcs=GridModel.QuickGraphics(gridmodl)
    #solve for load case
    lcs.solve(loadCaseName=self.loadCaseName,loadCaseExpr=self.loadCaseExpr)
    #Displacements and rotations displays
    for st in self.setsToDispDspRot:
        for arg in self.listDspRot:
            if arg[0]=='u':
                fcUn=self.unitsScaleDispl
                unDesc=self.unitsDispl
            else:
                fcUn=1.0
                unDesc=''
            grfname=pathGr+self.loadCaseName+st.elSet.name+arg
            lcs.displayDispRot(itemToDisp=arg,setToDisplay=st.elSet,fConvUnits=fcUn,unitDescription=unDesc,fileName=grfname+'.jpg')
            lcs.displayDispRot(itemToDisp=arg,setToDisplay=st.elSet,fConvUnits=fcUn,unitDescription=unDesc,fileName=grfname+'.eps')
            capt=self.loadCaseDescr + '. ' + st.genDescr.capitalize() + ', ' + capStdTexts[arg] + ' ' + unDesc
            insertGrInTex(texFile=texFile,grFileNm=grfname,grWdt=grWdt,capText=capt)
    #Internal forces displays on sets of «shell» elements
    for st in self.setsToDispIntForc:
        for arg in self.listIntForc:
            if arg[0]=='M':
                fcUn=self.unitsScaleMom
                unDesc=self.unitsMom
            else:
                fcUn=self.unitsScaleForc
                unDesc=self.unitsForc
            grfname=pathGr+self.loadCaseName+st.elSet.name+arg
            lcs.displayIntForc(itemToDisp=arg,setToDisplay=st.elSet,fConvUnits= fcUn,unitDescription=unDesc,fileName=grfname+'.jpg')
            lcs.displayIntForc(itemToDisp=arg,setToDisplay=st.elSet,fConvUnits= fcUn,unitDescription=unDesc,fileName=grfname+'.eps')
            capt=self.loadCaseDescr + '. ' + st.genDescr.capitalize() + ', ' + capStdTexts[arg] + ' ' + unDesc
            insertGrInTex(texFile=texFile,grFileNm=grfname,grWdt=grWdt,capText=capt)
    #Internal forces displays on sets of «beam» elements
    for st in self.setsToDispBeamIntForc:
        for arg in self.listBeamIntForc:
            if arg[0]=='M':
                fcUn=self.unitsScaleMom
                unDesc=self.unitsMom
            else:
                fcUn=self.unitsScaleForc
                unDesc=self.unitsForc
            grfname=pathGr+self.loadCaseName+st.elSet.name+arg
            lcs.displayIntForcDiag(itemToDisp=arg,setToDisplay=st.elSet,fConvUnits= fcUn,scaleFactor=self.scaleDispBeamIntForc,unitDescription=unDesc,viewName=self.viewName,fileName=grfname+'.jpg')
            lcs.displayIntForcDiag(itemToDisp=arg,setToDisplay=st.elSet,fConvUnits= fcUn,scaleFactor=self.scaleDispBeamIntForc,unitDescription=unDesc,viewName=self.viewName,fileName=grfname+'.eps')
            capt=self.loadCaseDescr + '. ' + st.genDescr.capitalize() + ', ' + capStdTexts[arg] + ' ' + unDesc
            insertGrInTex(texFile=texFile,grFileNm=grfname,grWdt=grWdt,capText=capt)
    texFile.write('\\clearpage\n')
    return

def checksReports(limitStateLabel,setsToReport,argsToReport,capTexts,pathGr,texReportFile,grWdt):
    report=open(texReportFile,'w')    #report latex file
    dfDisp= vtk_grafico_ef.RecordDefDisplayEF()
    for st in setsToReport:
        for arg in argsToReport:
            attributeName= limitStateLabel + 'Sect1'
            field= Fields.getScalarFieldFromControlVar(attributeName,arg,st.elSet,None,1.0)
            capt=capTexts[limitStateLabel] + ', ' + capTexts[arg] + '. '+ st.genDescr.capitalize() + ', ' + st.sectDescr[0]
            grFileNm=pathGr+st.elSet.name+arg+'Sect1'
            field.display(defDisplay=dfDisp,caption=capt,fName=grFileNm+'.jpg')
            insertGrInTex(texFile=report,grFileNm=grFileNm,grWdt=grWdt,capText=capt)

            attributeName= limitStateLabel + 'Sect2'
            field= Fields.getScalarFieldFromControlVar(attributeName,arg,st.elSet,None,1.0)
            capt=capTexts[limitStateLabel] + ', ' + capTexts[arg] + '. '+ st.genDescr.capitalize() + ', ' + st.sectDescr[1]
            grFileNm=pathGr+st.elSet.name+arg+'Sect2'
            field.display(defDisplay=dfDisp,caption=capt,fName=grFileNm+'.jpg')
            insertGrInTex(texFile=report,grFileNm=grFileNm,grWdt=grWdt,capText=capt)
    report.close()
    return

def insertGrInTex(texFile,grFileNm,grWdt,capText,labl=''):
    '''Include a graphic in a LaTeX file
    :param texFile:    laTex file where to include the graphics 
                       (e.g.:'text/report_loads.tex')
    :param grFileNm:   name of the graphic file with path and without extension
    :param grWdt:      width to be applied to graphics
    :param capText:    text for the caption
    :param labl:       label
    '''
    texFile.write('\\begin{figure}\n')
    texFile.write('\\begin{center}\n')
    texFile.write('\\includegraphics[width='+grWdt+']{'+grFileNm+'}\n')
    texFile.write('\\caption{'+capText+'}\n')
    if labl<>'':
      texFile.write('\\label{'+labl+'}\n')
    texFile.write('\\end{center}\n')
    texFile.write('\\end{figure}\n')
    return
  

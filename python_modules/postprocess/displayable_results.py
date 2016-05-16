# -*- coding: utf-8 -*-
from postprocess import utils_display
from postprocess import LimitStateData as lsd
from postprocess import ControlVars as cv

#Codenames and descriptions of common analysis and design results.

class ResultDescription(object):
  def __init__(self,code,description,units= ''):
    '''Description of an analysis or design result to display
    code: name used to retrieve the property from de analysis object (node, element,...)
    description: phrase describing the result to represent.
    units: word describing the units (MPa, kN.m, kN,...)
    ''' 
    self.code= code
    self.description= description
    self.units= units
  def __str__(self):
    return self.code + ' ' + self.description + ' ' + self.units
  def getCaption(self):
    return self.description + ' [' + self.units + ']'
  def getReinforcementLabel(self):
    return int(self.code[-1])

def getResultsDescriptionsFromControlVar(cv):
  retval= list()
  codes= cv.getFieldNames()
  for c in codes:
    print 'code= ', c
    retval.append(ResultDescription(c,''))
  print ' retval= ', retval
  return retval

class ResultsDescriptionContainer(dict):
  ''' Results to display as figures... '''
  def __init__(self,limitStateData,lst):
    '''Results description container constructor
       limitStateData; data defining limit state check label (something like "Fatigue" or "CrackControl") and the name of the file that contains the results to display.
       lst: list of results descriptions.
    '''
    self.limitStateData= limitStateData
    for l in lst:
      self.add(l)
  def add(self,rd):
    self[rd.code]= rd
  def getBaseOutputFileName(self,partCode):
    '''Returns the basic part of the output file names.'''
    return partCode+ '_results_verif_' + self.limitStateData.label
  def getLaTeXOutputFileName(self,partCode):
    '''Return the name of the LaTeX file to write figures into.'''
    return self.getBaseOutputFileName(partCode)+'.tex'
  def getLaTeXFigureListFileName(self,partCode):
    '''Return the name of the LaTeX file to write a list explaining figures.'''
    return self.getBaseOutputFileName(partCode)+'_figure_list.tex'
  def getFigureDefinitionList(self,partToDisplay):
    '''Builds a list of figures to display.
       partToDisplay: part of the model wich will be displayed'''
    retval= list()
    for key in self.keys():
      result= self[key]
      partName= partToDisplay.partName
      index= result.getReinforcementLabel()
      txtArmature= partToDisplay.reinforcementLabels[index-1]
      print '**** key= ', key
      print '**** label= ', self.limitStateData.label
      figDef= utils_display.FigureDefinition(partName,self.limitStateData.label,key,result.description,txtArmature,result.units)
      retval.append(figDef)
    return retval
  def display(self,tp,partToDisplay):
    '''Calls TakePhoto object tp to display figures corresponding to part.
       partToDisplay: part of the model that will be displayed.'''
    latexFigsFilename= self.getLaTeXOutputFileName(partToDisplay.getShortName())
    print 'latexFigsFilename= ', latexFigsFilename
    latexListFilename= self.getLaTeXFigureListFileName(partToDisplay.getShortName())
    figList= self.getFigureDefinitionList(partToDisplay)
    tp.displayFigures(figList,latexFigsFilename,latexListFilename)


#Issues sous charges quasi-permanentes (fissuration)
qplCrackControl= lsd.quasiPermanentLoadsCrackControl
rds= ResultsDescriptionContainer(qplCrackControl,getResultsDescriptionsFromControlVar(cv.CrackControlVars()))
exit()
issQPfisFrench= ResultsDescriptionContainer(qplCrackControl,[ResultDescription("sg_sPos1","Enveloppe de contraintes maximales sous charges quasi-permanentes, face positive", 'MPa'),
    ResultDescription("NCPPos1","Effort normal associé à l'enveloppe de contraintes maximales sous charges quasi-permanentes, face positive", 'kN/m'),
    ResultDescription("MyCPPos1","Moment de flexion associé à l'enveloppe de contraintes maximales sous charges quasi-permanentes, face positive", 'm.kN/m'),
    ResultDescription("sg_sNeg1","Enveloppe de contraintes maximales sous charges quasi-permanentes, face negative", 'MPa'),
    ResultDescription("NCPNeg1","Effort normal associé à l'enveloppe de contraintes maximales sous charges quasi-permanentes, face negative", 'kN/m'),
    ResultDescription("MyCPNeg1","Moment de flexion associé à l'enveloppe de contraintes maximales sous charges quasi-permanentes, face negative", 'm.kN/m'),
    ResultDescription("sg_sPos2","Enveloppe de contraintes maximales sous charges quasi-permanentes, face positive", 'MPa'),
    ResultDescription("NCPPos2","Effort normal associé à l'enveloppe de contraintes maximales sous charges quasi-permanentes, face positive", 'kN/m'),
    ResultDescription("MyCPPos2","Moment de flexion associé à l'enveloppe de contraintes maximales sous charges quasi-permanentes, face positive", 'm.kN/m'),
    ResultDescription("sg_sNeg2","Enveloppe de contraintes maximales sous charges quasi-permanentes, face negative", 'MPa'),
    ResultDescription("NCPNeg2","Effort normal associé à l'enveloppe de contraintes maximales sous charges quasi-permanentes, face negative", 'kN/m'),
    ResultDescription("MyCPNeg2","Moment de flexion associé à l'enveloppe de contraintes maximales sous charges quasi-permanentes, face negative", 'm.kN/m')])

#Issues sous charges fréquentes (fissuration)
fqlCrackControl= lsd.freqLoadsCrackControl
issFQfisFrench= ResultsDescriptionContainer(fqlCrackControl,[ResultDescription("sg_sPos1","Enveloppe de contraintes maximales sous charges fréquentes, face positive", 'MPa'),
    ResultDescription("NCPPos1","Effort normal associé à l'enveloppe de contraintes maximales sous charges fréquentes, face positive", 'kN/m'),
    ResultDescription("MyCPPos1","Moment de flexion associé à l'enveloppe de contraintes maximales sous charges fréquentes, face positive", 'm.kN/m'),
    ResultDescription("sg_sNeg1","Enveloppe de contraintes maximales sous charges fréquentes, face negative", 'MPa'),
    ResultDescription("NCPNeg1","Effort normal associé à l'enveloppe de contraintes maximales sous charges fréquentes, face negative", 'kN/m'),
    ResultDescription("MyCPNeg1","Moment de flexion associé à l'enveloppe de contraintes maximales sous charges fréquentes, face negative", 'm.kN/m'),
    ResultDescription("sg_sPos2","Enveloppe de contraintes maximales sous charges fréquentes, face positive", 'MPa'),
    ResultDescription("NCPPos2","Effort normal associé à l'enveloppe de contraintes maximales sous charges fréquentes, face positive", 'kN/m'),
    ResultDescription("MyCPPos2","Moment de flexion associé à l'enveloppe de contraintes maximales sous charges fréquentes, face positive", 'm.kN/m'),
    ResultDescription("sg_sNeg2","Enveloppe de contraintes maximales sous charges fréquentes, face negative", 'MPa'),
    ResultDescription("NCPNeg2","Effort normal associé à l'enveloppe de contraintes maximales sous charges fréquentes, face negative", 'kN/m'),
    ResultDescription("MyCPNeg2","Moment de flexion associé à l'enveloppe de contraintes maximales sous charges fréquentes, face negative", 'm.kN/m')])

#Issues sous charges durables - contraintes normales
nsr= lsd.normalStressesResistance
issDRnormFrench= ResultsDescriptionContainer(nsr,[ResultDescription("FCCP1","Facteur de capacité (contraintes normales) des éléments sous charges durables (ELUT2*)"),
    ResultDescription("NCP1","Effort normal associé au facteur de capacité (contraintes normales) sous charges durables", 'kN/m'),
    ResultDescription("MyCP1","Moment de flexion associé au facteur de capacité (contraintes normales) sous charges durables", 'm.kN/m'),
    ResultDescription("FCCP2","Facteur de capacité (contraintes normales) des éléments sous charges durables (ELUT2*)"),
    ResultDescription("NCP2","Effort normal associé au facteur de capacité (contraintes normales) sous charges durables", 'kN/m'),
    ResultDescription("MyCP2","Moment de flexion associé au facteur de capacité (contraintes normales) sous charges durables", 'm.kN/m')])

#Issues sous charges durables - contraintes de cisaillement
shr= lsd.shearResistance
issDRcisFrench= ResultsDescriptionContainer(lsd.shearResistance,[ResultDescription("FCCP1","Facteur de capacité (contraintes de cisaillement) des éléments sous charges durables (ELUT2*)"),
    ResultDescription("NCP1","Effort normal associé au facteur de capacité (contraintes de cisaillement) sous charges durables", 'kN/m'),
    ResultDescription("VuCP1","Effort tranchant associé au facteur de capacité (contraintes de cisaillement) sous charges durables", 'kN/m'),
    ResultDescription("FCCP2","Facteur de capacité (contraintes de cisaillement) des éléments sous charges durables (ELUT2*)"),
    ResultDescription("NCP2","Effort normal associé au facteur de capacité (contraintes de cisaillement) sous charges durables", 'kN/m'),
    ResultDescription("VuCP2","Effort tranchant associé au facteur de capacité (contraintes de cisaillement) sous charges durables", 'kN/m')])

#Fatigue
fr= lsd.fatigueResistance
issFatigueFrench= ResultsDescriptionContainer(fr,[ResultDescription("sg_sPos01","Contraintes dans l'acier sous charges permanentes, face positive", 'MPa'),
    ResultDescription("sg_sPos11","Contraintes dans l'acier sous modèle de charge de fatigue, face positive", 'MPa'),
    ResultDescription("inc_sg_sPos1","Incrément des Contraintes dans l'acier sous modèle de charge de fatigue, face positive", 'MPa'),
    ResultDescription("sg_sNeg01","Contraintes dans l'acier sous charges permanentes, face negative", 'MPa'),
    ResultDescription("sg_sNeg11","Contraintes dans l'acier sous modèle de chargge de fatigue, face negative", 'MPa'),
    ResultDescription("inc_sg_sNeg1","Incrément des contraintes dans l'acier sous modèle de charge de fatigue, face negative", 'MPa'),
    ResultDescription("inc_sg_s1","Enveloppe des incréments des contraintes dans l'acier sous modèle de charge de fatigue (faces negative et positive)", 'MPa'),
    ResultDescription("sg_c01","Contraintes dans le béton sous charges permanentes", 'MPa'),
    ResultDescription("inc_sg_c1","Incrèment des Contraintes dans le béton sous modèle de charge de fatige", 'MPa'),
    ResultDescription("N01","Effort normal sous charges permanentes", 'kN/m'),
    ResultDescription("N11","Effort normal sous modèle de charge de fatigue", 'kN/m'),
    ResultDescription("My01","Moment de flexion sous charges permanentes", 'kN m/m'),
    ResultDescription("My11","Effort tranchant sous modèle de charge de fatigue", ' kN m/m'),
    ResultDescription("Vy01","Moment de flexion sous charges permanentes", 'kN m/m'),
    ResultDescription("Vy11","Effort tranchant sous modèle de charge de fatigue", 'kN/m'),
    ResultDescription("Mu1","Valeur ultime du moment de flexion", 'kN m/m'),
    ResultDescription("Vu1","Valeur ultime de l'Effort tranchant", ' kN/m'),
    ResultDescription("sg_sPos02","Contraintes dans l'acier sous charges permanentes, face positive", 'MPa'),
    ResultDescription("sg_sPos12","Contraintes dans l'acier sous modèle de charge de fatigue, face positive", 'MPa'),
    ResultDescription("inc_sg_sPos2","Incrément des Contraintes dans l'acier sous modèle de charge de fatigue, face positive", 'MPa'),
    ResultDescription("sg_sNeg02","Contraintes dans l'acier sous charges permanentes, face negative", 'MPa'),
    ResultDescription("sg_sNeg12","Contraintes dans l'acier sous modèle de chargge de fatigue, face negative", 'MPa'),
    ResultDescription("inc_sg_sNeg2","Incrément des contraintes dans l'acier sous modèle de charge de fatigue, face negative", 'MPa'),
    ResultDescription("inc_sg_s2","Enveloppe des incréments des contraintes dans l'acier sous modèle de charge de fatigue (faces negative et positive)", 'MPa'),
    ResultDescription("sg_c02","Contraintes dans le béton sous charges permanentes", 'MPa'),
    ResultDescription("inc_sg_c2","Incrèment des Contraintes dans le béton sous modèle de charge de fatige", 'MPa'),
    ResultDescription("N02","Effort normal sous charges permanentes", 'kN/m'),
    ResultDescription("N12","Effort normal sous modèle de charge de fatigue", 'kN/m'),
    ResultDescription("My02","Moment de flexion sous charges permanentes", 'kN m/m'),
    ResultDescription("My12","Effort tranchant sous modèle de charge de fatigue", ' kN m/m'),
    ResultDescription("Vy02","Moment de flexion sous charges permanentes", 'kN m/m'),
    ResultDescription("Vy12","Effort tranchant sous modèle de charge de fatigue", 'kN/m'),
    ResultDescription("Mu2","Valeur ultime du moment de flexion", 'kN m/m'),
    ResultDescription("Vu2","Valeur ultime de l'Effort tranchant", ' kN/m')])

# #Resultados bajo cargas quasi-permanentes (fisuración)
# issQPfisEsp= ResultsDescriptionContainer(lsd.quasiPermanentLoadsCrackControl,[ResultDescription("sg_sPos1","Envolvente de tensiones máximas bajo cargas quasi-permanentes, cara positiva", 'MPa'),
#     ResultDescription("NCPPos1","Axil asociado a la envolvente de tensiones máximas bajo cargas quasi-permanentes, cara positiva", 'kN/m'),
#     ResultDescription("MyCPPos1","Momento flector asociado a la envolvente de tensiones máximas bajo cargas quasi-permanentes, cara positiva", 'm.kN/m'),
#     ResultDescription("sg_sNeg1","Envolvente de tensiones máximas bajo cargas quasi-permanentes, cara negativa", 'MPa'),
#     ResultDescription("NCPNeg1","Axil asociado a la envolvente de tensiones máximas bajo cargas quasi-permanentes, cara negativa", 'kN/m'),
#     ResultDescription("MyCPNeg1","Momento flector asociado a la envolvente de tensiones máximas bajo cargas quasi-permanentes, cara negativa", 'm.kN/m'),
#     ResultDescription("sg_sPos2","Envolvente de tensiones máximas bajo cargas quasi-permanentes, cara positiva", 'MPa'),
#     ResultDescription("NCPPos2","Axil asociado a la envolvente de tensiones máximas bajo cargas quasi-permanentes, cara positiva", 'kN/m'),
#     ResultDescription("MyCPPos2","Momento flector asociado a la envolvente de tensiones máximas bajo cargas quasi-permanentes, cara positiva", 'm.kN/m'),
#     ResultDescription("sg_sNeg2","Envolvente de tensiones máximas bajo cargas quasi-permanentes, cara negativa", 'MPa'),
#     ResultDescription("NCPNeg2","Axil asociado a la envolvente de tensiones máximas bajo cargas quasi-permanentes, cara negativa", 'kN/m'),
#     ResultDescription("MyCPNeg2","Momento flector asociado a la envolvente de tensiones máximas bajo cargas quasi-permanentes, cara negativa", 'm.kN/m')])

# #Resultados bajo cargas frecuentes (fissuration)
# issFQfisEsp= ResultsDescriptionContainer(lsd.freqLoadsCrackControl, [ResultDescription("sg_sPos1","Envolvente de tensiones máximas bajo cargas frecuentes, cara positiva", 'MPa'),
#     ResultDescription("NCPPos1","Axil asociado a la envolvente de tensiones máximas bajo cargas frecuentes, cara positiva", 'kN/m'),
#     ResultDescription("MyCPPos1","Momento flector asociado a la envolvente de tensiones máximas bajo cargas frecuentes, cara positiva", 'm.kN/m'),
#     ResultDescription("sg_sNeg1","Envolvente de tensiones máximas bajo cargas frecuentes, cara negativa", 'MPa'),
#     ResultDescription("NCPNeg1","Axil asociado a la envolvente de tensiones máximas bajo cargas frecuentes, cara negativa", 'kN/m'),
#     ResultDescription("MyCPNeg1","Momento flector asociado a la envolvente de tensiones máximas bajo cargas frecuentes, cara negativa", 'm.kN/m'),
#     ResultDescription("sg_sPos2","Envolvente de tensiones máximas bajo cargas frecuentes, cara positiva", 'MPa'),
#     ResultDescription("NCPPos2","Axil asociado a la envolvente de tensiones máximas bajo cargas frecuentes, cara positiva", 'kN/m'),
#     ResultDescription("MyCPPos2","Momento flector asociado a la envolvente de tensiones máximas bajo cargas frecuentes, cara positiva", 'm.kN/m'),
#     ResultDescription("sg_sNeg2","Envolvente de tensiones máximas bajo cargas frecuentes, cara negativa", 'MPa'),
#     ResultDescription("NCPNeg2","Axil asociado a la envolvente de tensiones máximas bajo cargas frecuentes, cara negativa", 'kN/m'),
#     ResultDescription("MyCPNeg2","Momento flector asociado a la envolvente de tensiones máximas charges frecuentes, cara negativa", 'm.kN/m')])
 
# #Resultados bajo cargas durables - tensiones normales
# issDRnormEsp= ResultsDescriptionContainer(lsd.normalStressesResistance,[ResultDescription("FCCP1","Factor de capacidad (tensiones normales) de los elementos bajo cargas durables (ELUT2*)"),
#     ResultDescription("NCP1","Axil asociado al factor de capacidad (tensiones normales) bajo cargas durables", 'kN/m'),
#     ResultDescription("MyCP1","Momento flector asociado al factor de capacidad (tensiones normales) bajo cargas durables", 'm.kN/m'),
#     ResultDescription("FCCP2","Factor de capacidad (tensiones normales) de los elementos bajo cargas durables (ELUT2*)"),
#     ResultDescription("NCP2","Axil asociado al factor de capacidad (tensiones normales) bajo cargas durables", 'kN/m'),
#     ResultDescription("MyCP2","Momento flector asociado al factor de capacidad (tensiones normales) bajo cargas durables", 'm.kN/m')])
 
# #Resultados bajo cargas durables - tensiones tangenciales
# issDRcisEsp= ResultsDescriptionContainer(lsd.shearResistance,[ResultDescription("FCCP1","Factor de capacidad (tensiones tangenciales) de los elementos bajo cargas durables (ELUT2*)"),
#     ResultDescription("NCP1","Axil asociado al factor de capacidad (tensiones tangenciales) bajo cargas durables", 'kN/m'),
#     ResultDescription("VuCP1","Esfuerzo cortante asociado al factor de capacidad (tensiones tangenciales) bajo cargas durables", 'kN/m'),
#     ResultDescription("FCCP2","Factor de capacidad (tensiones tangenciales) de los elementos bajo cargas durables (ELUT2*)"),
#     ResultDescription("NCP2","Axil asociado al factor de capacidad (tensiones tangenciales) bajo cargas durables", 'kN/m'),
#     ResultDescription("VuCP2","Esfuerzo cortante asociado al factor de capacidad (tensiones tangenciales) bajo cargas durables", 'kN/m')])

# #Fatiga
# issFatigueEsp= ResultsDescriptionContainer(lsd.fatigueResistance,[ResultDescription("sg_sPos01","Tensiones en el acero bajo cargas permanentes, cara positiva", 'MPa'),
#     ResultDescription("sg_sPos11","Tensiones en el acero bajo el modelo de carga de fatiga, cara positiva", 'MPa'),
#     ResultDescription("inc_sg_sPos1","Incremento de tensiones en el acero bajo el modelo de carga de fatiga, cara positiva", 'MPa'),
#     ResultDescription("sg_sNeg01","Tensiones en el acero bajo cargas permanentes, cara negativa", 'MPa'),
#     ResultDescription("sg_sNeg11","Tensiones en el acero bajo el modelo de carga de fatiga, cara negativa", 'MPa'),
#     ResultDescription("inc_sg_sNeg1","Incremento de tensión en el acero bajo el modelo de carga de fatiga, cara negativa", 'MPa'),
#     ResultDescription("inc_sg_s1","Envolvente del incremento de tensión en el acero bajo el modelo de carga de fatiga (faces negative et positive)", 'MPa'),
#     ResultDescription("sg_c01","Tensiones en el hormigón bajo cargas permanentes", 'MPa'),
#     ResultDescription("inc_sg_c1","Incremento de tensiones en el hormigón bajo el modelo de carga de fatiga", 'MPa'),
#     ResultDescription("N01","Axil bajo cargas permanentes", 'kN/m'),
#     ResultDescription("N11","Axil bajo el modelo de carga de fatiga", 'kN/m'),
#     ResultDescription("My01","Momento flector bajo cargas permanentes", 'kN m/m'),
#     ResultDescription("My11","Esfuerzo cortante bajo el modelo de carga de fatiga", ' kN m/m'),
#     ResultDescription("Vy01","Momento flector bajo cargas permanentes", 'kN m/m'),
#     ResultDescription("Vy11","Esfuerzo cortante bajo el modelo de carga de fatiga", 'kN/m'),
#     ResultDescription("Mu1","Valeur ultime du moment de flexion", 'kN m/m'),
#     ResultDescription("Vu1","Valeur ultime de l'Esfuerzo cortante", ' kN/m'),
#     ResultDescription("sg_sPos02","Tensiones en el acero bajo cargas permanentes, cara positiva", 'MPa'),
#     ResultDescription("sg_sPos12","Tensiones en el acero bajo el modelo de carga de fatiga, cara positiva", 'MPa'),
#     ResultDescription("inc_sg_sPos2","Incremento de tensiones en el acero bajo el modelo de carga de fatiga, cara positiva", 'MPa'),
#     ResultDescription("sg_sNeg02","Tensiones en el acero bajo cargas permanentes, cara negativa", 'MPa'),
#     ResultDescription("sg_sNeg12","Tensiones en el acero sous modèle de charge de fatigue, cara negativa", 'MPa'),
#     ResultDescription("inc_sg_sNeg2","Incremento de tensión en el acero bajo el modelo de carga de fatiga, cara negativa", 'MPa'),
#     ResultDescription("inc_sg_s2","Envolvente del incremento de tensión en el acero bajo el modelo de carga de fatiga (faces negative et positive)", 'MPa'),
#     ResultDescription("sg_c02","Tensiones en el hormigón bajo cargas permanentes", 'MPa'),
#     ResultDescription("inc_sg_c2","Incremento de tensiones en el hormigón bajo el modelo de carga de fatiga", 'MPa'),
#     ResultDescription("N02","Axil bajo cargas permanentes", 'kN/m'),
#     ResultDescription("N12","Axil bajo el modelo de carga de fatiga", 'kN/m'),
#     ResultDescription("My02","Momento flector bajo cargas permanentes", 'kN m/m'),
#     ResultDescription("My12","Esfuerzo cortante bajo el modelo de carga de fatiga", ' kN m/m'),
#     ResultDescription("Vy02","Momento flector bajo cargas permanentes", 'kN m/m'),
#     ResultDescription("Vy12","Esfuerzo cortante bajo el modelo de carga de fatiga", 'kN/m'),
#     ResultDescription("Mu2","Valor último del momento flector", 'kN m/m'),
#     ResultDescription("Vu2","Valor último del esfuerzo cortante", ' kN/m')])

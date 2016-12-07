# -*- coding: utf-8 -*-
# Home made test
# Sign criteria for the internal forces of an elastic beam 2d element.
# 2D cantilever beam, start node  with all its 3DOF fixed, point loads on the 
# middle span (L/2)

__author__= "Luis C. Pérez Tato (LCPT) , Ana Ortega (AO_O) "
__copyright__= "Copyright 2016, LCPT, AO_O"
__license__= "GPL"
__version__= "3.0"
__email__= "l.pereztato@ciccp.es, ana.ortega@ciccp.es "

import math
import xc_base
import geom
import xc
from solution import predefined_solutions
from model import predefined_spaces
from model import fix_node_3dof
from materials import typical_materials

def getInternalForcesBeginNode(elemTag):
  ''':return: internal forces on the element's first node.''' 
  return (elementos.getElement(elemTag).getN1,elementos.getElement(elemTag).getV1,elementos.getElement(elemTag).getM1)

def getInternalForcesEndNode(elemTag):
  ''':return: internal forces on the element's last node.''' 
  return (elementos.getElement(elemTag).getN2,elementos.getElement(elemTag).getV2,elementos.getElement(elemTag).getM2)

def printResults(N1,V1,M1,N2,V2,M2,phaseRatios,phase):
  ratioMsg= 'ratio'+str(phase)
  print 'N1= ', N1, ' N2= ', N2 
  print ratioMsg+'0= ', phaseRatios[0]
  print 'V1= ',V1, 'V2= ',V2 
  print ratioMsg+'1= ', phaseRatios[1]
  print 'M1= ',M1, 'M2= ', M2
  print ratioMsg+'2= ', phaseRatios[2]

                     
# Material properties
E= 2.1e6*9.81/1e-4 # Elastic modulus (Pa)
nu= 0.3 # Poisson's ratio
G= E/(2*(1+nu)) # Shear modulus

# Cross section properties (IPE-80)
A= 7.64e-4 # Cross section area (m2)
Iy= 80.1e-8 # Cross section moment of inertia (m4)
Iz= 8.49e-8 # Cross section moment of inertia (m4)
J= 0.721e-8 # Cross section torsion constant (m4)

# Geometry
L= 1.5 # Bar length (m)


# Load
F= 1.5e3    # Load magnitude (kN)
xRelPtoAplic= 0.5 # x relative (compared to the total length) of the
                  # point on which the load is applied

prueba= xc.ProblemaEF()
preprocessor=  prueba.getPreprocessor
nodes= preprocessor.getNodeLoader
# Problem type
predefined_spaces.gdls_resist_materiales2D(nodes)
nodes.defaultTag= 1 #First node number.
nodes.newNodeXYZ(0,0.0,0.0)
nodes.newNodeXYZ(L,0.0,0.0)

trfs= preprocessor.getTransfCooLoader
lin= trfs.newLinearCrdTransf2d("lin")
lin.xzVector= xc.Vector([0,0,1])

# Materials
caracMecSeccion= xc.CrossSectionProperties2d()
caracMecSeccion.A= A; caracMecSeccion.E= E; caracMecSeccion.G= G;
caracMecSeccion.I= Iz; 
seccion= typical_materials.defElasticSectionFromMechProp2d(preprocessor, "seccion",caracMecSeccion)

# Elements definition
elementos= preprocessor.getElementLoader
elementos.defaultTransformation= "lin"
elementos.defaultMaterial= "seccion"
elementos.defaultTag= 1 #Tag for the next element.
beam2d= elementos.newElement("elastic_beam_2d",xc.ID([1,2]));



coacciones= preprocessor.getConstraintLoader
fix_node_3dof.fixNode000(coacciones,1)

cargas= preprocessor.getLoadLoader
casos= cargas.getLoadPatterns
#Load modulation.
ts= casos.newTimeSeries("constant_ts","ts")
casos.currentTimeSeries= "ts"
lp0= casos.newLoadPattern("default","0")
eleLoad= lp0.newElementalLoad("beam2d_point_load")
eleLoad.elementTags= xc.ID([1])
eleLoad.axialComponent= F
eleLoad.x= xRelPtoAplic
#We add the load case to domain.
casos.addToDomain("0")

# Solution 0 N
analisis= predefined_solutions.simple_static_linear(prueba)
result= analisis.analyze(1)

RF= elementos.getElement(1).getResistingForce()
(N1,V1,M1)= getInternalForcesBeginNode(1)
NTeor= F
(N2,V2,M2)= getInternalForcesEndNode(1)

ratios= list()

ratio0= abs((N1-NTeor)/N1)+abs(N2)
ratio1= abs(V1)+abs(V2)
ratio2= abs(M1)+abs(M2)
phaseRatios= [ratio0,ratio1,ratio2]
ratios.extend(phaseRatios)

# print 'RF= ',RF
# printResults(N1,V1,M1,N2,V2,M2,phaseRatios,'')

lp0.removeFromDomain()
lp1= casos.newLoadPattern("default","1")
eleLoad= lp1.newElementalLoad("beam2d_point_load")
eleLoad.elementTags= xc.ID([1])
eleLoad.transComponent= F
eleLoad.x= xRelPtoAplic
casos.addToDomain("1")

# Solution 1 V
analisis= predefined_solutions.simple_static_linear(prueba)
result= analisis.analyze(1)

RF= elementos.getElement(1).getResistingForce()
(N1,V1,M1)= getInternalForcesBeginNode(1)
V1Teor=F
M1Teor= F*xRelPtoAplic*L
(N2,V2,M2)= getInternalForcesEndNode(1)

ratio10= abs(N1)+abs(N2)
ratio11= abs((V1-V1Teor)/V1Teor)+abs(V2)
ratio12= abs((M1-M1Teor)/M1)+abs(M2)

phaseRatios= [ratio10,ratio11,ratio12]
ratios.extend(phaseRatios)

print "RF= ",RF
printResults(N1,V1,M1,N2,V2,M2,phaseRatios,'1')

result= 0.0
for r in ratios:
  result+= r*r
result= math.sqrt(result)
# print 'ratios= ',ratios
# print 'result= ',result

import os
fname= os.path.basename(__file__)
if (result<1e-10):
  print "test ",fname,": ok."
else:
  print "test ",fname,": ERROR."

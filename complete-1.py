# -*- coding: mbcs -*-


# set parameters for later use
jobName = "interlocking-1"
modelName = "i1"

from abaqus import *
from abaqusConstants import *
session.Viewport(name='Viewport: 1', origin=(0.0, 0.0), width=531.605163574219, 
    height=325.702056884766)
session.viewports['Viewport: 1'].makeCurrent()
session.viewports['Viewport: 1'].maximize()
from caeModules import *
from driverUtils import executeOnCaeStartup

from part import *
from material import *
from section import *
from assembly import *
from step import *
from interaction import *
from load import *
from mesh import *
from job import *
from sketch import *
from visualization import *
from connectorBehavior import *

executeOnCaeStartup()
Mdb()

# import the .stl
import sys
sys.path.insert(6, 
    r'/usr/SIMULIA/EstProducts/2023/linux_a64/code/python2.7/lib/abaqus_plugins/stlImport')
import stl2inp
stl2inp.STL2inp(stlfile='/home/data/schnelle/Interlocking-Simulations/complete-1.stl', 
    modelName=modelName, mergeNodesTolerance=1E-06)

# remove old model
del mdb.models['Model-1']

# create a material
mdb.models[modelName].Material(name='high-strength')
mdb.models[modelName].materials['high-strength'].Elastic(table=((
    2000000000000.0, 0.3), ))

# convert the stl and supress the warning
from abaqus import backwardCompatibility
backwardCompatibility.setValues(reportDeprecated=False)
execfile('/home/data/schnelle/Interlocking-Simulations/abq3Dmesh2geom.py', __main__.__dict__)

p = mdb.models[modelName].parts['PART-1_geom']
f = p.faces
p.AddCells(faceList = f[0:24])

mdb.models[modelName].HomogeneousSolidSection(name='Section-1',
    material='high-strength', thickness=None)
p = mdb.models[modelName].parts['PART-1_geom']
c = p.cells
cells = c.getSequenceFromMask(mask=('[#3 ]', ), )
region = p.Set(cells=cells, name='Set-1')
p = mdb.models[modelName].parts['PART-1_geom']
p.SectionAssignment(region=region, sectionName='Section-1', offset=0.0,
    offsetType=MIDDLE_SURFACE, offsetField='',
    thicknessAssignment=FROM_SECTION)

# make a step
mdb.models[modelName].StaticStep(name='Step-1', previous='Initial')

# set interactions
mdb.models[modelName].ContactProperty('IntProp-1')
mdb.models[modelName].interactionProperties['IntProp-1'].TangentialBehavior(
    formulation=FRICTIONLESS)
mdb.models[modelName].interactionProperties['IntProp-1'].NormalBehavior(
    pressureOverclosure=HARD, allowSeparation=ON,
    constraintEnforcementMethod=DEFAULT)

# delete old part
del mdb.models[modelName].parts['PART-1']

# make assembly
a2 = mdb.models[modelName].rootAssembly
p = mdb.models[modelName].parts['PART-1_geom']
a2.Instance(name='PART-1_geom-1', part=p, dependent=ON)

# create load
a1 = mdb.models[modelName].rootAssembly
s1 = a1.instances['PART-1_geom-1'].faces
side1Faces1 = s1.findAt(((3.333333, 6.666667, 10.001), ), ((6.666667, 3.333333,
    10.001), ))
region = a1.Surface(side1Faces=side1Faces1, name='Surf-6')
mdb.models[modelName].Pressure(name='Load-2', createStepName='Step-1',
    region=region, distributionType=UNIFORM, field='', magnitude=100.0,
    amplitude=UNSET)

# boundary conditions
a1 = mdb.models[modelName].rootAssembly
v1 = a1.instances['PART-1_geom-1'].vertices
verts1 = v1.findAt(((0.0, 10.0, 0.0), ), ((0.0, 0.0, 0.0), ), ((10.0, 0.0,
    0.0), ), ((10.0, 10.0, 0.0), ))
region = a1.Set(vertices=verts1, name='Set-2')
mdb.models[modelName].EncastreBC(name='BC-2', createStepName='Step-1',
    region=region, localCsys=None)

# maybe fix movement of other part as well?
# a1 = mdb.models['two-cubes'].rootAssembly
# v1 = a1.instances['PART-1_geom-1'].vertices
# verts1 = v1.getSequenceFromMask(mask=('[#f00 ]', ), )
# region = a1.Set(vertices=verts1, name='Set-4')
# mdb.models['two-cubes'].ZsymmBC(name='BC-3', createStepName='Step-1',
#     region=region, localCsys=None)

# mesh part
p = mdb.models[modelName].parts['PART-1_geom']
p.seedPart(size=1.0, deviationFactor=0.1, minSizeFactor=0.1)

# change to tet mesh
# p = mdb.models[modelName].parts['PART-1_geom']
# c = p.cells
# pickedRegions = c.findAt(((6.666667, 3.333333, 5.0), ), ((6.666667, 3.333333,
#     10.001), ))
# p.setMeshControls(regions=pickedRegions, elemShape=TET, technique=FREE)
# elemType1 = mesh.ElemType(elemCode=C3D20R)
# elemType2 = mesh.ElemType(elemCode=C3D15)
# elemType3 = mesh.ElemType(elemCode=C3D10)
# p = mdb.models[modelName].parts['PART-1_geom']
# c = p.cells
# cells = c.findAt(((6.666667, 3.333333, 5.0), ), ((6.666667, 3.333333, 10.001),
#     ))
# pickedRegions =(cells, )
# p.setElementType(regions=pickedRegions, elemTypes=(elemType1, elemType2,
#     elemType3))

# mesh itself
p = mdb.models[modelName].parts['PART-1_geom']
p.generateMesh()
a = mdb.models[modelName].rootAssembly
a1 = mdb.models[modelName].rootAssembly
# a1.regenerate()
p = mdb.models[modelName].parts['PART-1_geom']

# create job
mdb.Job(name=jobName, model=modelName, description='', type=ANALYSIS,
    atTime=None, waitMinutes=0, waitHours=0, queue=None, memory=90,
    memoryUnits=PERCENTAGE, getMemoryFromAnalysis=True,
    explicitPrecision=SINGLE, nodalOutputPrecision=SINGLE, echoPrint=OFF,
    modelPrint=OFF, contactPrint=OFF, historyPrint=OFF, userSubroutine='',
    scratch='', resultsFormat=ODB, numThreadsPerMpiProcess=1,
    multiprocessingMode=DEFAULT, numCpus=1, numGPUs=0)

# enable paralellization
mdb.jobs[jobName].setValues(numThreadsPerMpiProcess=1, numCpus=4,
    numDomains=4)


# submit the job
# mdb.jobs[jobName].submit(consistencyChecking=OFF)

# -*- coding: mbcs -*-


# set parameters for later use
jobName = "i-1-small-gaps"
interlockingName = "interlocking-1"
frameName = "frame-1"

modelName = "Model-1"

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
# import sys
# sys.path.insert(6, r'/usr/SIMULIA/EstProducts/2023/linux_a64/code/python2.7/lib/abaqus_plugins/stlImport')
# import stl2inp
# stl2inp.STL2inp(stlfile='/home/data/schnelle/Interlocking-Simulations/10x10/interlocking-1a.stl', modelName=modelName, mergeNodesTolerance=1E-8)

# stl2inp.STL2inp(stlfile='/home/data/schnelle/Interlocking-Simulations/10x10/frame-1a.stl', modelName=frameName, mergeNodesTolerance=1E-8)

# remove old model
# del mdb.models['Model-1']

step = mdb.openStep(
    '/home/data/schnelle/Interlocking-Simulations/masters/versTrans.step',
    scaleFromFile=OFF)
mdb.models[modelName].PartFromGeometryFile(name=interlockingName,
    geometryFile=step, combine=True, dimensionality=THREE_D,
    type=DEFORMABLE_BODY, scale=0.1)

step = mdb.openStep(
    '/home/data/schnelle/Interlocking-Simulations/masters/frame.step',
    scaleFromFile=OFF)
mdb.models[modelName].PartFromGeometryFile(name=frameName,
    geometryFile=step, combine=True, dimensionality=THREE_D,
    type=DEFORMABLE_BODY, scale=0.1)


# create a material
mdb.models[modelName].Material(name='high-strength')
mdb.models[modelName].materials['high-strength'].Elastic(table=(( 210e+09, 0.3), ))
mdb.models[modelName].materials['high-strength'].Density(table=((7850.0, ), ))
mdb.models[modelName].materials['high-strength'].Damping(alpha=2.0, beta=0.00000001)


# convert the stl and supress the warning
# from abaqus import backwardCompatibility
# backwardCompatibility.setValues(reportDeprecated=False)
# execfile('/home/data/schnelle/Interlocking-Simulations/10x10/abq3Dmesh2geom.py', __main__.__dict__)
# execfile('/home/data/schnelle/Interlocking-Simulations/10x10/abq3Dmesh2geom-frame.py', __main__.__dict__)

# combine models
# del mdb.models[frameName].parts['PART-1']
# del mdb.models[modelName].parts['PART-1']

# mdb.models[frameName].parts.changeKey(fromName='PART-1_geom', toName='frame')
# mdb.models[modelName].parts.changeKey(fromName='PART-1_geom', toName='interlocking')

# mdb.models[modelName].Part('frame', mdb.models[frameName].parts['frame'])

# del mdb.models[frameName]

# add models to assembly
a2 = mdb.models[modelName].rootAssembly
p = mdb.models[modelName].parts[interlockingName]
a2.Instance(name=frameName, part=p, dependent=ON)
p = mdb.models[modelName].parts[frameName]
a2.Instance(name=modelName, part=p, dependent=ON)


# delete old part from assembly
# a1 = mdb.models[modelName].rootAssembly
# del a1.features['PART-1-1']

mdb.models[modelName].HomogeneousSolidSection(name='Section-1', material='high-strength', thickness=None)

# make a step
mdb.models[modelName].ExplicitDynamicsStep(name='Step-1', previous='Initial', timePeriod=8.0, improvedDtMethod=ON)
# set 100 intervals
mdb.models['Model-1'].fieldOutputRequests['F-Output-1'].setValues(
    numIntervals=100)

# set interaction property
mdb.models[modelName].ContactProperty('IntProp-1')
mdb.models[modelName].interactionProperties['IntProp-1'].TangentialBehavior(formulation=FRICTIONLESS)
mdb.models[modelName].interactionProperties['IntProp-1'].NormalBehavior(pressureOverclosure=EXPONENTIAL, table=((1000.0, 0.0), (0.0, 1e-07)),maxStiffness=None, constraintEnforcementMethod=DEFAULT)


# create interaction from property
mdb.models[modelName].ContactExp(name='Int-1', createStepName='Initial')
mdb.models[modelName].interactions['Int-1'].includedPairs.setValuesInStep(stepName='Initial', useAllstar=ON)
mdb.models[modelName].interactions['Int-1'].contactPropertyAssignments.appendInStep(stepName='Initial', assignments=((GLOBAL, SELF, 'IntProp-1'), ))

# create an amplitude
mdb.models[modelName].SmoothStepAmplitude(name='Amp-1', timeSpan=STEP, data=((
    0.0, 0.0), (2.0, 1.0)))

# # create job
# mdb.Job(name=jobName, model=modelName, description='', type=ANALYSIS,
#     atTime=None, waitMinutes=0, waitHours=0, queue=None, memory=90,
#     memoryUnits=PERCENTAGE, getMemoryFromAnalysis=True,
#     explicitPrecision=SINGLE, nodalOutputPrecision=SINGLE, echoPrint=OFF,
#     modelPrint=OFF, contactPrint=OFF, historyPrint=OFF, userSubroutine='',
#     scratch='', resultsFormat=ODB, numThreadsPerMpiProcess=1,
#     multiprocessingMode=DEFAULT, numCpus=1, numGPUs=0)

# # enable paralellization
# mdb.jobs[jobName].setValues(numThreadsPerMpiProcess=1, numCpus=4,
#     numDomains=4)


# submit the job
# mdb.jobs[jobName].submit(consistencyChecking=OFF)

# -*- coding: mbcs -*-

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
session.viewports['Viewport: 1'].partDisplay.geometryOptions.setValues(
    referenceRepresentation=ON)
Mdb()

# import the .stl
import sys
sys.path.insert(6, 
    r'/usr/SIMULIA/EstProducts/2023/linux_a64/code/python2.7/lib/abaqus_plugins/stlImport')
import stl2inp
stl2inp.STL2inp(stlfile='/home/data/schnelle/abaqus/two-cubes.stl', 
    modelName='two-cubes', mergeNodesTolerance=1E-06)

# create a material
mdb.models['two-cubes'].Material(name='high-strength')
mdb.models['two-cubes'].materials['high-strength'].Elastic(table=((
    2000000000000.0, 0.3), ))

# convert the stl and supress the warning
from abaqus import backwardCompatibility
backwardCompatibility.setValues(reportDeprecated=False)
execfile('/home/data/schnelle/abaqus/abq3Dmesh2geom.py', __main__.__dict__)

p = mdb.models['two-cubes'].parts['PART-1_geom']
f = p.faces
p.AddCells(faceList = f[0:24])

mdb.models['two-cubes'].HomogeneousSolidSection(name='Section-1',
    material='high-strength', thickness=None)
p = mdb.models['two-cubes'].parts['PART-1_geom']
c = p.cells
cells = c.getSequenceFromMask(mask=('[#3 ]', ), )
region = p.Set(cells=cells, name='Set-1')
p = mdb.models['two-cubes'].parts['PART-1_geom']
p.SectionAssignment(region=region, sectionName='Section-1', offset=0.0,
    offsetType=MIDDLE_SURFACE, offsetField='',
    thicknessAssignment=FROM_SECTION)

# make a step
mdb.models['two-cubes'].StaticStep(name='Step-1', previous='Initial')
session.viewports['Viewport: 1'].assemblyDisplay.setValues(step='Step-1')

# set interactions
mdb.models['two-cubes'].ContactProperty('IntProp-1')
mdb.models['two-cubes'].interactionProperties['IntProp-1'].TangentialBehavior(
    formulation=FRICTIONLESS)
mdb.models['two-cubes'].interactionProperties['IntProp-1'].NormalBehavior(
    pressureOverclosure=HARD, allowSeparation=ON,
    constraintEnforcementMethod=DEFAULT)




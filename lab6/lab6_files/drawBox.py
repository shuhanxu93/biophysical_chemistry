# -*- coding: utf-8 -*-
from pymol.cgo import *
from pymol import cmd
from random import randint
from random import uniform

#############################################################################
#                                                                            
# drawBox.py -- Draws a box
#                                                                            
#############################################################################
def drawBox(x=0.0, y=0.0, z=0.0, X=10, Y=10, Z=10):
        linewidth=2.0
        r=uniform(0.5, 1.0)
        g=uniform(0.5, 1.0)
        b=uniform(0.5, 1.0)

        minX = x - X/2
        minY = y - Y/2
        minZ = z - Z/2
        maxX = x + X/2
        maxY = y + Y/2
        maxZ = z + Z/2

        w = (X+Y+Z)/90.0

        axis = [
                CONE, minX+X*0.1, minY, minZ, minX+X*0.2, minY, minZ, w, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 1.0, 
                CONE, minX, minY+Y*0.1, minZ, minX, minY+Y*0.2, minZ, w, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 1.0, 1.0, 
                CONE, minX, minY, minZ+Z*0.1, minX, minY, minZ+Z*0.2, w, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 1.0, 1.0]
       
        boundingBox = [
                LINEWIDTH, float(linewidth),

                BEGIN, LINES,
                COLOR, float(r), float(g), float(b),

                VERTEX, minX, minY, minZ,       #1
                VERTEX, minX, minY, maxZ,       #2

                VERTEX, minX, maxY, minZ,       #3
                VERTEX, minX, maxY, maxZ,       #4

                VERTEX, maxX, minY, minZ,       #5
                VERTEX, maxX, minY, maxZ,       #6

                VERTEX, maxX, maxY, minZ,       #7
                VERTEX, maxX, maxY, maxZ,       #8


                VERTEX, minX, minY, minZ,       #1
                VERTEX, maxX, minY, minZ,       #5

                VERTEX, minX, maxY, minZ,       #3
                VERTEX, maxX, maxY, minZ,       #7

                VERTEX, minX, maxY, maxZ,       #4
                VERTEX, maxX, maxY, maxZ,       #8

                VERTEX, minX, minY, maxZ,       #2
                VERTEX, maxX, minY, maxZ,       #6


                VERTEX, minX, minY, minZ,       #1
                VERTEX, minX, maxY, minZ,       #3

                VERTEX, maxX, minY, minZ,       #5
                VERTEX, maxX, maxY, minZ,       #7

                VERTEX, minX, minY, maxZ,       #2
                VERTEX, minX, maxY, maxZ,       #4

                VERTEX, maxX, minY, maxZ,       #6
                VERTEX, maxX, maxY, maxZ,       #8

                END
        ]

        boxName = "box_" + str(randint(0,10000))
        while boxName in cmd.get_names():
                boxName = "box_" + str(randint(0,10000))

        cmd.load_cgo(boundingBox + axis,boxName)
        return boxName

cmd.extend ("drawBox", drawBox)

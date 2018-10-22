#!/usr/bin/env python

import pytest
import tally
import json

"""
Placer problem:
There is an ADT grid.
+-------++-------++-------++-------++-------++-------++-------++-------+
|  <N>  ||  <N>  ||  <N>  ||  <N>  ||  <N>  ||  <N>  ||  <N>  ||  <N>  |
+---v---++---v---++---v---++---v---++---v---++---v---++---v---++---v---+
+---^---++---^---++---^---++---^---++---^---++---^---++---^---++---^---+
|  <P>  ||  <P>  ||  <P>  ||  <P>  ||  <P>  ||  <P>  ||  <P>  ||  <P>  |
+-------++-------++-------++-------++-------++-------++-------++-------+
+-------++-------++-------++-------++-------++-------++-------++-------+
|  <P>  ||  <P>  ||  <P>  ||  <P>  ||  <P>  ||  <P>  ||  <P>  ||  <P>  |
+---v---++---v---++---v---++---v---++---v---++---v---++---v---++---v---+
+---^---++---^---++---^---++---^---++---^---++---^---++---^---++---^---+
|  <N>  ||  <N>  ||  <N>  ||  <N>  ||  <N>  ||  <N>  ||  <N>  ||  <N>  |
+-------++-------++-------++-------++-------++-------++-------++-------+
+-------++-------++-------++-------++-------++-------++-------++-------+
|  <N>  ||  <N>  ||  <N>  ||  <N>  ||  <N>  ||  <N>  ||  <N>  ||  <N>  |
+---v---++---v---++---v---++---v---++---v---++---v---++---v---++---v---+
+---^---++---^---++---^---++---^---++---^---++---^---++---^---++---^---+
|  <P>  ||  <P>  ||  <P>  ||  <P>  ||  <P>  ||  <P>  ||  <P>  ||  <P>  |
+-------++-------++-------++-------++-------++-------++-------++-------+
+-------++-------++-------++-------++-------++-------++-------++-------+
|  <P>  ||  <P>  ||  <P>  ||  <P>  ||  <P>  ||  <P>  ||  <P>  ||  <P>  |
+---v---++---v---++---v---++---v---++---v---++---v---++---v---++---v---+
+---^---++---^---++---^---++---^---++---^---++---^---++---^---++---^---+
|  <N>  ||  <N>  ||  <N>  ||  <N>  ||  <N>  ||  <N>  ||  <N>  ||  <N>  |
+-------++-------++-------++-------++-------++-------++-------++-------+
Each ADT exposes nets on their left and right, so the placer must prevent shorts.
This can be modeled as a shared m1 track on the left and right boundaries of the ADT.
The placer will determine whether to flip around the y-axis, to make the necessary connections.

The cells will also need to be flipped around the x-axis depending on position in the grid.
Let's number these using the lower left corner as (0,0).
Rows where y % 4 == 0 are unflipped N ADTs.
Rows where y % 4 == 1 are   flipped P ADTs.
Rows where y % 4 == 2 are unflipped P ADTs.
Rows where y % 4 == 3 are   flipped N ADTs.


We want to be able to place larger than one ADT entities.
So we have things like this:
+---^---+
|t0<N>t1|
+-------+
or like this:
+---^---++---^---+
|t0<N>t1||t1<N>t2|
+-------++-------+
or like this:
+---^---++---^---+
|t0<P>t1||t1<P>t2|
+-------++-------+
+-------++-------+
|t2<P>t3||t3<P>t4|
+---v---++---v---+
but not anything that looks like this (can't fit anywhere in the grid):
+-------++-------+
|t0<P>t1||t1<P>t2|
+---v---++---v---+
+---^---++---^---+
|t2<P>t3||t3<P>t4|
+-------++-------+
or like this (3 adjacent N rows not in grid):
+-------++-------+
|t0<N>t1||t1<N>t2|
+---v---++---v---+
+---^---++---^---+
|t2<N>t3||t3<N>t4|
+-------++-------+
+-------++-------+
|t5<N>t6||t6<P>t7|
+---v---++---v---+
"""

class Tech:
# Mock the tech file to temporarily simplify integration
  def __init__( self):
      self.halfXADTGrid = 1
      self.halfYADTGrid = 1
      self.pitchPoly   = 720
      self.pitchDG     = 720
      self.verticalMetals = ["metal1","metal3","metal5"]
      self.horizontalMetals = ["metal2","metal4"]

class Rect:
  def __init__( self, llx=None, lly=None, urx=None, ury=None):
      self.llx = llx
      self.lly = lly
      self.urx = urx
      self.ury = ury

  def canonical( self):
      [llx,lly,urx,ury] = self.toList()
      if llx > urx: llx,urx = urx,llx
      if lly > ury: lly,ury = ury,lly
      return Rect( llx,lly,urx,ury)

  def toList( self):
      return [self.llx, self.lly, self.urx, self.ury]


class Transformation:
    def __init__( self, oX=0, oY = 0, sX=1, sY=1):
        self.oX = oX
        self.oY = oY
        self.sX = sX
        self.sY = sY

    def hit( self, p):
        x,y = p
        return self.sX * x + self.oX, self.sY * y + self.oY

    def hitRect( self, r):
        llx,lly = self.hit( (r.llx, r.lly))
        urx,ury = self.hit( (r.urx, r.ury))
        return Rect( llx, lly, urx, ury)

    def preMult( self, A):
        # A            self
        # sx 0  ox     sx 0  ox
        # 0  sy oy     0  sy oy   
        # 0  0  1      0  0  1
        C = Transformation()
        C.sX = A.sX * self.sX
        C.sY = A.sY * self.sY
        C.oX = A.sX * self.oX + A.oX
        C.oY = A.sY * self.oY + A.oY
        return C

    def postMult( self, A):
        # self         A
        # sx 0  ox     sx 0  ox
        # 0  sy oy     0  sy oy   
        # 0  0  1      0  0  1
        C = Transformation()
        C.sX = self.sX * A.sX
        C.sY = self.sY * A.sY
        C.oX = self.sX * A.oX + self.oX
        C.oY = self.sY * A.oY + self.oY
        return C

def test_transformation_hit0():
    t = Transformation( 0, 10)
    assert (0,10) == t.hit( (0,0))

def test_transformation_hit1():
    t = Transformation( 0, 10, 1, -1)
    assert (0,0) == t.hit( (0,10))

def test_transformation_preMult0():
    a = Transformation( 0, 10, 0, 0)
    b = Transformation( 0,  0, 1,-1)
    assert (0,-10) == (a.preMult(b)).hit( (0,0))

def test_transformation_postMult0():
    a = Transformation( 0, 10, 0, 0)
    b = Transformation( 0,  0, 1,-1)
    assert (0,-10) == (b.postMult(a)).hit( (0,0))

def encode_T( tech, obj):
  if isinstance(obj, Rect):
    r = Rect()
    r.llx = tech.pitchPoly*tech.halfXADTGrid*2*obj.llx
    r.urx = tech.pitchPoly*tech.halfXADTGrid*2*obj.urx
    r.lly = tech.pitchDG  *tech.halfYADTGrid*2*obj.lly
    r.ury = tech.pitchDG  *tech.halfYADTGrid*2*obj.ury 
    return r.toList()
  else:
    raise TypeError(repr(obj) + " is not JSON serializable.")

class CellTemplate:
    def __init__( self, nm):
        self.nm = nm
        
    def __repr__( self):
        return "CellTemplate(" + nm + "," + self.instances + "," + self.bbox + ")"

    def write_globalrouting_json( self, fp, tech):
        grs = []
        terminals = []

        terminals.append( { "netName" : self.nm, "layer" : "diearea", "rect" : self.bbox})
        for inst in self.instances:
            r = inst.transformation.hitRect( inst.template.bbox)
            nm = self.nm + '/' + inst.nm + ':' + inst.template.nm
            terminals.append( { "netName" : nm, "layer" : "cellarea", "rect" : r.canonical()})

        grGrid = []
        for x in range( self.bbox.llx, self.bbox.urx):
            for y in range( self.bbox.lly, self.bbox.ury):
                grGrid.append( Rect( x,y,x+1,y+1))

        data = { "bbox" : self.bbox, "globalRoutes" : grs, "globalRouteGrid" : grGrid, "terminals" : terminals}

        fp.write( json.dumps( data, indent=2, default=lambda x: encode_T(tech,x)) + "\n")


class CellLeaf(CellTemplate):
    def __init__( self, nm):
        super().__init__(nm)

    @property
    def instances( self):
        return []

    @property
    def bbox( self):
        return Rect(0,0,1,1)

class CellHier(CellTemplate):
    def __init__( self, nm):
        super().__init__(nm)
        self.instances = []
        self.bbox = None

    def updateBbox( self):
        self.bbox = Rect(None,None,None,None)
        for inst in self.instances:
            r = inst.transformation.hitRect( inst.template.bbox).canonical()
            if self.bbox.llx is None or self.bbox.llx > r.llx: self.bbox.llx = r.llx
            if self.bbox.lly is None or self.bbox.lly > r.lly: self.bbox.lly = r.lly
            if self.bbox.urx is None or self.bbox.urx < r.urx: self.bbox.urx = r.urx
            if self.bbox.ury is None or self.bbox.ury < r.ury: self.bbox.ury = r.ury


class CellInstance:
    def __init__( self, nm, template, trans):
        self.nm = nm
        self.template = template
        self.transformation = trans

class RasterInstance:
    def __init__( self, r, ci):
        self.r = r
        self.ci = ci
        self.filled = tally.BitVec( r.s, ci.nm + '_filled', r.nx*r.ny)
        self.anchor = tally.BitVec( r.s, ci.nm + '_anchor', r.nx*r.ny)

    def backannotatePlacement( self):
        self.ci.transformation = None
        for x in range(self.r.nx):
            for y in range(self.r.ny):
                if self.anchor.val( self.r.idx( x, y)) is True:
                    self.ci.transformation = Transformation( x, y)

    def semantic( self):
        for x in range(self.r.nx):
            for y in range(self.r.ny):
                anchor = self.anchor.var( self.r.idx( x, y))
                bbox = self.ci.template.bbox
                for xx in range( bbox.llx, bbox.urx):
                    for yy in range( bbox.lly, bbox.ury):
                        if x + xx < self.r.nx and y + yy < self.r.ny:
                            self.r.s.emit_implies( anchor, self.filled.var( self.r.idx( x+xx, y+yy)))
                        else:
                            self.r.s.emit_never( anchor)

        self.r.s.emit_exactly_one( [self.anchor.var( i) for i in range( self.r.nx*self.r.ny)])


class Raster:
    def __init__( self, s, template, nx, ny):
        self.s = s    
        self.template = template
        self.ris = []
        self.nx = nx
        self.ny = ny
        self.bv = tally.BitVec( s, template.nm, nx*ny)

    def idx( self, x, y):
        return x*self.ny + y

    def semantic( self):
        for inst in self.template.instances:
            print( 'Instance Name:', inst.nm)
            self.ris.append( RasterInstance( self, inst))
            for ri in self.ris:
                ri.semantic()

        for x in range(self.nx):
            for y in range(self.ny):
                master = self.bv.var( self.idx( x, y))
                for ri in self.ris:
                    filled = ri.filled.var( self.idx( x, y))
                    self.s.emit_implies( filled, master)
                self.s.emit_at_most_one( [ri.filled.var( self.idx( x, y)) for ri in self.ris])

        self.s.solve()
        assert self.s.state == 'SAT'

        for ri in self.ris:
            ri.backannotatePlacement()

        for ri in self.ris:
            self.print_rasters( ri.anchor)
            self.print_rasters( ri.filled)

        self.print_rasters( self.bv)


    def print_rasters( self, bv):
        print( bv)
        for y in range(self.ny-1,-1,-1): 
            print( ''.join( [ ('1' if bv.val(self.idx(x,y)) else '0') for x in range(self.nx)]))


def test_build_raster():
    s = tally.Tally()
    raster = Raster( s, 'xy', 4, 10)

    s.solve()
    assert s.state == 'SAT'

def test_simple_hier():

    l = CellLeaf( "ndev")
    h = CellHier( "npair")

    h.instances.append( CellInstance( 'u0', l, Transformation(0,0)))
    h.instances.append( CellInstance( 'u1', l, Transformation(1,0)))

    h.updateBbox()
        
    with open( "mydesign_dr_globalrouting.json", "wt") as fp:
        tech = Tech()
        h.write_globalrouting_json( fp, tech)

def test_grid_hier():

    l = CellLeaf( "ndev")

    b0 = CellHier( "block0")
    b0.instances.append( CellInstance( 'u0', l, Transformation(0,0)))
    b0.instances.append( CellInstance( 'u1', l, Transformation(4,2,-1,-1)))
    b0.updateBbox()

    b1 = CellHier( "block1")
    b1.instances.append( CellInstance( 'u0', l, Transformation(0,0)))
    b1.instances.append( CellInstance( 'u1', l, Transformation(2,4,-1,-1)))
    b1.updateBbox()

    g = CellHier( "grid")
    g.instances.append( CellInstance( 'u0', b0, Transformation(0,0)))
    g.instances.append( CellInstance( 'u1', b1, Transformation(4,2)))
    g.instances.append( CellInstance( 'u2', b1, Transformation(6,2)))
    g.updateBbox()

    s = tally.Tally()
    r = Raster( s, g, 4, 6)
    r.semantic()
    g.updateBbox()

    with open( "mydesign_dr_globalrouting.json", "wt") as fp:
        tech = Tech()
        g.write_globalrouting_json( fp, tech)

if __name__ == "__main__":
    test_grid_hier()
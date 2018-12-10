from placer import *

def test_mirrors():

    ux = 4
    uy = 8

    nunit = CellLeaf( "nunit", Rect(0,0,ux,uy))
    nunit.addTerminal( "s1", Rect(0,0,0,uy))
    nunit.addTerminal( "g1", Rect(1,0,1,uy))
    nunit.addTerminal( "d", Rect(2,0,2,uy))
    nunit.addTerminal( "g2", Rect(3,0,3,uy))
    nunit.addTerminal( "s2", Rect(4,0,4,uy))

    mirrors = CellHier( "mirrors")

    configs = [('4',8,'out4'),('2',4,'out2'),('1a',2,'out1a'),('1b',2,'out1b'),('ref',2,'vmirror')]

    for (tag, mult, _) in configs:
        for i in range(mult):
            mirrors.addInstance( CellInstance( "CM_%s_%d" % (tag,i), nunit))

    for (tag, mult, d) in configs:
        for i in range(mult):
            mirrors.connect( "CM_%s_%d" % (tag,i), 's1', 'gnd!')
            mirrors.connect( "CM_%s_%d" % (tag,i), 'g1', 'vmirror')
            mirrors.connect( "CM_%s_%d" % (tag,i), 'd',  d)
            mirrors.connect( "CM_%s_%d" % (tag,i), 'g2', 'vmirror')
            mirrors.connect( "CM_%s_%d" % (tag,i), 's2', 'gnd!')

    nx = 2+6*ux
    ny = 4*uy

    mirrors.bbox = Rect( 0, 0, nx, ny)

    s = tally.Tally()
    r = Raster( s, mirrors, nx, ny)
    r.semantic()

    #put a raft on the left and right
    for x in [0,nx-1]:
      for y in range(ny):
        for ri in r.ris:
          s.emit_never( ri.filled.var( r.idx( x, y)))


#
# Assign common centroid placement
#
    places = [('4',1,3),('4',2,3),('4',3,3),('4',4,3),('2',1,2),('ref',2,2),('1a',3,2),('1b',4,2),('2',5,2)]
    places_common_centroid = [ (tag,5-x,3-y) for (tag,x,y) in places]

    od = OrderedDict()
    for (tag,x,y) in places + places_common_centroid:
        if tag not in od: od[tag] = []
        od[tag].append( (tag,x,y))

    ri_tbl = { ri.ci.nm: ri for ri in r.ris}
    for (tag,v) in od.items():
        for (idx,(tag,x,y)) in enumerate(v):
            s.emit_always( ri_tbl["CM_%s_%i" % (tag,idx)].anchor.var( r.idx( 1+x*ux, y*uy)))


    for x in range(nx):
      for y in range(ny):
        for ri in r.ris:
          if y % uy != 0:
            s.emit_never( ri.anchor.var( r.idx( x,y)))
            s.emit_never( ri.anchorMX.var( r.idx( x,y)))
            s.emit_never( ri.anchorMY.var( r.idx( x,y)))
            s.emit_never( ri.anchorMXY.var( r.idx( x,y)))
          else:
            s.emit_never( ri.anchorMX.var( r.idx( x,y)))
            s.emit_never( ri.anchorMXY.var( r.idx( x,y)))

    s.solve()
    assert s.state == 'SAT'

    specified_nets = set()
    remaining_nets = [ n for n in r.nets.keys() if n not in specified_nets]

    def chunk( it, size):
      it = iter(it)
      return iter( lambda: tuple(itertools.islice(it, size)), ())

    groups = [ list(tup) for tup in chunk( remaining_nets, 6)]

    r.optimizeNets( groups)

    with open( "mydesign_dr_globalrouting.json", "wt") as fp:
        tech = Tech()
        mirrors.write_globalrouting_json( fp, tech)

    with open( "mirrors_placer_out.json", "wt") as fp:
        tech = Tech()
        mirrors.dumpJson( fp, tech)


def test_diffpairs():

    ux = 4
    uy = 8

    nunit = CellLeaf( "nunit", Rect(0,0,ux,uy))
    nunit.addTerminal( "s1", Rect(0,0,0,uy))
    nunit.addTerminal( "g1", Rect(1,0,1,uy))
    nunit.addTerminal( "d", Rect(2,0,2,uy))
    nunit.addTerminal( "g2", Rect(3,0,3,uy))
    nunit.addTerminal( "s2", Rect(4,0,4,uy))

    dp = CellHier( "dp")

    configs = [('a',2,'outa','ina','so'),('b',2,'outb','inb','so'),('s',2,'si','c','so')]

    for (tag, mult, d, g, s) in configs:
        for i in range(mult):
            dp.addInstance( CellInstance( "DP_%s_%d" % (tag,i), nunit))

    for (tag, mult, d, g, s) in configs:
        for i in range(mult):
            dp.connect( "DP_%s_%d" % (tag,i), 's1', s)
            dp.connect( "DP_%s_%d" % (tag,i), 'g1', g)
            dp.connect( "DP_%s_%d" % (tag,i), 'd',  d)
            dp.connect( "DP_%s_%d" % (tag,i), 'g2', g)
            dp.connect( "DP_%s_%d" % (tag,i), 's2', s)

    nx = 2+4*ux
    ny = 2*uy

    dp.bbox = Rect( 0, 0, nx, ny)

    s = tally.Tally()
    r = Raster( s, dp, nx, ny)
    r.semantic()

    #put a raft on the left and right
    for x in [0,nx-1]:
      for y in range(ny):
        for ri in r.ris:
          s.emit_never( ri.filled.var( r.idx( x, y)))

#
# Assign common centroid placement
#
    places = [('a',1,1),('b',2,1),('s',3,1)]
    places_common_centroid = [ (tag,3-x,1-y) for (tag,x,y) in places]

    od = OrderedDict()
    for (tag,x,y) in places + places_common_centroid:
        if tag not in od: od[tag] = []
        od[tag].append( (tag,x,y))

    ri_tbl = { ri.ci.nm: ri for ri in r.ris}
    for (tag,v) in od.items():
        for (idx,(tag,x,y)) in enumerate(v):
            s.emit_always( ri_tbl["DP_%s_%i" % (tag,idx)].anchor.var( r.idx( 1+x*ux, y*uy)))


    for x in range(nx):
      for y in range(ny):
        for ri in r.ris:
          if y % uy != 0:
            s.emit_never( ri.anchor.var( r.idx( x,y)))
            s.emit_never( ri.anchorMX.var( r.idx( x,y)))
            s.emit_never( ri.anchorMY.var( r.idx( x,y)))
            s.emit_never( ri.anchorMXY.var( r.idx( x,y)))
          else:
            s.emit_never( ri.anchorMX.var( r.idx( x,y)))
            s.emit_never( ri.anchorMXY.var( r.idx( x,y)))

    s.solve()
    assert s.state == 'SAT'

    specified_nets = set()
    remaining_nets = [ n for n in r.nets.keys() if n not in specified_nets]

    def chunk( it, size):
      it = iter(it)
      return iter( lambda: tuple(itertools.islice(it, size)), ())

    groups = [ list(tup) for tup in chunk( remaining_nets, 6)]

    r.optimizeNets( groups)

    with open( "mydesign_dr_globalrouting.json", "wt") as fp:
        tech = Tech()
        dp.write_globalrouting_json( fp, tech)

    with open( "dp_placer_out.json", "wt") as fp:
        tech = Tech()
        dp.dumpJson( fp, tech)

def test_diffpairs2x():

    ux = 4
    uy = 8

    nunit = CellLeaf( "nunit", Rect(0,0,ux,uy))
    nunit.addTerminal( "s1", Rect(0,0,0,uy))
    nunit.addTerminal( "g1", Rect(1,0,1,uy))
    nunit.addTerminal( "d", Rect(2,0,2,uy))
    nunit.addTerminal( "g2", Rect(3,0,3,uy))
    nunit.addTerminal( "s2", Rect(4,0,4,uy))

    dp = CellHier( "dp")

    configs = [('a',4,'outa','ina','so'),('b',4,'outb','inb','so'),('s',4,'si','c','so')]

    for (tag, mult, d, g, s) in configs:
        for i in range(mult):
            dp.addInstance( CellInstance( "DP_%s_%d" % (tag,i), nunit))

    for (tag, mult, d, g, s) in configs:
        for i in range(mult):
            dp.connect( "DP_%s_%d" % (tag,i), 's1', s)
            dp.connect( "DP_%s_%d" % (tag,i), 'g1', g)
            dp.connect( "DP_%s_%d" % (tag,i), 'd',  d)
            dp.connect( "DP_%s_%d" % (tag,i), 'g2', g)
            dp.connect( "DP_%s_%d" % (tag,i), 's2', s)

    nx = 2+4*ux
    ny = 4*uy

    dp.bbox = Rect( 0, 0, nx, ny)

    s = tally.Tally()
    r = Raster( s, dp, nx, ny)
    r.semantic()

    #put a raft on the left and right
    for x in [0,nx-1]:
      for y in range(ny):
        for ri in r.ris:
          s.emit_never( ri.filled.var( r.idx( x, y)))

#
# Assign common centroid placement
#
    places = [          ('a',1,3),('b',2,3),
              ('s',0,2),('a',1,2),('b',2,2),('s',3,2)]
    places_common_centroid = [ (tag,3-x,3-y) for (tag,x,y) in places]

    od = OrderedDict()
    for (tag,x,y) in places + places_common_centroid:
        if tag not in od: od[tag] = []
        od[tag].append( (tag,x,y))

    ri_tbl = { ri.ci.nm: ri for ri in r.ris}
    for (tag,v) in od.items():
        for (idx,(tag,x,y)) in enumerate(v):
            s.emit_always( ri_tbl["DP_%s_%i" % (tag,idx)].anchor.var( r.idx( 1+x*ux, y*uy)))


    for x in range(nx):
      for y in range(ny):
        for ri in r.ris:
          if y % uy != 0:
            s.emit_never( ri.anchor.var( r.idx( x,y)))
            s.emit_never( ri.anchorMX.var( r.idx( x,y)))
            s.emit_never( ri.anchorMY.var( r.idx( x,y)))
            s.emit_never( ri.anchorMXY.var( r.idx( x,y)))
          else:
            s.emit_never( ri.anchorMX.var( r.idx( x,y)))
            s.emit_never( ri.anchorMXY.var( r.idx( x,y)))

    s.solve()
    assert s.state == 'SAT'

    specified_nets = set()
    remaining_nets = [ n for n in r.nets.keys() if n not in specified_nets]

    def chunk( it, size):
      it = iter(it)
      return iter( lambda: tuple(itertools.islice(it, size)), ())

    groups = [ list(tup) for tup in chunk( remaining_nets, 6)]

    r.optimizeNets( groups)

    with open( "mydesign_dr_globalrouting.json", "wt") as fp:
        tech = Tech()
        dp.write_globalrouting_json( fp, tech)

    with open( "dp_placer_out.json", "wt") as fp:
        tech = Tech()
        dp.dumpJson( fp, tech)



def test_diffpairs4x():

    ux = 4
    uy = 8

    nunit = CellLeaf( "nunit", Rect(0,0,ux,uy))
    nunit.addTerminal( "s1", Rect(0,0,0,uy))
    nunit.addTerminal( "g1", Rect(1,0,1,uy))
    nunit.addTerminal( "d", Rect(2,0,2,uy))
    nunit.addTerminal( "g2", Rect(3,0,3,uy))
    nunit.addTerminal( "s2", Rect(4,0,4,uy))

    dp = CellHier( "dp")

    configs = [('a',8,'outa','ina','so'),('b',8,'outb','inb','so'),('s',8,'si','c','so')]

    for (tag, mult, d, g, s) in configs:
        for i in range(mult):
            dp.addInstance( CellInstance( "DP_%s_%d" % (tag,i), nunit))

    for (tag, mult, d, g, s) in configs:
        for i in range(mult):
            dp.connect( "DP_%s_%d" % (tag,i), 's1', s)
            dp.connect( "DP_%s_%d" % (tag,i), 'g1', g)
            dp.connect( "DP_%s_%d" % (tag,i), 'd',  d)
            dp.connect( "DP_%s_%d" % (tag,i), 'g2', g)
            dp.connect( "DP_%s_%d" % (tag,i), 's2', s)

    nx = 2+6*ux
    ny = 4*uy

    dp.bbox = Rect( 0, 0, nx, ny)

    s = tally.Tally()
    r = Raster( s, dp, nx, ny)
    r.semantic()

    #put a raft on the left and right
    for x in [0,nx-1]:
      for y in range(ny):
        for ri in r.ris:
          s.emit_never( ri.filled.var( r.idx( x, y)))

#
# Assign common centroid placement
#
    places = [('s',0,3),('a',1,3),('a',2,3),('b',3,3),('b',4,3),('s',5,3),
              ('s',0,2),('a',1,2),('a',2,2),('b',3,2),('b',4,2),('s',5,2)]
    places_common_centroid = [ (tag,5-x,3-y) for (tag,x,y) in places]

    od = OrderedDict()
    for (tag,x,y) in places + places_common_centroid:
        if tag not in od: od[tag] = []
        od[tag].append( (tag,x,y))

    ri_tbl = { ri.ci.nm: ri for ri in r.ris}
    for (tag,v) in od.items():
        for (idx,(tag,x,y)) in enumerate(v):
            s.emit_always( ri_tbl["DP_%s_%i" % (tag,idx)].anchor.var( r.idx( 1+x*ux, y*uy)))


    for x in range(nx):
      for y in range(ny):
        for ri in r.ris:
          if y % uy != 0:
            s.emit_never( ri.anchor.var( r.idx( x,y)))
            s.emit_never( ri.anchorMX.var( r.idx( x,y)))
            s.emit_never( ri.anchorMY.var( r.idx( x,y)))
            s.emit_never( ri.anchorMXY.var( r.idx( x,y)))
          else:
            s.emit_never( ri.anchorMX.var( r.idx( x,y)))
            s.emit_never( ri.anchorMXY.var( r.idx( x,y)))

    s.solve()
    assert s.state == 'SAT'

    specified_nets = set()
    remaining_nets = [ n for n in r.nets.keys() if n not in specified_nets]

    def chunk( it, size):
      it = iter(it)
      return iter( lambda: tuple(itertools.islice(it, size)), ())

    groups = [ list(tup) for tup in chunk( remaining_nets, 6)]

    r.optimizeNets( groups)

    with open( "mydesign_dr_globalrouting.json", "wt") as fp:
        tech = Tech()
        dp.write_globalrouting_json( fp, tech)

    with open( "dp_placer_out.json", "wt") as fp:
        tech = Tech()
        dp.dumpJson( fp, tech)


def test_vga(optimize=True,raft=True):
    ux = 4
    uy = 8

    mirrors = CellLeaf( "mirrors", Rect(0,0,6*ux,4*uy))
    mirrors.addTerminal( "out4", Rect(0,0,0,uy))
    mirrors.addTerminal( "out2", Rect(1,0,1,uy))
    mirrors.addTerminal( "out1a", Rect(2,0,2,uy))
    mirrors.addTerminal( "out1b", Rect(3,0,3,uy))
    mirrors.addTerminal( "vmirror", Rect(4,0,4,uy))

    dp1 = CellLeaf( "dp1", Rect(0,0,4*ux,2*uy))
    dp1.addTerminal( "outa", Rect(0,0,0,uy))
    dp1.addTerminal( "outb", Rect(1,0,1,uy))
    dp1.addTerminal( "ina", Rect(2,0,2,uy))
    dp1.addTerminal( "inb", Rect(3,0,3,uy))
    dp1.addTerminal( "si", Rect(4,0,4,uy))
    dp1.addTerminal( "c", Rect(5,0,5,uy))

    dp2 = CellLeaf( "dp2", Rect(0,0,4*ux,4*uy))
    dp2.addTerminal( "outa", Rect(0,0,0,uy))
    dp2.addTerminal( "outb", Rect(1,0,1,uy))
    dp2.addTerminal( "ina", Rect(2,0,2,uy))
    dp2.addTerminal( "inb", Rect(3,0,3,uy))
    dp2.addTerminal( "si", Rect(4,0,4,uy))
    dp2.addTerminal( "c", Rect(5,0,5,uy))

    dp4 = CellLeaf( "dp4", Rect(0,0,6*ux,4*uy))
    dp4.addTerminal( "outa", Rect(0,0,0,uy))
    dp4.addTerminal( "outb", Rect(1,0,1,uy))
    dp4.addTerminal( "ina", Rect(2,0,2,uy))
    dp4.addTerminal( "inb", Rect(3,0,3,uy))
    dp4.addTerminal( "si", Rect(4,0,4,uy))
    dp4.addTerminal( "c", Rect(5,0,5,uy))

    vga = CellHier( "vga")

    io = [("outa","outa"),("outb","outb"),("ina","ina"),("inb","inb")]

    vga.addAndConnect( mirrors, "m", [("out4","v4"),("out2","v2"),("out1a","v1a"),("out1b","v1b"),("vmirror","vmirror")])
    vga.addAndConnect( dp1, "dp1a", io + [("si","v1a"),("c","c1a")])
    vga.addAndConnect( dp1, "dp1b", io + [("si","v1b"),("c","c1b")])
    vga.addAndConnect( dp2, "dp2",  io + [("si","v2"),("c","c2")])
    vga.addAndConnect( dp4, "dp4",  io + [("si","v4"),("c","c4")])

    assert not raft

    nx = 6*ux
    ny = 16*uy
#    nx = (2*5)*ux
#    ny = 8*uy
#    nx = 2+(2*4+2*6)*ux+6
#    ny = 4*uy

    vga.bbox = Rect( 0, 0, nx, ny)

    s = tally.Tally()
    r = Raster( s, vga, nx, ny)
    r.semantic()

    if raft:
      #put a raft on the left and right
      for x in [0,nx-1]:
        for y in range(ny):
          for ri in r.ris:
            s.emit_never( ri.filled.var( r.idx( x, y)))

    for x in range(nx):
      for y in range(ny):
        for ri in r.ris:
          if y % uy != 0:
            s.emit_never( ri.anchor.var( r.idx( x,y)))
            s.emit_never( ri.anchorMX.var( r.idx( x,y)))
            s.emit_never( ri.anchorMY.var( r.idx( x,y)))
            s.emit_never( ri.anchorMXY.var( r.idx( x,y)))
          else:
            s.emit_never( ri.anchorMX.var( r.idx( x,y)))
            s.emit_never( ri.anchorMXY.var( r.idx( x,y)))

    s.solve()
    assert s.state == 'SAT'

    drv_nets = ["v1a","v1b","v2", "v4"]
    out_nets = ["outa","outb"]
    in_nets  = ["ina","inb"]
    ctrl_nets = ["c1a","c1b","c2", "c4"]

    specified_nets = set(out_nets + in_nets + drv_nets + ctrl_nets)
    remaining_nets = [ n for n in r.nets.keys() if n not in specified_nets]

    def chunk( it, size):
      it = iter(it)
      return iter( lambda: tuple(itertools.islice(it, size)), ())

    groups = [drv_nets,out_nets,in_nets,ctrl_nets] + [ list(tup) for tup in chunk( remaining_nets, 6)]

    print("Groups:", groups)

    if optimize:
        r.optimizeNets( groups)
    else:
        r.solve()

    with open( "mydesign_dr_globalrouting.json", "wt") as fp:
        tech = Tech()
        vga.write_globalrouting_json( fp, tech)

    with open( "vga_placer_out.json", "wt") as fp:
        tech = Tech()
        vga.dumpJson( fp, tech)


import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser( description="Placer equalizer")
    parser.add_argument( "-n", "--block_name", type=str, required=True)
    parser.add_argument( "-noopt", "--no_optimize", action='store_true')
    parser.add_argument( "-noraft", "--no_raft", action='store_true')

    args = parser.parse_args()

    if args.block_name == "vga":
        test_vga( not args.no_optimize, raft=not args.no_raft)
    elif args.block_name == "mirrors":
        test_mirrors()
    elif args.block_name == "diffpairs":
        test_diffpairs()
    elif args.block_name == "diffpairs2x":
        test_diffpairs2x()
    elif args.block_name == "diffpairs4x":
        test_diffpairs4x()
    else:
        assert(False)

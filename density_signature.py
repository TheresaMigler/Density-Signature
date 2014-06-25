import random
import bisect
import numpy


from igraph import *   

#This function takes an input graph and returns a path with an egalitarian orientation.
def PathReversal(ingraph):
    # arbritrarily orient if not directed:
    G = ingraph.copy()
    if not(G.is_directed()): G.to_directed(False)

    n = G.vcount()
    print(n)
    vertices = set(range(n))
    indegree = lambda v: G.degree(v,IN)

    nopathsreversed = True

    while n > 0:
        foundapath = False

        # find a vertex of max indegree that is unboxed
        vmax = max(vertices,key=indegree)
        k = indegree(vmax)

        # try to find a reversible path
        BFS = G.bfsiter(vmax,IN) # BFS tree from root
        for ver in BFS: # iterate by BFS order
            v = ver.index
            if (v in vertices and indegree(v) < (k-1)):
                nopathsreversed = False
                # get the path from vstart to root
                path = G.get_shortest_paths(v, vmax, None, OUT, output="vpath")[0]
                
                # reverse this path 
                pathedges = G.get_eids([],path)
                for e in pathedges:
                    G.add_edge(G.es[e].target,G.es[e].source)
                G.delete_edges(pathedges)

                # a path has been reversed
                foundapath = True
                break

        # no path has been found
        if not(foundapath):
            BFS = G.bfsiter(vmax,IN)
            # add to box
            for ver in BFS:
                v = ver.index
                if v in vertices:
                    G.vs[v]["box"] = k
                    vertices.remove(v)
                    n = n-1
                    # print n

    if nopathsreversed: print("No paths reversed")
    
    return G


#This function returns an array. The first entry in this array is the density signature.

def DensityDecomposition(ingraph):
    # assumes ingraph vertices have attribute "box"
    # and has a path-reversal orientation
    
    if not(ingraph.is_directed()): 
        print("Graph is NOT directed")
        return False
    print("Graph is directed")

    if not("box" in set(ingraph.vs.attributes())): 
        print("Graph is NOT boxed")
        return False
    print("Graph is boxed")

    # ease-making
    n = ingraph.vcount()
    vertices = range(n)
    indegree = lambda v: ingraph.degree(v,IN)
    box = lambda v: int(ingraph.vs[v]["box"])

    # check that box and vertex indegrees match up
    for v in vertices:
        if not(indegree(v) == box(v)) and not(indegree(v) == box(v)-1):
            print("Vertex "+str(v)+" is boxed incorrectly.  "+str(v)+" has indegree "+str(indegree(v))+" but is in box "+str(box(v)))
            return False
    print("Vertex degrees match box numbers")

    # sort vertices by box
    vertices.sort(key=box,reverse=True)

    # build boxes
    k = box(vertices[0])
    box_vcounts = [0]*(k+1)
    box_vertices = [[]]*(k+1)
    for v in vertices:
        if box(v) == k:
            # add to box
            box_vcounts[k] = box_vcounts[k]+1
            box_vertices[k] = box_vertices[k]+[v]
        else:
            # new box
            k = box(v)
            box_vcounts[k] = 1
            box_vertices[k] = [v]

    k = box(vertices[0])
    box_ecounts = [[0]*(k+1) for x in xrange(k+1)]
    for i in range(k+1):
        gk = ingraph.induced_subgraph(box_vertices[i])
        box_ecounts[i][i] = gk.ecount()
    for i in range(k+1):
        for j in range(i+1,k+1):
            gk = ingraph.induced_subgraph(box_vertices[i]+box_vertices[j])
            box_ecounts[i][j] = gk.ecount()-box_ecounts[i][i]-box_ecounts[j][j]
    
    return (box_vcounts, box_ecounts, box_vertices)

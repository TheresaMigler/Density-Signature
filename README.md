Density-Signature
=================

Here you will find the code required to path-reverse a graph to find its density decomposition and density decomposition. Also you will find the code required to generate random graphs using the density decomposition.

Contact: tmigler@gmail.com

Information about the algorithms can be found here: http://arxiv.org/abs/1405.1001

## What is included:
The code  is written in Python, using the igraph library. 
density_signature.py includes the functions to find the density decomposition and density distribution. models.py includes the functions to generate random graphs using the density distribution.
Input graphs should be in .gml format. I have included two .gml files. One is an undirected social network of frequent associations between 62 dolphins in a community living off Doubtful Sound, New Zealand. The other is a network of coauthorships between scientists posting preprints on the Condensed Matter E-Print Archive between Jan 1, 1995 and December 31, 1999. These networks are made available by Mark Newman here: http://www-personal.umich.edu/~mejn/netdata/


## Usage:
Here is an example involving the coauthorship network.

\>\>\> graph = Graph.Read_GML("/Desktop/phys.gml")

\>\>\> hgraph = PathReversal(graph)            

16726

\>\>\> boxes = DensityDecomposition(hgraph)

Graph is directed

Graph is boxed

Vertex degrees match box numbers

\>\>\> boxes[0]

[462, 2869, 3832, 3568, 2499, 1589, 1018, 362, 221, 278, 28]

\>\>\> modelgraph = RDDmodel(boxes[0])

(28, 10)

(278, 9)

(221, 8)

(362, 7)

(1018, 6)

(1589, 5)

(2499, 4)

(3568, 3)

(3832, 2)

(2869, 1)

16726

No paths reversed

\>\>\> modelgraph2 = HSWmodel(boxes[0],.5)

(278, 9)

(221, 8)

(362, 7)

(1018, 6)

(1589, 5)

(2499, 4)

(3568, 3)

(3832, 2)

(2869, 1)

>>> 

For reference, the PathReversal took 6 minutes and the RDDmodel took 4.

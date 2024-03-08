# TSPLIP visualized

Well, turns out this already exists way better, use this instead: https://pypi.org/project/tsplib95/

I used TSPLIBs examples to benchmark some heuristics.
Since i use NetworkX to visualize the node trees, i wrote some python code that reads the provided .tsp and .tour files from TSPLIB and converts them to be easily usable for NetworkX.

The script contains functions to:
- Parse a .tsp file to a custom .edges file, which contains a NetworkX-style [Node1 Node2 Weight] list
- Calculate the geo-distance as specified in TSPLIB
- Calculate the att(pseudo-euclidian)-distance
- Parse a .tour file and extract the optimal tour as a list
- Draw a node-tree with a custom path
- Calculate the length of a path
- Close an incomplete path by joining the ends together

There are some distance calculation methods in TSPLIB taht i didnt implement yet. Maybe later...

Thanks to: http://comopt.ifi.uni-heidelberg.de/software/TSPLIB95/tsp/
Which is awesome!

Maybe this helps someone!  

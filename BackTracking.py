# def coloring(solution,lcolor,i,lnodes):
#     if i == len(lnodes):
#         solution.append([node.color for node in lnodes])
#         return
#         # fillColor(node[0],lcolor)
#     node = lnodes[i]
#     for color in lcolor:
#         if(node.isSafe(color)):
#             node.color = color
#             coloring(solution,lcolor,i+1,lnodes)
#             node.color = "" #for backtracking
import copy


# def coloringWithCanonicalOrder(solution,solsorted_set,lcolor,i,lnodes):
#     if i == len(lnodes):
#         sol = [node.color for node in lnodes]
#         sortedsol = set(sorted(sol))
#         # res =
#
#         if sortedsol not in solsorted_set:
#             solution.append(sol)
#             # print(sol)
#             solsorted_set.append(sortedsol)
#         return
#     if len(solution) >= 10000:
#         return
#         # fillColor(node[0],lcolor)
#     node = lnodes[i]
#     for cid, color in enumerate(lcolor):
#         if(node.isSafeCanonical(cid)):
#             node.color = cid
#             coloringWithCanonicalOrder(solution,solsorted_set,lcolor,i+1,lnodes)
#             node.color = -1 #for backtracking

def coloringWithCanonicalOrder(solution, solsorted_set, lcolor, i, lnodes):
    if i == len(lnodes):
        sol = [node.color for node in lnodes]
        sortedsol = tuple(sorted(sol))  # keeps duplicates, order-independent

        if sortedsol not in solsorted_set:
            solution.append(sol)
            solsorted_set.add(sortedsol)  # fast O(1) lookup
        return

    if len(solution) >= 10000:
        return

    node = lnodes[i]
    for cid, color in enumerate(lcolor):
        if node.isSafeCanonical(cid):
            node.color = cid
            coloringWithCanonicalOrder(solution, solsorted_set, lcolor, i+1, lnodes)
            node.color = -1  # backtrack

def getSolutions(lnodes,lcolor):
    Solutions = list()
    solsorted_set = set()
    nodes = copy.deepcopy(lnodes)
    # for c in lcolor:
        # nodes[0].color = c
        # solution = list()
    coloringWithCanonicalOrder(solution=Solutions,solsorted_set= solsorted_set,lcolor=lcolor, lnodes=nodes, i=0)
        # Solutions.append((c,solution))
    return Solutions




def loadData():
    serpDatLst = []
    f = open('serp_input.csv')
    serpHdrLst = f.readline().strip().split(',')
    for line in f:
        serpDatLine = line.strip().split(',')
        serpDatLst.append([int(x) for x in serpDatLine] )
    f.close
    #return serpHdrLst, serpDatLst[0:11]  # return only first few ... for debug.
    return serpHdrLst, serpDatLst       # return all for non-debug.
#############################################################################

def rangeData(serpHdrLst, serpDatLst):
    minMaxLst = []
    for hIdx,hdr in enumerate(serpHdrLst):
        valLst = []
        for vals in serpDatLst:
            valLst.append(vals[hIdx])
        minVal = min(valLst)
        maxVal = max(valLst)
        minMaxLst.append((minVal, maxVal))
    return minMaxLst
#############################################################################

def genSerpSearchCriteriaLst(minMaxLst):
    import math

    diffs       = [b-a+1 for a,b in minMaxLst]
    numToGen    = math.prod(diffs)
    should      = ['inc'] * len(minMaxLst)
    currVals    = [x[0] for x in minMaxLst]
    serpSrchLst = []

    while len(serpSrchLst) < numToGen:

        serpSrchLst.append(currVals[:]) # <-- the ':' fixed a bug.

        for idx in range(len(currVals)-1, -1, -1):
            if should[idx] == 'inc':
                currVals[idx] += 1
                if currVals[idx]  > minMaxLst[idx][1]:
                    currVals[idx] = minMaxLst[idx][1]
                    should[idx] = 'dec'
                    continue

            if should[idx] == 'dec':
                currVals[idx] -= 1
                if currVals[idx]  < minMaxLst[idx][0]:
                    currVals[idx] = minMaxLst[idx][0]
                    should[idx] = 'inc'
                    continue

            break

    return serpSrchLst
#############################################################################

def genSerpSortedDataLst(serpSearchCriteriaLst, serpDataLst):
    serpSortedDataLst = []
    for critera in serpSearchCriteriaLst:
        for data in serpDataLst:
            if data == critera:
                serpSortedDataLst.append(data)
    return serpSortedDataLst
#############################################################################

def writeSerpToFile(serpHdr, serpDatLst):
    with open('serp_output.txt', 'w') as f:
        for val in serpHdr:
            f.write('{} '.format(val))
        f.write('\n')
        for vals in serpDatLst:
            for val in vals:
                f.write('{:2} '.format(val))
            f.write('\n')
    return
#############################################################################

if __name__ == '__main__':
    import pprint as pp

    serpHdr, serpDatLst = loadData()
    minMaxLst = rangeData(serpHdr, serpDatLst)
    serpSearchCriteriaLst = genSerpSearchCriteriaLst(minMaxLst)
    serpSortedDatLst = genSerpSortedDataLst(serpSearchCriteriaLst, serpDatLst)
    writeSerpToFile(serpHdr, serpSortedDatLst)

    #debug = True
    debug = False
    if debug:
        thingsToPprint = [serpDatLst, serpSortedDatLst]
        #thingsToPprint = [serpSearchCriteriaLst, serpDatLst, serpSortedDatLst]
        for x in thingsToPprint:
            print()
            pp.pprint(x)
            print()
        print(len(serpDatLst), len(serpSortedDatLst))

def loadData():
    serpInput = []
    f = open('serp_input.csv')
    serpHeader = f.readline().strip().split(',')
    for line in f:
        serpInputLine = line.strip().split(',')
        serpInput.append([int(x) for x in serpInputLine] )
    f.close
    return serpHeader, serpInput[0:3]
    #return serpHeader, serpInput
#############################################################################

def rangeData(serpHeader,  serpInput):
    import pprint as pp
    minMaxLst = []
    for hIdx,hdr in enumerate(serpHeader):
        valLst = []
        for vals in serpInput:
            valLst.append(vals[hIdx])
        minVal = min(valLst)
        maxVal = max(valLst)
        minMaxLst.append((minVal, maxVal))
    return minMaxLst
#############################################################################

def genSerpSearchCriteriaLst( minMaxLst ):
    import math
    
    diffs       = [b-a+1 for a,b in minMaxLst]
    numToGen    = math.prod(diffs)
    should      = [ 'inc' ] * len(minMaxLst)
    currVals    = [ x[0] for x in minMaxLst ]
    serpSrchLst = []
    
    while len(serpSrchLst) < numToGen:

        serpSrchLst.append(currVals[:])

        for idx in range( len(currVals)-1, -1, -1 ):
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

def genSerpSortedDataLst( serpSearchCriteriaLst, serpData ):
    serpSortedDataLst = []
    return serpSortedDataLst
#############################################################################    

if __name__ == '__main__':
    import pprint as pp

    serpHeader, serpData = loadData()
    minMaxLst = rangeData(serpHeader, serpData)

    serpSearchCriteriaLst = genSerpSearchCriteriaLst(minMaxLst)
    serpSortedDataLst = genSerpSortedDataLst(serpSearchCriteriaLst, serpData)

    print()
    pp.pprint(serpSearchCriteriaLst)
    print()
    
# A fast and memory efficient implementation
# by Hjelmqvist, Sten
def fastMemLev(s, t):
    # degenerate cases
    if s == t:
        return 0
    if len(s) == 0:
        return len(t)
    if len(t) == 0:
        return len(s)
  
    # create two work vectors of integer distances
    #int[] v0 = new int[t.Length + 1];
    #int[] v1 = new int[t.Length + 1];
    v0 = []
    v1 = []
  
    # initialize v0 (the previous row of distances)
    # this row is A[0][i]: edit distance for an empty s
    # the distance is just the number of characters to delete from t
    # for (int i = 0; i < v0.Length; i++)
    # v0[i] = i;
    for i in range(len(t)+1):
        v0.append(i)
        v1.append(0)
 
    for i in range(len(s)): 
        # calculate v1 (current row distances) from the previous row v0
        # first element of v1 is A[i+1][0]
        # edit distance is delete (i+1) chars from s to match empty t
        v1[0] = i + 1
  
        # use formula to fill in the rest of the row
        for j in range(len(t)):
            cost = 0 if s[i] == t[j] else 1;
            v1[j + 1] = min(v1[j]+1, v0[j+1]+1, v0[j]+cost)
  
        # copy v1 (current row) to v0 (previous row) for next iteration
        for j in range(len(t)+1):
            v0[j] = v1[j]
  
    return v1[len(t)]
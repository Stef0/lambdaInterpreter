from lambdaClass import parser


def substitute(lam, x, M, dic):
    
    '''
    lam is from the class Node
    x is the variable name to be substituted with node M,
    dic is the dictionary of named lambda terms
    
    '''
      
    if lam.data == '%':
        substitute(lam.child2, x, M, dic)
        
    elif lam.data == '@':
        substitute(lam.child1, x, M, dic)
        substitute(lam.child2, x, M, dic)        
       
    elif lam.data == x:
        lam.data = M.data
        lam.child1 = M.child1
        lam.child2 = M.child2
        
# =============================================================================
#     elif lam.data.isupper(): #is this necessary?
# 
#         extend(lam, dic)
#         substitute(lam, x, M, dic)
# =============================================================================
        
    else:
        return
    
    
    
            
def extend(lam, dic):
    '''
    lam is a named lambda term and dic is a dictionary of terms, 
    lam is substituted by it's term found in the dictionary
    '''

    
    
    if not lam.data.isupper():
        raise Exception("WTF you should extend terms")
    elif not lam.data in dic:
        raise Exception("WTF the term that you are trying to extend is not in dic")
    else:
        
        name = lam.data
        freshVar(dic[lam.data], name)
        
        name = dic[lam.data].data
        c1 = dic[lam.data].child1   
        c2 = dic[lam.data].child2         
        lam.data = name
        lam.child1 = c1
        lam.child2 = c2

def freshVar(lam, name):
    '''
    lam is a lambda term, we want to make fresh variables for it. we append name to all its variables
    this is inefficient as fuck
    '''

    if lam.data.islower():
        lam.data = lam.data + name
    
    if lam.child1 == None:
        return
    else: 
        freshVar(lam.child1,name)
    
    if lam.child2 == None:
        return
    else: 
        freshVar(lam.child2,name)    

        
    
def betaOpHead(lam, dic):
    
    '''
    lam is a named lambda term and dic is a dictionary of terms
    this function implements one step of Normal-order reduction: 
    the strategy in which one applies the rule for beta reduction 
    in head position
    '''
    if lam.data == '%' : 
        lam.betanormal = True
        return lam
    elif lam.data == '@' :
        if lam.child1.data == '%':
            
            lam1 = lam.child1.child2
            substitute(lam1, lam.child1.child1.data, lam.child2, dic)
            
            return lam1
        else:
            # recursive case? application of type (A B) (C D)
            return lam
    else:
        lam.betanormal = True
        return lam
    
    
def betaHeadRec(lam, dic, limit = 100):
    a = lam
    while (not a.betanormal) and limit>0:
        a = betaOpHead(a,dic)
        limit = limit - 1
    
    if lam.betanormal == True:
        return a
    if limit == 0:
        return "limit of applications reached"
        


    
A = parser('(%x.((x y) (%x.(%z.(z x)))))')        
B = parser('((%x.(x x)) (%x.y))')

T = parser('(%x.(x x))')
Z = parser('(%x.x)')

dic = {}
dic['A'] = A
dic['B'] = B

C = parser('B')

substitute(T, 'x', Z, dic)

B = betaOpHead(B, dic)    
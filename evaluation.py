from lambdaClass import parser, Node

import time


    
def CASub(term, var, sTerm): 
    '''
    capture avoiding substitution of sTerm for var in term
    '''
    if term.data == var.data:
        term.data = sTerm.data
        term.l = sTerm.l
        term.r = sTerm.r
        
    elif term.data == '@':
        CASub(term.l, var, sTerm)
        CASub(term.r, var, sTerm) 
        
    elif term.data =='%' and term.l != var:
        
        sTerm.getVar()
        if term.l.data in sTerm.freshVar:
            freshify(term, term.l, sTerm.freshVar)
        
        CASub(term.r, var, sTerm) 
        
        
        
    elif term.data =='%' and term.l == var:
        return
    

    
def freshify(term, var, badSet): 
    '''
    in term, make the var fresh, with a new var that is not in badSet
    ''' 
    new = var.data
    while new in badSet:
        new +='1'
    
    term.alphaConv(var.data,new)    

            
def extend(lam, dic):
    
    '''
    lam is a named lambda term and dic is a dictionary of terms, 
    lam is substituted by its term found in the dictionary
    '''
   
    if not lam.data.isupper():
        raise Exception("WTF you should extend terms")
    elif not lam.data in dic:
        raise Exception("WTF the term that you are trying to extend is not in dic")
    else:
                
        name = dic[lam.data].data
        left = dic[lam.data].l.show()
        right = dic[lam.data].r.show()
        c1 = parser(left)   
        c2 = parser(right)      
        lam.data = name
        lam.l = c1
        lam.r = c2
        
    
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

        if lam.l.data == '%':
            var = lam.l.l
            term = lam.l.r  
            CASub(term, var, lam.r)

            return term
        
        elif lam.l.data.islower():
            return lam
        
        elif lam.l.data.isupper():
            extend(lam.l, dic)
            lam = betaOpHead(lam, dic)
            return lam
        
        else:
            lam1 = betaOpHead(lam.l, dic)
            lam.l = lam1
            return lam# recursive case? application of type (A B) (C D)
            
    else:
        lam.betanormal = True
        return lam
    
    
def betaHeadRec(lam, dic, limit = 100, func = betaOpHead):
    
    initialLimit = limit
    
    while (not lam.betanormal) or limit>0:
        lam = func(lam,dic)
        limit = limit - 1
    
    if lam.betanormal == True:
        return lam
    if limit == 0:
        lam.limit = initialLimit
        print("limit of applications reached")
        
        return lam
     
def betaRecMemo(lam, dic, memo = {}, limit = 100, func = betaOpHead):
    
    initialLimit = limit
    lam1 = parser(lam.show())
    track = set()
    
    while (not lam1.betanormal) and limit>0:
        a = lam1.show()
        if a in memo:
            lam1 = memo[a]
            lam1.betanormal = True
            break
        lam1 = func(lam1,dic)
        track.add(a)
        limit = limit - 1
    
    if lam1.betanormal == True:
        memo[lam.show()] = lam1
        for i in track:
            memo[i] = lam1
        return lam1
    if limit == 0:
        lam1.limit = initialLimit
        print("limit of applications reached")
        
        return lam1
    
    
def apply(func1, func2, name = 'temp'):
    ''' given two strings of 2 lambda terms, returns their application '''
    a = Node('@')
    a.l = Node(func1)
    a.r = Node(func2)
    return a

def putInDic(func, name, dic):
    '''
    puts the term func in the dictionary dic, with name
    '''
    dic[name] = func
    func.name = name
        
    
A = parser('(%x.((x y) (%x.(%z.(z x)))))')        
B = parser('((%x.(x x)) (%x.y))')

ID = parser('(%x.x)')
DUB = parser('(%x.(x x))')
X = parser('(%x.y)')
C = parser('((DUB ID) (%x.f))')
TRUE  = parser('(%x.(%y.x))')
FALSE = parser('(%x.(%y.y))')
OR  = parser('(%x.(%y.((x TRUE) y)))')
AND = parser('(%x.(%y.((x y) FALSE)))')
NOT = parser('(%x.((x FALSE) TRUE))')


test = parser('((OR TRUE) FALSE)')
test1 = parser('((OR FALSE) FALSE)')
test2 = parser('((OR TRUE) TRUE)')
test3 = parser('((OR FALSE) TRUE)')

test4 = parser('((AND TRUE) FALSE)')
test5 = parser('((AND FALSE) FALSE)')
test6 = parser('((AND TRUE) TRUE)')
test7 = parser('((AND FALSE) TRUE)')

test8 = parser('(NOT TRUE)')
test9 = parser('(NOT FALSE)')

dic = {}

dic['A'] = A
dic['B'] = B
dic['X'] = X
dic['DUB'] = DUB
dic['ID'] = ID
dic['TRUE'] = TRUE
dic['FALSE'] = FALSE
dic['OR'] = OR
dic['AND'] = AND
dic['NOT'] = NOT

memo = {}

betaRecMemo(test8, dic, memo).show()


#TODO in betaOpHead, understand why there is a bug while calling:
betaOpHead(test, dic)  
#but not
test = betaOpHead(test, dic) 


#test for capture avoid substitution:
a = parser('(%x.y)')
y = parser('y')
x = parser('x')
CASub(a, y, x)
    

#betaHeadRec(test,dic)

#CASub(T, parser('x'), Z)

# B = betaOpHead(B, dic)    
# C1 = betaOpHead(C, dic)  
# C = betaHeadRec(C,dic)
betaOpHead(test, dic)


# start = time.time()
# for i in range(100):
#     TRUE  = parser('(%x.(%y.x))')
#     FALSE = parser('(%x.(%y.y))')
#     OR  = parser('(%x.(%y.((x TRUE) y)))')
#     dic = {}
#     dic['TRUE'] = TRUE
#     dic['FALSE'] = FALSE
#     dic['OR'] = OR
#     test = parser('((OR TRUE) FALSE)')
#     #test = betaHeadRec1(test, dic)
# end = time.time()
# time1 = ((end - start)/100)
# print((end - start)/100)

# start = time.time()
# for i in range(100):
#     TRUE  = parser('(%x.(%y.x))')
#     FALSE = parser('(%x.(%y.y))')
#     OR  = parser('(%x.(%y.((x TRUE) y)))')
#     dic = {}
#     dic['TRUE'] = TRUE
#     dic['FALSE'] = FALSE
#     dic['OR'] = OR
#     test = apply (apply(OR, TRUE), FALSE)
#     test = betaHeadRec(test, dic)
# end = time.time()
# time2 = ((end - start)/100)
# print((end - start)/100)

# print(time2 - time1)


# start = time.time()
# for i in range(100):
#     #test = parser('((OR TRUE) FALSE)')
#     memo = {}
#     betaRecMemo(test, dic, memo)
# end = time.time()
# time2 = ((end - start)/100)
# print((end - start)/100)

# start = time.time()
# memo = {}
# for i in range(100):
#     #test = parser('((OR TRUE) FALSE)')
#     throw = {}
#     betaRecMemo(test, dic, memo)
# end = time.time()
# time2 = ((end - start)/100)
# print((end - start)/100)



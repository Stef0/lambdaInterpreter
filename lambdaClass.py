'''
grammar:
    
variables are in lowercase
Terms start in uppercase

the grammar for a term is:
    
    named term M
    
    variable x
    
    (λ x . M) 	Abstraction 	    Function definition (M is a lambda term). 
                                    The variable x becomes bound in the expression.
                                    
    (M N) 	    Application 	    Applying a function to an argument. M and N are lambda terms. 
    
    
    The reduction operations include:
        
        Operation 	                Name 	        Description
        
        (λx.M[x]) → (λy.M[y]) 	    α-conversion 	Renaming the bound variables in the expression. Used to avoid name collisions.
        
        ((λx.M) E) → (M[x := E]) 	β-reduction 	Replacing the bound variables with the argument expression in the body of the abstraction. 

'''



class lambd :
    def __init__(self, Ninputs, Noutputs, shape, signature = []):
        
        self.Ninputs = Ninputs
        self.Noutputs = Noutputs
        self.Bnormal = "Don't know if normal"
    #def betanormal(self):
        #returns a boolean or text "don't know if normal" if the lambd is in betanormal form
        #return self.Bnormal


class Node(object):
    def __init__(self, data, depth = 0):
        
        self.depth = depth
        self.data = data
        self.daddy = None
        self.child1 = None
        self.child2 = None

        self.betanormal = None        
  
        
        
    def addChild1(self, obj):
                
        self.child1 = obj
      
    def addChild2(self, obj):
                
        self.child2 = obj
        
    def addDaddy(self, obj):
                
        self.daddy = obj
              
        

def parser2(st):

    '''base case: named term or variable
    recursive step: node with % lambda abstraction or @ application
    '''
    
    pos = st.find('(')
    
    if pos == -1: #only variables and terms
        return Node(st)
    
    else:
        
        stack = []
        
        for num,ch in enumerate(st):
            if ch == '(':
                stack.append(num)
            elif ch == ')':
                end = stack.pop()
    
            if stack == []:
    
                if st[end+1] == '%':
                    lambd = Node('%')
                    dotPos = st.find('.')
                    childOne = Node(st[end+2:dotPos])
                    lambd.addChild1(childOne)
                    childTwo = parser2(st[dotPos+1:num])
                    lambd.addChild2(childTwo)
                    return lambd
                else:
                    
                    lambd = Node('@')
                    
                    if st[end+1:num].find('(') == -1:
                        end1 = st[end+1:num].find(' ')
                    else:
                        
                        end1 = findApp(st[end+1:num])
                    
                    childOne = parser2(st[1:end1+1])
                    childTwo = parser2(st[end1+2:num])
                    lambd.addChild1(childOne)
                    lambd.addChild2(childTwo)
                    return lambd
            
def findApp(st):
    ''' 
    finds space between first-layer-deep parenthesis
    '''
    
    stack1 = []   
    
    for ind, cha in enumerate(st):
        
        if cha == '(':
            stack1.append(ind)
        elif cha == ')':
            stack1.pop()
        
        if stack1 == []:
            return ind+1
        
        
        

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
        
    elif lam.data.isupper():

        extend(lam, dic)
        substitute(lam, x, M, dic)
        
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
        
    
def betaoperation(lam, dic):
    
    '''
    lam is a named lambda term and dic is a dictionary of terms
    this function implements one step of Normal-order reduction: 
    the strategy in which one applies the rule for beta reduction 
    in head position
    '''
    if lam.data == '%' : 
        return
    elif lam.data == '@' :
        if lam.child1.data == '%':
            
            lam1 = lam.child1.child2
            substitute(lam1, lam.child1.child1.data, lam.child2, dic)
            
            return lam1
        else:
            return
    else:
        lam.betanormal = True
        return 
        
    
    
A = parser2('(%x.((x y) (%x.(%z.(z x)))))')        
B = parser2('((%x.(x x)) (%x.y))')

T = parser2('(%x.(x x))')
Z = parser2('(%x.x)')

dic = {}
dic['A'] = A
dic['B'] = B

C = parser2('B')

substitute(T, 'x', Z, dic)

S = betaoperation(B, dic)

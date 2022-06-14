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

        
  
        
        
    def addChild1(self, obj):
                
        self.child1 = obj
      
    def addChild2(self, obj):
                
        self.child2 = obj
        
    def addDaddy(self, obj):
                
        self.daddy = obj
              
        

def parser2(st):

    '''base case: named term or variable'''
    
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
                    lambd = Node('lambda')
                    dotPos = st.find('.')
                    childOne = Node(st[end+2:dotPos])
                    lambd.addChild1(childOne)
                    childTwo = parser2(st[dotPos+1:num])
                    lambd.addChild2(childTwo)
                    return lambd
                else:
                    
                    
                    
                    lambd = Node('app')
                    
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
    
    stack1 = []   
    
    for ind, cha in enumerate(st):
        
        if cha == '(':
            stack1.append(ind)
        elif cha == ')':
            stack1.pop()
        
        if stack1 == []:
            return ind+1
        
        
        
        
a = parser2('((x y) (x Y))')        

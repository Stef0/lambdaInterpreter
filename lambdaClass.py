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

class Node(object):
    
    def __init__(self, expr):
        

        self.data = expr

        self.l = None
        self.r = None

        self.betanormal = None  
        
        self.limit = None
        
        self.name = None
        
        self.var = set()
        self.freshVar = set()
    
      
    def addL(self, obj):
                
        self.l = obj
        
      
    def addR(self, obj):
                
        self.r = obj
        

    def show(self):
        
        string = []
        
        if self.data == '@':
            string = '('+self.l.show()+' '+self.r.show()+')'
        elif self.data == '%':
            string = '(%'+self.l.show()+'.'+self.r.show()+')'
        else:
            string = self.data
            
        return string
    
    def getVar(self):
        
        if self.var:
            return
        
        bound = []
        
        def recCall(node, var, freshVar, bound):
            
            if node.data.islower():
                var.add(node.data)
                if not(node.data in bound):
                   freshVar.add(node.data)
                return
            
            if node.data.isupper():
                return
            
            if node.data == '%':
                var.add(node.l.data)
                bound += node.l.data
                recCall(node.r, var, freshVar, bound)
            
            if node.data == '@':
                recCall(node.r, var, freshVar, bound)
                recCall(node.l, var, freshVar, bound)
        
        recCall(self, self.var, self.freshVar, bound)
        
    def alphaConv(self, old, new):
        
        if old in self.var:
            self.var.remove(old)
            self.var.add(new)
            
        if old in self.freshVar:
            self.freshVar.remove(old)
            self.freshVar.add(new)
            
        if self.data == old:
            self.data = new
        elif self.data == '@' or self.data == '%':
            self.l.alphaConv(old,new)
            self.r.alphaConv(old,new)
            

        

def findApp(st):
    '''
    Parameters
    ----------
    st : string of a lambda term

    Returns
    -------
    returns the first space between 2 sets of parentheses, or returns -1 if there is no such space
    '''

    
    stack1 = []   
    l = len(st)-1
    
    for ind, cha in enumerate(st):
        
        if cha == '(':
            stack1.append(ind)
        elif cha == ')':
            stack1.pop()
        
        if (len(stack1) <= 1) and ind != l and cha == ' ':
            return ind+1            

    return -1



def parser(st):

    '''base case: named term or variable
    recursive step: node with % lambda abstraction or @ application
    '''
    
    pos = st.find('(')
    
    l = len(st)-1
    
    if pos == -1: #case for variables and named terms
        return Node(st)
    
    else:
        
        space = findApp(st)
        
        if space != -1 :   #application case 
            
            lambd = Node('@')
            childOne = parser(st[1:space-1])
            childTwo = parser(st[space:l])
            lambd.addL(childOne)
            lambd.addR(childTwo)
            return lambd
        
        else:       #lambda case
        
            lambd = Node('%')
            dotPos = st.find('.')
            childOne = Node(st[2:dotPos])
            lambd.addL(childOne)
            childTwo = parser(st[dotPos+1:l])
            lambd.addR(childTwo)
            return lambd            
            


T = parser('(%x.(x x))')
Z = parser('(%x.x)')

parser('(%x.(x x))')

X = parser('(%x.((x y) (%x.(%z.(z x)))))')

A = parser('(%x.((x y) (%x.(%z.((z x) (k x))))))')        
B = parser('((%x.(x x)) (%x.y))')






    
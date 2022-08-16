import time
import evaluation, lambdaClass

IDENTITY = lambda a: a
IF = IDENTITY

# boolean values
TRUE  = lambda a: lambda b: a
FALSE = lambda a: lambda b: b

# base boolean operations
OR  = lambda a: lambda b: a(TRUE)(b)
AND = lambda a: lambda b: a(b)(FALSE)
NOT = lambda a: a(FALSE)(TRUE)

# additional boolean operations
XOR  = lambda a: lambda b: a(b(FALSE)(TRUE))(b(TRUE)(FALSE))
XNOR = lambda a: lambda b: NOT(XOR(a)(b))

# combinators
I = IDENTITY
K = TRUE
S = lambda a: lambda b: lambda c: a(c)(b(c))
Y = lambda f: (
    (lambda x: f(lambda y: x(x)(y)))
    (lambda x: f(lambda y: x(x)(y)))
)


start = time.time()
for i in range(100):
    TRUE  = lambda a: lambda b: a
    FALSE = lambda a: lambda b: b
    OR  = lambda a: lambda b: a(TRUE)(b)
    dic = {}
    dic['TRUE'] = TRUE
    dic['FALSE'] = FALSE
    dic['OR'] = OR    
    test = OR (TRUE) (FALSE)
    test (1) (2)
end = time.time()
print((end - start)/100)

start = time.time()
for i in range(100):
    TRUE  = parser('(%x.(%y.x))')
    FALSE = parser('(%x.(%y.y))')
    OR  = parser('(%x.(%y.((x TRUE) y)))')
    dic = {}
    dic['TRUE'] = TRUE
    dic['FALSE'] = FALSE
    dic['OR'] = OR
    test = apply (apply(OR, TRUE), FALSE)
    test = betaHeadRec(test, dic)
end = time.time()
print((end - start)/100)





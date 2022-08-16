# lambdaInterpreter

An interpreter for lambda calculus in python. It uses lazy evaluation (memoized call by name)

# example usage:

To assign a term you want to use the parser of a string (watch out for parentheses since parenthesis inference is not implemented):
TRUE  = parser('(%x.(%y.x))')
FALSE = parser('(%x.(%y.y))')
OR  = parser('(%x.(%y.((x TRUE) y)))')

You also want to assign the names used for the terms in a dictionary:
dic['TRUE'] = TRUE
dic['FALSE'] = FALSE
dic['OR'] = OR

Then you call the evaluation with the betaRecMemo function:
test = parser('((OR TRUE) FALSE)')
result = betaRecMemo(test, dic)
result.show()
>> 'TRUE'

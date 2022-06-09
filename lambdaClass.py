class lambd :
    def __init__(self, Ninputs, Noutputs, shape, signature = []):
        
        self.Ninputs = Ninputs
        self.Noutputs = Noutputs
        self.Bnormal = "Don't know if normal"
    #def betanormal(self):
        #returns a boolean or text "don't know if normal" if the lambd is in betanormal form
        #return self.Bnormal
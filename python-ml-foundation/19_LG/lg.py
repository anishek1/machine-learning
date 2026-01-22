class MeraLin:

    def __init__(self):
        self.m=None
        self.b=None
    
    def fit(self,x_train,y_train):
        num=0
        den=0
        
        for i in range(x_train.shape[0]): 

            num=num+((x_train[i]-x_train.mean())*(y_train[i]-y_train.mean()))
            den=den+((x_train[i]-x_train.mean())*(x_train[i]-x_train.mean()))

        self.m=num/den
        self.b=y_train.mean()-(self.m* x_train.mean())
        print(self.m)
        print(self.b)
        
    def predict(self,x_test):

        print(x_test)
        return self.m * x_test + self.b
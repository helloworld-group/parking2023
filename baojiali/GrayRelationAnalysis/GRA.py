import numpy as np
A=np.array([[55,24,10],[65,38,22],[75,40,18],[100,50,20]])

aaaa=1
Mean=np.mean(A,axis=0)
print(Mean)

A_norm=A/Mean
print(A_norm)

Y=A_norm[:,0]
X=A_norm[:,1:]

absX0_Xi=np.abs(X-np.tile(Y.reshape(-1,1),reps=(1,X.shape[1])))

a=np.min(absX0_Xi)
b=np.max(absX0_Xi)
rho=0.5

gamma=(a+rho*b)/(abs+rho*b)

print(np.mean(gamma,axis=0))

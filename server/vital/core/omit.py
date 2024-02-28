import numpy as np

def OMIT(RGB):
    RGB = np.expand_dims(RGB.transpose(1, 0), 0)
    bvp = []
    for i in range(RGB.shape[0]):
        X = RGB[i]
        Q, R = np.linalg.qr(X)
        S = Q[:, 0].reshape(1, -1)
        P = np.identity(3) - np.matmul(S.T, S)
        Y = np.dot(P, X)
        bvp.append(Y[1, :])
    bvp = np.array(bvp)
    bvp = bvp.squeeze()
    return bvp
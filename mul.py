import numpy as np
from sklearn.linear_model import LogisticRegression

# def train(x,y):
#
#     LogisticRegression()
def __init__(self, base_clf):
    self.base_clf = ModelWrapper(copy.deepcopy(base_clf))
    self.n_labels = None
    self.clfs_ = []

def train(self, X, y):
    self.n_labels = np.shape(y)[1]

    for i in range(self.n_labels):
        clf = copy.deepcopy(self.base_clf)
        pred = np.zeros((len(X), i))
        for j in range(i):
            tempX = np.hstack((X, pred[:, :j]))
            pred[:, j] = self.clfs_[j].predict(tempX)
        print(i)
        clf.fit(np.hstack((X, pred[:, :i])), y[:, i])
        self.clfs_.append(clf)
def predict(self, X):
    pred = np.zeros((len(X), self.n_labels))
    for i in range(self.n_labels):
        tempX = np.hstack((X, pred[:, :i]))
        pred[:, i] = self.clfs_[i].predict(tempX)

    return pred.astype(int)








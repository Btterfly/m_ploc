from load import *
from sklearn import svm
import numpy as np
from sklearn.linear_model import LogisticRegression
import requests
def askJava(uuid,state):
    return requests.get(url="http://127.0.0.1:8989/sys-task/state?uuid="+uuid+"&state="+state)

def getXlistForH_i(X,Y,i):
    XL=[]
    for j in range(len(X)):
        x=X[j].tolist()
        # x=X[j]
        y=Y[j]
        # print(y[0:i])
        for yy in y[0:i]:
            x.append(yy)
        XL.append(x)
    return XL

def getTrainY(y,i):
    return [item[i] for item in y]
    pass

'''基分类器'''
def trainHi(X,Y,i,solver):
    print(i)
    lr=LogisticRegression(multi_class="ovr", solver=solver, random_state=1126,class_weight='balanced')
    # lr = svm.SVC(C=0.8, kernel='rbf', gamma=20, decision_function_shape='ovr',class_weight='balanced')
    lr.fit(getXlistForH_i(X,Y,i),getTrainY(Y,i))
    return lr

'''SVM'''
def trainHi_SVM(X,Y,i,solver):
    print(i)
    # lr=LogisticRegression(multi_class="ovr", solver=solver, random_state=1126,class_weight={0:0.1,1:0.1})
    # sv = svm.SVC(C=0.8, kernel='rbf', gamma=20, decision_function_shape='ovr',class_weight='balanced')
    sv = svm.SVC(C=0.5, kernel='linear', decision_function_shape='ovr',class_weight='balanced')
    sv.fit(getXlistForH_i(X,Y,i),getTrainY(Y,i))
    return sv

'''分类器链'''
def train(x,y,clf,m):
    if clf=="LogisticRegression":
        Hs=[]
        '''len(y)个基分类器'''
        for i in range(0,20):
            '''i:第i个基分类器'''
            Hs.append(trainHi_SVM(x,y,i,m["solver"]))
        return Hs

'''预测'''
def predict(Hs,xx,yy):
     xx=feature.getone_feature(xx,0.05,10)
     print("XXXXXXXXXXXXXX",xx)
     y=[]
     for i in range(0,20):
         lab=Hs[i].predict([xx])[0]
         # print(lab)
         if lab==1:
             y.append(yy[i])
         xx.append(lab)
     return y


def pre_main(uuid,xx,yy):
    Hs=np.load('C:/Users/mmh/Desktop/mPloc/model/moudle_'+uuid+'.npy', allow_pickle=True)
    res=predict(Hs,xx,yy)
    return res


def gettest_x(xx,j):
    for i in j:
        xx.append()


'''测试'''
def test(Hs,x,y):
    recall = 0
    precision = 0
    accuracy = 0
    specificity = 0
    loss = 0
    MCC = 0
    xx=x.tolist()
    print('----------------')
    for j in range(0, 20):
        TP = 0
        FP = 0
        TN = 0
        FN = 0
        for i in range(0, len(x)):
            yy=Hs[j].predict([xx[i]])[0]
            xx[i].append(yy)
            yt = y[i][j]
            if yt == yy and yy == 0:
                TN=TN+1
            if yt== yy and yy == 1:
                TP=TP+1
            if yy== 0 and yt == 1:
                FN=FN+1
            if yy== 1 and yt== 0:
                FP=FP+1
        accuracy=accuracy+(TP+TN)/(TP+FP+TN+FN)
        loss=loss+(FN+FP)/(TP+FP+TN+FN)
        recall=recall+TP/(TP+FN)
        if (TP+FP)==0:
            print(j)
        else:
            precision = precision + (TP / (FP + TP))
        specificity=specificity+TN/(FP+TN)
        if (TP + FP) == 0:
            print(j)
        else:
            MCC=MCC+(TP*TN-FP*FN)/np.sqrt((TP+FP)*(TP+FN)*(TN+FP)*(TN+FN))
        ac='accuracy:'+str(accuracy/20)
        lo='loss:'+str(loss/20)
        re='recall:'+str(recall/20)
        pr='precision:'+str(precision/20)
        sp='specificity:'+str(specificity/20)
        ma='MCC:'+str(MCC/20)

    return ac,lo,re,pr,sp,ma

def train_main(uuid,path,clf,m,split):
    xx,yy=getxy(path,0.1,5)
    sp=int(len(xx)*split)
    l=len(xx)-1
    x=np.array(xx)
    y=np.array(yy)
    askJava(uuid, "正在训练")
    Hs=train(x[0:sp],y[0:sp],clf,m)
    np.save('C:/Users/mmh/Desktop/mPloc/model/moudle_'+uuid,Hs)
    askJava(uuid,"正在测试")
    # test1=test(Hs,x[sp:l],y[sp:l])
    test2=test(Hs,x[0:sp], y[0:sp])
    askJava(uuid,str(test2))
#
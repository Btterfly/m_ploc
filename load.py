import csv
import feature
# Seq="MTDRARLRLHDTAAGVVRDFVPLRPGHVSIYLCGATVQGLPHIGHVRSGVAFDILRRWLLARGYDVAFIRNVTDIEDKILAKAAAAGRPWWEWAATHERAFTAAYDALDVLPPSAEPRATGHITQMIEMIERLIQAGHAYTGGGDVYFDVLSYPEYGQLSGHKIDDVHQGEGVAAGKRDQRDFTLWKGEKPGEPSWPTPWGRGRPGWHLECSAMARSYLGPEFDIHCGGMDLVFPHHENEIAQSRAAGDGFARYWLHNGWVTMGGEKMSKSLGNVLSMPAMLQRVRPAELRYYLGSAHYRSMLEFSETAMQDAVKAYVGLEDFLHRVRTRVGAVCPGDPTPRFAEALDDDLSVPIALAEIHHVRAEGNRALDAGDHDGALRSASAIRAMMGILGCDPLDQRWESRDETSAALAAVDVLVQAELQNREKAREQRNWALADEIRGRLKRAGIEVTDTADGPQWSLLGGDTK"
# lab_dec = {'plasma membrane': 0, 'mitochondrion': 1, 'golgi apparatus': 2, 'synapse': 3, 'centriole': 4,
#                    'microsome': 5, 'melanosome': 6, 'cortex': 7, 'endoplasmic reticulum': 8, 'cytoskeleton: 9,'
#                    'peroxisome': 10, 'centrosome': 11, 'extracellular space': 12, 'nucleus': 13, 'cell membrane': 14,
#                    'lysosome': 15, 'spindle': 16, 'acrosome': 17, 'cytoplasm': 18, 'endosome': 19
#                    }
lab_dec = ['plasma membrane','mitochondrion', 'golgi apparatus', 'synapse','centriole',
                   'microsome','melanosome', 'cortex','endoplasmic reticulum', 'cytoskeleton',
                   'peroxisome','centrosome', 'extracellular space','nucleus','cell membrane',
                   'lysosome','spindle', 'acrosome', 'cytoplasm', 'endosome']

def getxy(path,w,u):
    xx = []
    y = []
    with open(path) as f:
        file = csv.reader(f)
        xx = feature.getfile_feature(file, w, u)
        file = csv.reader(open(path))
        for row in file:
            t = []
            a = (row[2].split(','))
            for lab in lab_dec:
                isLab = False
                for x in range(len(a)):
                    if lab == a[x]:
                        t.append(1)
                        isLab = True
                        break
                if isLab is False:
                    t.append(0)
            y.append(t)
    return xx,y

def getyy():
    return lab_dec

    # def getxy(path):
    #     y=[]
    #     xx=[]
    #     with open(path) as f:
    #         file=csv.reader(f)
    #         xx=feature.getfile_feature(file,0.5,2)
    #         file=csv.reader(open(path))
    #         for row in file:
    #             lab=[0 for i in range(20)]
    #             a=(row[2].split(','))
    #             for i in a:
    #                 lab[lab_dec[i]]=1
    #             y.append(lab)
    #     return xx,y

    # print(feature.getone_feature(Seq,0.5,2))

    # feature.getfile_feature(file,0.5,2)
    #feature.getone_feature(str,double w,int lambda )
    #x=feature.getfile_feature(file,0.5,2)

    #np.save("C:/Users/mmh/Desktop/x.npy",np.array(x))
# xx = np.load("C:/Users/mmh/Desktop/x.npy")





# for row in file:
#     y.append(row[2])
#     lab = row[2].split(',')
#     t = [0 for i in range(0, 20)]
#     for i in lab:
#         t[lab_dec[i]] = 1
#     label.append(t)

# print(y)




    




# print(feature.getfile_feature(feature,file,0.5,1))
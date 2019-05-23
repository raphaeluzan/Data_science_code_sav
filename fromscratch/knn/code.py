import requests
import ast
from math import *
import numpy


r = requests.get('http://raphaeluzan.fr/data.php')
var = ast.literal_eval(r.text)


#A l'aide de la distance euclidienne on calcul la distance( vectoriel) entre deux utilisateurs
def distance_euclidienne(user1,user2):
    sum = 0
    for cle in var["fields"][0].keys():
        if cle != 'name':
            if (int(user2[cle]) > 0 ) and (int(user1[cle]) > 0 ):
                sum = sum + pow(int(user2[cle])-int(user1[cle]),2)

    return sqrt(sum)

def similarite_pearson(user1,user2):
    li1 = []
    li2 = []
    for cle in var["fields"][0].keys():
        if cle != 'name':
            if (int(user1[cle]) > 0) and (int(user2[cle]) > 0):
                li1.append(int(user1[cle]))
                li2.append(int(user2[cle]))
    return numpy.corrcoef(li1, li2)[0,1]

#Calcul d'indice de similarité entre deux utilisateurs
def similarite(user1,user2):
    return (1/(1+distance_euclidienne(user1,user2)))

#On tri le tableau li dans l'ordre decroissant
def tri_res(li):
    li.sort(key=lambda x: x[1],reverse=True)
    return li

def les_k_plus_proches_voisins(k,j):
    li=[]
    i=0
    while i < len(var["fields"]):
        if j==i:
            print('')
        else:
            li.append([var["fields"][i]["name"],similarite(var["fields"][i], var["fields"][j])])
        i=i+1
    return tri_res(li)[0:k]

def recommander(k,user):
    li = []
    knn = les_k_plus_proches_voisins(k,user)
    print(knn)
    i=0
    #On parcourt notre resultat pour ne garder que les noms d'utilisateurs les plus proches
    while i<k:
        li.append(knn[i][0])
        i=i+1
    res = []
    #On parcourt les films
    for cle in var["fields"][0].keys():
        p=0
        note =0
        moyenne = 0.0
        sum=0
        count = 0
        if cle != 'name':
            while p<k:
                r=0
                #On parcourt les personnes
                while r<len(var['fields']):
                    note = 0
                    if (str(var["fields"][r]["name"]) == str(knn[p][0])):
                        if int(var["fields"][r][cle]) >= 0:
                            note = var["fields"][r][cle]
                            count = count +1
                        else :
                            note=0
                        break

                    r = r+1
                moyenne = float(moyenne) + float(note)
                p=p+1
            if count != 0:
                moyenne = float(float(moyenne)/float(count))
            else :
                moyenne = float(-1)
            res.append([cle,int(moyenne)])
    return tri_res(res)

##On recupere la donnée en bloc
#print(var)

##Voir la liste des utilisateurs
i = 0
while i<len(var["fields"]) :
    print( str(i)+ "|| " + var["fields"][i]["name"] )
    i=i+1

##Afficher le detail sur un utilisateur
#print(var['fields'][0])

##distance euclidienne
#print(distance_euclidienne(var['fields'][1],var['fields'][14]))

##donner la similarité entre deux utilisateur
#print(similarite(var['fields'][1],var['fields'][14]))
#print(similarite(var['fields'][1],var['fields'][1]))
#print(similarite(var['fields'][1],var['fields'][1]))

##trouver les k plus proches
#print(les_k_plus_proches_voisins(4,4))
#print(les_k_plus_proches_voisins(4,1))

##recommandation de films a partir des k plus proches
#print(recommander(3,17))


#print(similarite_pearson(var['fields'][0],var['fields'][3]))
#print(recommander(3,0))

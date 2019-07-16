import pandas as pd
def words():




    a=pd.read_excel('C:\\Users\\acer\\Desktop\\comm.xlsx')
    l=list(a.ix[:,'Command'])
    l.sort()
    word=[]
    for x in l:
    	word+=x.split()
    word.sort()
    
    return l,list(set(word))

    
    

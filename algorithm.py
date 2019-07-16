import pandas as pd
def counter(sentence,words):
	returned_2D=[]
	for i in range(0,len(sentence)):
		dic={}
		for k in range(len(words)):
			count=0
			for v in range(len(sentence[i].split(' '))):
				if words[k]==sentence[i].split(' ')[v]:
					count=count+1
			dic[str(k)]=count
		returned_2D.append(list(dic.values()))
	return returned_2D	
#--------------------------------------------------------------------------------------------------------------------------------------#

def dictionary_builder(file):
	dic={}
	df=pd.read_excel(file)
	list_of_category=list(set(list(df.ix[:,'Actuall'])))
	commands=list(df.ix[:,'Command'])
	list_of_category.sort()
	for i in list_of_category:
		dic[i]=[]
		for v in range(df.shape[0]):
			if df.ix[v,'Actuall']==i:
				dic[i].append(commands[v])
	return dic
#-------------------------------------------------------------------------------------------------------------------------------------#

def probability(input_,unique_word_list,dictionary,counter_output):
	#rajat's function
	k=input_.split(' ')
	list_of_probability=[]
	for v in list(dictionary.keys()):
		prob_k=1
		for i in k:
			if i not in unique_word_list:
				prob_i=1/(len(dictionary[v])+len(unique_word_list))
			else:
				words=[]
				for tt in dictionary[v]:
					words+=tt.split(' ')
				
				prob_i=(words.count(i)+1)/(len(dictionary[v])+len(unique_word_list))
			prob_k=prob_k*prob_i
		list_of_probability.append(prob_k)
	print(list_of_probability)	
	return list(dictionary.keys())[list_of_probability.index(max(list_of_probability))]
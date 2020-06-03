import os
import itertools
from itertools import *
import numpy as np

# 1.Functions to retrieve our specific data from the dataset:
path = os.path.abspath(__file__).split(os.path.basename(__file__))[0]
class Dataset:
    def __init__(self,data_path,names_path=None,start_idx=21,l=12):
        self.start_idx = start_idx
        self.l = l
        self.selected = np.zeros(1)
        self.combinations=[]
         
        ## set possible column combinations
        for i in range(1,13):
            self.combinations+= list(map(list,list(combinations(range(0,12),i))))

        ## get column names for dataset columns
        if names_path is None:      
            self.col_headers = {'MSKB1': 5, 'MHHUUR': 9, 'MSKC': 7, 'MHKOOP': 10, 'MSKD': 8,\
                 'MBERARBO': 3, 'MBERBOER': 0, 'MSKB2': 6, 'MAUT1': 11, 'MBERARBG': 2,\
                      'MBERMIDD': 1, 'MSKA': 4}
        else:
            with open(names_path,'r') as head:
                self.labels = head.read().split('\n')
            self.labels = [label.split()[0:2] for label in self.labels if label !='' ]
            self.col_headers = dict()
            for label in self.labels[self.start_idx:self.start_idx+self.l]:
                self.col_headers[label[1]] = int(label[0])-self.start_idx
        
        ## read data from file

        with open(data_path,'r') as data_file:
            self.data = data_file.read().split('\n')[:-1]

        ## hold data into numpy array
        self.data = [np.reshape(np.char.array(line.split('\t')[self.start_idx-1:self.start_idx+l-1]),(12,1)) for line in self.data if line !='' ]
        self.data = np.transpose(np.concatenate(self.data,1))
        ## split data into list of numpy column vectors 
        self.data = np.hsplit(self.data,12)
        self.l = self.data[0].shape[0]

        ## format values for separation
        for i in range(12):
            s= '/'+ list(self.col_headers.keys())[list(self.col_headers.values()).index(i)] +','
            self.data[i] = np.core.defchararray.add(self.data[i],s)

        return
 
    def get_data(self,cols,rows=None):
        
        ## set rows range required
        if isinstance(rows,list):
            rows = slice(rows[0],rows[1]+1)
        elif rows is None:
            rows=slice(0,self.l)


        if isinstance(cols,(int,str)):
            cols = [cols]
        self.selected = []
        

        for col in cols:
            if isinstance(col,int):
                self.selected.append(self.data[col][rows])
            elif isinstance(col,str):
                self.selected.append(self.data[self.col_headers[col]][rows])

        return self.selected


def support(data,min_support,combs):
    '''
    data: list of lists: each list represent a column
    min_support: float
    combs : list of all columns combinations to be considered
    return: dictionary of min-support itemset
    '''

    itemsets = {}       ## item , occurences
    length = data[0].shape[0]
    for ii , comb in enumerate(combs):
        tot = data[comb[0]]
        ## merge columns in a combination into one column of concatenated strings
        if len(comb)>1:
            for i in range(1,len(comb)-1):
                tot = np.core.defchararray.add(tot,data[comb[i]])
        ## get unique values in column , and their occurenece number
        items,occ = np.unique(tot,return_counts=True)
        for i , (item , occ) in enumerate(zip(items,occ)):
            ## retrieve values with occureneces more than min_support 
            if occ/length > min_support:
                itemsets[item[:-1]] = occ/length


    return itemsets



def Perform_association_rules(support):
    counter = 0
    max = 0
    combins = []

    for k in support:
        for i in k:
            if ',' in i:
                counter += 1
        if (counter > max):
            max = counter
        counter = 0

    length = max + 1

    counter = 0
    final_combins = []
    for k in support:
        for i in k:
            if ',' in i:
                counter += 1
        if (length == counter + 1):
            combins = k
            List_Of_Dict = combins.split(',')
            final_combins.append(List_Of_Dict)

        counter = 0

    Trial_List = final_combins
    Final_List2 = []

    for j in range(len(Trial_List)):
        rules_comb = []
        for L in range(0, length):
            for subset in itertools.combinations(Trial_List[j], L):
                subset = list(subset)
                res = [i for i in Trial_List[j] if i not in subset]

                if (len(subset) != 0):
                    left = "\'"
                    for k in range(len(subset)):
                        left += subset[k]
                        if (k != len(subset) - 1):
                            left += ','

                    left += "\'"
                    right = "\'"
                    for k in range(len(res)):
                        right += res[k]
                        if (k != len(res) - 1):
                            right += ','

                    right += "\'"
                    str = left + ',' + right
                    li = list(str.split("',"))
                    # print(li)
                    li = [s.replace('\'', '') for s in li]
                    rules_comb.append(li)
        Final_List2.append(rules_comb)

    return Final_List2


def final_association_rules(all_association_rules,support,min_confidence):
    Final_association_rules = []
    length = len(all_association_rules)

    j = 0
    left_and_right = ""
    for i in range(length):
        rule = all_association_rules[i]         # deh list: [['1/0', '3/0'], ['3/0', '1/0']]
        rule_combination_length = len(rule)     # 2
        for k in range(rule_combination_length):
            left = rule[k][j]
            right = rule[k][j + 1]
            if k == 0:
                left_and_right = left + ',' + right

            support_left = support[left]
            support_left_and_right = support[left_and_right]
            confidence = ((support_left_and_right) / (support_left))

            if confidence < min_confidence:
                continue

            Final_association_rules.append([left, right, confidence])

    return Final_association_rules



def Lift_Levarage (rules,support):
  levarage = []
  lift = []
  output = []
  x=len(rules)
  for i in range (x):
    # 1.support left side:
    left = rules[i][0]
    supleft = support[left]

    # 2.support right side:
    right = rules[i][1]
    supright = support[right]

    # 3.support lift and right:
    confidence_value = rules[i][2]
    supint = (confidence_value) * (supleft)

    # 4.Calculate levarage value:
    lev = (supint - (supleft*supright))
    levarage.append(lev)

    # 5.Calculate lift value:
    value = confidence_value *(1/supright)
    lift.append(value)

    output.append(lift[i]-levarage[i])
  return levarage, lift,output

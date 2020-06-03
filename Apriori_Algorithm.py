from Functions import *
import time

# 1.Read the determined data from the customer data set for an insurance company:
data = Dataset(path+'ticdata2000.txt')
ret = data.get_data(range(0,12))

# 2.User defined min support and min confidence:
min_support = float(input('Enter the min support = '))
min_confidence = float(input('Enter the min confidence = '))

# 3.Calculate support data items:
Support_Data_Items = support(ret,min_support,data.combinations)

# 4.Find all possible association rules within the largest support order:
All_Association_Rules = Perform_association_rules(Support_Data_Items)

# 5.Find the final association rules which its confidence value is larger/equal the min confidence:
Final_Association_Rules = final_association_rules(All_Association_Rules,Support_Data_Items,min_confidence)

# 6.Find Lift and leverage for the final association rules:
#print(len(Final_Association_Rules))
levarage, lift, output = Lift_Levarage(Final_Association_Rules, Support_Data_Items)

levarage,lift,Final_Association_Rules = zip(*sorted(zip(levarage,lift,Final_Association_Rules),key = lambda tup : tup[1]))

# 7.representing the results:
print('\n'+'Final Result:')
for i in range (len(levarage)):
    rule = Final_Association_Rules[i][0] + '--->' + Final_Association_Rules[i][1]
    confidence = Final_Association_Rules[i][2]
    lev = levarage[i]
    lif = lift[i]
#    print('*', rule, ', confidence = ',confidence, ', levarage = ',lev, ', lift = ',lif)
    print('* %-100s \n\t confidence = %.8f , leverage = %.8f , lift = %.8f'%(rule,confidence,lev,lif))

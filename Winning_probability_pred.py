# -*- coding: utf-8 -*-
"""probability_win_data.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1gPWbs-ub61BccfNB_fhmS1nAP4Rsx_vv
"""

#classification realted functions
def check_straight(dic):    
    '''
      input: dictionary containing card info      
    '''    
    # Extract classes
    C1 = dic['C1'] 
    C2 = dic['C2'] 
    C3 = dic['C3'] 
    C4 = dic['C4'] 
    C5 = dic['C5']
    
    class_flag = 1
    
    # Make a class list 
    C = [C1, C2, C3, C4, C5]
    
    # Sort the list 
    C.sort()
    
    # Start checking for an order
    for i in range(len(C)-1):
        if C[i+1]==C[i]+1:
            pass
        else:
            class_flag = 0
            break
    return class_flag

def series_to_dict(ser):
    dic = {} 
    
    # Allot dictionary positions
    dic['S1'] = ser[0]
    dic['C1'] = ser[1]
    dic['S2'] = ser[2]
    dic['C2'] = ser[3]
    dic['S3'] = ser[4]
    dic['C3'] = ser[5]
    dic['S4'] = ser[6]
    dic['C4'] = ser[7]
    dic['S5'] = ser[8]
    dic['C5'] = ser[9]
    
    # Return the dectionary 
    return dic

def check_flush(dic):    
    '''
      input: dictionary containing card info      
    '''
    # Extract suites 
    S1 = dic['S1'] 
    S2 = dic['S2'] 
    S3 = dic['S3'] 
    S4 = dic['S4'] 
    S5 = dic['S5'] 
    
    # Check if all suites same 
    if S1 == S2 == S3 == S4 == S5:
        return 1    # all matching suites
    else: 
        return 0

def check_royal(dic):    
    '''
      input: dictionary containing card information      
    '''    
    # Extract classes
    C1 = dic['C1'] 
    C2 = dic['C2'] 
    C3 = dic['C3'] 
    C4 = dic['C4'] 
    C5 = dic['C5']
    
    # Make a class list 
    C = [C1, C2, C3, C4, C5]
    C.sort()
    
    # Check for Royal 
    if C[0] == 1: 
        for i in range(1, 5):
            if C[i] != 9 + i:
                       return 0
        return 1

def check_from_4_to_9(dic):    
    '''
      input: dictionary containing all cards' info      
    '''    
    # Extract classes
    C1 = dic['C1'] 
    C2 = dic['C2'] 
    C3 = dic['C3'] 
    C4 = dic['C4'] 
    C5 = dic['C5']
    
    # Counts the number of unique cards in the sorted list
    counter = 1
    
    # Make a class list 
    C = [C1, C2, C3, C4, C5]
    C.sort()
    
    # Looping through all cases
    for i in range(1,5):
        if C[i] == C[i-1]:
            pass
        else: 
            counter += 1
    
    # 4 unique cards mean one pair
    if counter == 4:
        return 1    # Assigned label 
    
    # 3 unique cards could mean 2 pair or 3 of a kind 
    elif counter == 3: 
        
        # create counters for val counts 
        count = [1, 0, 0]
        
        j = 0
        for i in range(1, 5):
            if C[i] == C[i-1]:
                count[j] += 1
            else:
                j+=1
                count[j] += 1
        # Sort value counts list 
        count.sort()
        
        if count[2] == 2:
            return 2    # TWO PAIR CONDITION SATISFIED 
        
        if count[2] == 3: 
            return 3    # THREE OF A KIND CONDTITION SATISFIED 
    
    # If 2 unique cards then we could have 4 of a kind or full house 
    elif counter == 2: 
        
        # Check condition for four of a kind 
        if C[0] == C[1]:
            if C[0] == C[1] == C[2] == C[3]:
                return 7    # Four of a kind contion satisfied
            else:
                # Check full house conditions 
                return 6
        else:
            # Only four of a kind possible 
            return 7
    
    # If none
    else:
        return 0

def assign_hand_label(ser):    
    '''
      input: Series containing all the card information
      output: card hand label
    '''    
    # Extract Data 
    hand = series_to_dict(ser)
    # Check if a flush 
    if check_flush(hand):
        
        # Check if a Royal Flush 
        if check_royal(hand):
            return 9
        
        # Check if straight flush 
        elif check_straight(hand):
            return 8
        
        else: 
            return 5 
    
    # Check for the rest 
    if check_straight(hand) or check_royal(hand):
        return 4
    else:
        return check_from_4_to_9(hand)

# General Libraries
import numpy as np
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
from tabulate import tabulate
import seaborn as sns
from random import sample
import csv

# Machine Learning
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error
from sklearn.metrics import f1_score


# training_data =  pd.read_csv("poker-hand-training-true.data", header=None, sep=",")
testing_data =  pd.read_csv("poker-hand-testing.data", header=None, sep=",")

def get_labeled_features(data_frame):  
    last_col = list(data_frame.columns)[-1]
    phi = data_frame.drop(columns = [last_col]).copy()
    y = data_frame[last_col]
    phi=phi.to_numpy()
    return phi

def straight_flush_winner(sampled_hand,actual_hand):
    sampled_hand=np.array(sampled_hand)
    actual_hand=np.array(actual_hand)
    sampled_hand_max=np.max(np.delete(sampled_hand,[0,2,4,6,8]).astype(int))
    actual_hand_max=np.max(np.delete(actual_hand,[0,2,4,6,8]).astype(int))
    if(sampled_hand_max > actual_hand_max):
        return 0
    else:
        return 1

def four_of_kind_winner(sampled_hand,actual_hand):
    sampled_hand=np.array(sampled_hand)
    actual_hand=np.array(actual_hand)
    sampled_hand=np.delete(sampled_hand,[0,2,4,6,8]).astype(int)
    actual_hand=np.delete(actual_hand,[0,2,4,6,8]).astype(int)

    if(sampled_hand[0]==sampled_hand[1]):
        sample=sampled_hand[0]
    elif(sampled_hand[0]==sampled_hand[2]):
        sample=sampled_hand[0]
    else :
        sample=sampled_hand[1]

    if(actual_hand[0]==actual_hand[1]):
        actual=actual_hand[0]
    elif(actual_hand[0]==actual_hand[2]):
        actual=actual_hand[0]
    else :
        actual=actual_hand[1]

    if(sample>actual):
        return 0
    else:
        return 1

def flush_winner(sampled_hand,actual_hand):
    sampled_hand=np.array(sampled_hand)
    actual_hand=np.array(actual_hand)
    sampled_hand=np.sort(np.delete(sampled_hand,[0,2,4,6,8]).astype(int))
    actual_hand=np.sort(np.delete(actual_hand,[0,2,4,6,8]).astype(int))
    for i in range(5):
        if(actual_hand[4-i]>sampled_hand[4-i]):
            return 1
        elif(actual_hand[4-i]<sampled_hand[4-i]):
            return 0
    return 0

def straight_winner(sampled_hand,actual_hand):
    sampled_hand=np.array(sampled_hand)
    actual_hand=np.array(actual_hand)
    sampled_hand_max=np.max(np.delete(sampled_hand,[0,2,4,6,8]).astype(int))
    actual_hand_max=np.max(np.delete(actual_hand,[0,2,4,6,8]).astype(int))
    if(sampled_hand_max > actual_hand_max):
        return 0
    else:
        return 1

def three_of_kind_winner(sampled_hand,actual_hand):
    sampled_hand=np.array(sampled_hand)
    actual_hand=np.array(actual_hand)
    sampled_hand=np.sort(np.delete(sampled_hand,[0,2,4,6,8]).astype(int))
    actual_hand=np.sort(np.delete(actual_hand,[0,2,4,6,8]).astype(int))
    if(actual_hand[2]>=sampled_hand[2]):
        return 1
    else:
        return 0

def pair_winner(sampled_hand,actual_hand):
    sampled_hand=np.array(sampled_hand)
    actual_hand=np.array(actual_hand)
    sampled_hand=np.sort(np.delete(sampled_hand,[0,2,4,6,8]).astype(int))
    actual_hand=np.sort(np.delete(actual_hand,[0,2,4,6,8]).astype(int))
    for i in range(4):
        if(sampled_hand[i]==sampled_hand[i+1]):
            sample=sampled_hand[i]
            break
    for i in range(4):
        if(sampled_hand[i]==sampled_hand[i+1]):
            actual=actual_hand[i]
            break
    if(actual>=sample):
        return 1
    else:
        return 0

def high_winner(sampled_hand,actual_hand):
    sampled_hand=np.array(sampled_hand)
    actual_hand=np.array(actual_hand)
    sampled_hand_max=np.max(np.delete(sampled_hand,[0,2,4,6,8]).astype(int))
    actual_hand_max=np.max(np.delete(actual_hand,[0,2,4,6,8]).astype(int))
    if(actual_hand_max>=sampled_hand_max):
        return 1
    else:
        return 0

def tie_breaker(sampled_hand,actual_hand,hand_class):
    if(hand_class==9):
        return 1
    if(hand_class==8):
        return straight_flush_winner(sampled_hand,actual_hand)
    if(hand_class==7):
        return four_of_kind_winner(sampled_hand,actual_hand)
    if(hand_class==6):
        return full_house_winner(sampled_hand,actual_hand)
    if(hand_class==5):
        return flush_winner(sampled_hand,actual_hand)
    if(hand_class==4):
        return straight_winner(sampled_hand,actual_hand)
    if(hand_class==3):
        return three_of_kind_winner(sampled_hand,actual_hand)
    if(hand_class==2):
        return Two_pair_winner(sampled_hand,actual_hand)
    if(hand_class==1):
        return pair_winner(sampled_hand,actual_hand)
    if(hand_class==0):
        return high_winner(sampled_hand,actual_hand)

def full_house_winner(sampled_hand, actual_hand):
    sampled_hand=np.array(sampled_hand)
    actual_hand=np.array(actual_hand)
    sampled_hand=np.sort(np.delete(sampled_hand,[0,2,4,6,8]).astype(int))
    actual_hand=np.sort(np.delete(actual_hand,[0,2,4,6,8]).astype(int))

    if(actual_hand[2] >= sampled_hand[2]):
      return 1
    else:
      return 0

def Two_pair_winner(sampled_hand, actual_hand):
    sampled_hand=np.array(sampled_hand)
    actual_hand=np.array(actual_hand)
    sampled_hand=np.delete(sampled_hand,[0,2,4,6,8]).astype(int)
    actual_hand=np.delete(actual_hand,[0,2,4,6,8]).astype(int)

    sampled_hand= np.sort(sampled_hand)
    actual_hand= np.sort(actual_hand)

    max_hand_sample= sampled_hand[3]
    max_hand_actual= actual_hand[3]

    next_hand_sample= sampled_hand[1]
    next_hand_actual= actual_hand[1]

    if (max_hand_sample<=max_hand_actual):
      return 1
    elif (max_hand_sample > max_hand_actual):
      return 0
    else:
      if(next_hand_sample>next_hand_actual):
        return 0
      else:
        return 1

def predict_win(card_decks_10,actual_hand):
    hand= []
    hand1= []
    hand2= []

    for i in range(5):
      suit= ((actual_hand[i]-1)/13) + 1
      hand.append(suit)
      number= (actual_hand[i]-1)%13 + 1
      hand.append(number)

    for i in range(5):
      suit= ((card_decks_10[i]-1)/13) + 1
      hand1.append(suit)
      number= (card_decks_10[i]-1)%13 + 1
      hand1.append(number)

    for i in range(5,10):
      suit= ((card_decks_10[i]-1)/13) + 1
      hand2.append(suit)
      number= (card_decks_10[i]-1)%13 + 1
      hand2.append(number) 

    label= assign_hand_label(hand)
    label1= assign_hand_label(hand1)
    label2= assign_hand_label(hand2)

    if (label < label1 or label< label2):
      return 0
    elif (label > label1 and label > label2):
      return 1
    elif (label1 == label2):
      if(tie_breaker(hand1, hand2,label1)==1):
        return tie_breaker(hand2,hand,label2)
      else:
        return tie_breaker(hand1,hand,label1)
    else:
      if(label1>label2):
        return tie_breaker(hand1,hand,label)   
      else:
        return tie_breaker(hand2,hand,label)

def winning_probability(hand_):
    deck=np.arange(1,53)
    hand_=(hand_-1).astype(int)
    left_cards=np.delete(deck,hand_)
    N_win=0
    for i in range(5000):
        card_deck_10=sample(np.ndarray.tolist(left_cards),10)
        # print(card_deck_10)
        N_win+=predict_win(card_deck_10,hand_)
    # print(card_deck_10)
    return N_win/5000

win_prob=np.zeros((25010, 2))
hand_card=get_labeled_features(training_data)
for j in range(25010):
    hand=np.zeros(5)
    for i in range(5):
        hand[i]=(hand_card[j][2*i]-1)*13 + hand_card[j][2*i+1]
    win_prob[j][1]= winning_probability(hand)
    win_prob[j][0]= j + 1
    print(win_prob[j],j+1)


fields = ['Number', 'Probability']

filename = "ProbabilityData.csv"
    
with open(filename, 'w') as csvfile: 
    csvwriter = csv.writer(csvfile) 

    csvwriter.writerow(fields) 

    csvwriter.writerows(win_prob)

win_prob=np.zeros((8000, 2))
hand_card=get_labeled_features(testing_data)
for j in range(8000):
    hand=np.zeros(5)
    for i in range(5):
        hand[i]=(hand_card[j][2*i]-1)*13 + hand_card[j][2*i+1]
    win_prob[j][1]= winning_probability(hand)
    win_prob[j][0]= j + 1
    print(win_prob[j],j+1)

import csv
fields = ['Number', 'Probability']

filename = "ProbabilityData_Test.csv"
    
with open(filename, 'w') as csvfile: 
    csvwriter = csv.writer(csvfile) 

    csvwriter.writerow(fields) 

    csvwriter.writerows(win_prob)

"""Least Square Estimation: no hyperParameter Tuning"""

from sklearn import linear_model

Probabilities =  pd.read_csv("ProbabilityData.csv", header=None, sep=",")
sr_no= list(Probabilities.columns)[0]
Probabilities= Probabilities.drop(columns = [sr_no]).copy()
Probabilities=Probabilities.to_numpy()
Probabilities = np.delete(Probabilities, [0])

Probabilities_test =  pd.read_csv("ProbabilityData_Test.csv", header=None, sep=",")
sr_no= list(Probabilities_test.columns)[0]
Probabilities_test= Probabilities_test.drop(columns = [sr_no]).copy()
Probabilities_test=Probabilities_test.to_numpy()
Probabilities_test = np.delete(Probabilities_test, [0])

hand_card=get_labeled_features(training_data)
hand_card_test= get_labeled_features(testing_data)
hand_card_test= hand_card_test[0:2000, :]

model_LSE = linear_model.LinearRegression()

model_LSE.fit(hand_card, Probabilities)

# NEED TO USE THIS ON TEST DATA
Probabilities_pred = model_LSE.predict(hand_card)

Probabilities_pred_test= model_LSE.predict(hand_card_test)

print("Coefficients: \n", model_LSE.coef_)
print("Mean squared error Training: %.2f" % mean_squared_error(Probabilities, Probabilities_pred))

print("Mean squared error Test: %.2f" % mean_squared_error(Probabilities_test, Probabilities_pred_test))

from sklearn import linear_model

Probabilities =  pd.read_csv("ProbabilityData.csv", header=None, sep=",")
print(Probabilities)
sr_no= list(Probabilities.columns)[0]
Probabilities= Probabilities.drop(columns = [sr_no]).copy()
print(Probabilities)
Probabilities=Probabilities.to_numpy()
Probabilities = np.delete(Probabilities, [0])
print(Probabilities)


'''
Probabilities_test =  pd.read_csv("ProbabilityData_Test.csv", header=None, sep=",")
sr_no= list(Probabilities_test.columns)[0]
Probabilities_test= Probabilities_test.drop(columns = [sr_no]).copy()
Probabilities_test=Probabilities_test.to_numpy()
Probabilities_test = np.delete(Probabilities_test, [0])

hand_card=get_labeled_features(training_data)
hand_card_test= get_labeled_features(testing_data)
hand_card_test= hand_card_test[0:2000, :]
'''

model_LSE = linear_model.LinearRegression()

model_LSE.fit(hand_card, Probabilities)

# NEED TO USE THIS ON TEST DATA
Probabilities_pred = model_LSE.predict(hand_card)

Probabilities_pred_test= model_LSE.predict(hand_card_test)

print("Coefficients: \n", model_LSE.coef_)
print("Mean squared error Training: %.2f" % mean_squared_error(Probabilities, Probabilities_pred))

print("Mean squared error Test: %.2f" % mean_squared_error(Probabilities_test, Probabilities_pred_test))

"""Ridge Regression"""

from sklearn import linear_model

Probabilities =  pd.read_csv("ProbabilityData.csv", header=None, sep=",")
sr_no= list(Probabilities.columns)[0]
Probabilities= Probabilities.drop(columns = [sr_no]).copy()
Probabilities=Probabilities.to_numpy()
Probabilities = np.delete(Probabilities, [0])

hand_card=get_labeled_features(training_data)


reg2 = linear_model.RidgeCV(alphas=np.logspace(-6, 6, 13))
reg2.fit(hand_card, Probabilities)
reg2.alpha_

model_Ridge= linear_model.Ridge(alpha=10000)
model_Ridge.fit(hand_card, Probabilities)
Probabilities_pred_r = model_Ridge.predict(hand_card)

Probabilities_test =  pd.read_csv("ProbabilityData_Test.csv", header=None, sep=",")
sr_no= list(Probabilities_test.columns)[0]
Probabilities_test= Probabilities_test.drop(columns = [sr_no]).copy()
Probabilities_test=Probabilities_test.to_numpy()
Probabilities_test = np.delete(Probabilities_test, [0])

hand_card_test= get_labeled_features(testing_data)
hand_card_test= hand_card_test[0:2000, :]

model_Ridge.fit(hand_card, Probabilities)

Probabilities_pred_test= model_LSE.predict(hand_card_test)


print("Coefficients: \n", model_Ridge.coef_)
print("Mean squared error: %.2f" % mean_squared_error(Probabilities, Probabilities_pred_r))
print("Mean squared error: %.2f" % mean_squared_error(Probabilities_test, Probabilities_pred_test))
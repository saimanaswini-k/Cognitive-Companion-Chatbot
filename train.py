import docx
#chat utilities
from nltk.chat.util import Chat, reflections
import random
import re
#similarity
import warnings
warnings.filterwarnings("ignore")
from gensim.parsing.preprocessing import remove_stopwords
from fuzzywuzzy import fuzz
import operator


def readtxt(filename):
    doc = docx.Document(filename)
    fullText = []
    for para in doc.paragraphs:
        fullText.append(para.text)
    return '\n'.join(fullText)

data1=readtxt('Datasets/dataset.docx')

def data_prepping(data):
    data2=data.split('\n')
    data2=[d.strip() for d in data2]
    data2=[d for d in data2 if d!='']

    questions=[]; answers=[]

    for i in range(len(data2)):
        if i%2==0:
            answers.append(data2[i])
        else:
            questions.append(data2[i])
    return questions, answers

questions, answers=data_prepping(data1)

#Four elements in chat
class MyChat(Chat):

    def __init__(self, pairs, reflections={}):

        # add `z` because now items in pairs have three elements
        self._pairs = [(re.compile(x, re.IGNORECASE), y, z, p) for (x, y, z, p) in pairs]
        self._reflections = reflections
        self._regex = self._compile_reflections()

    def respond(self, str):

        # add `callback` because now items in pairs have three elements
        for (pattern, response, callback, flag) in self._pairs:
            match = pattern.match(str)
            if match:

                resp = random.choice(response)
                resp = self._wildcards(resp, match)

                if resp[-2:] == '?.':
                    resp = resp[:-2] + '.'
                if resp[-2:] == '??':
                    resp = resp[:-2] + '?'

                # run `callback` if exists
                if callback: # eventually: if callable(callback):
                    callback(match,flag)

                return resp

###All variables
patient_name=None;
action1=None; action2=None

def similarity_check(match, flag):
    sim = []
    groups=match.groups()
    query=groups[0]
    for key, value in df_sim.items():
        sim.append(fuzz.token_sort_ratio(remove_stopwords(key), remove_stopwords(query)))
    index, value = max(enumerate(sim), key=operator.itemgetter(1))
    if value < 70:
        pass
        # check_options(match, flag)
        ans = "Could not understand your query."
        print(ans)
    else:
        ans = list(df_sim.items())[index][1]
        print(ans)

###All functions
def enter_name(match, flag):
    global action1
    global patient_name
    if action1==None:
        groups = match.groups()
        patient_name=groups
        bot3=patient_name[0]+answers[3][1:]
        print(bot3)
        action1=4 #Jumping to 4th user query or greeting
    elif action1==4:
        bot4 = answers[4].replace('X', patient_name[0])
        print(bot4)
        action1=8 #To 8th user query
    elif action1==8:
        bot4=answers[9]
        print(bot4)

def user_agree(match, flag):
    global action2
    if action2==None:
        #question[1] related work
        bot2 = answers[2]
        print(bot2)
        action2=6 #indicating ready for question[6]
    elif action2==6:
        bot2=answers[7].replace('X',patient_name[0])
        print(bot2)
        action2=10
    elif action2==10:
        bot2=answers[11]
        print(bot2)
        action2=16
    elif action2==16:
        bot2=answers[17].replace('X',patient_name[0])
        print(bot2)
        action2=24
    elif action2==24:
        bot2=answers[25]
        print(bot2)
        action2=26
    elif action2==26:
        bot2=answers[27].replace('. ','\n')
        print(bot2)

###Chat System begining
pairs=[]
#Note: the response to questions[i] is answers[i+1]. The entire chat starts with answers[0]
print(answers[0])
#The start
user1='((hello|hay|hi)[\s]?(medibot)?)'
bot1=[answers[1]]
pairs.append([user1, bot1, None, None])

user2='^(yes|yeah|okay|ok)[\s]?[,]?[!]*[\s]?(sure)?$'
pairs.append([user2, [''], user_agree, None])

#Entering the name
# user3='(.+)[\s](.+)'
# user3='^\w+\s\w+$'
user3=r"^\b([a-zA-Z]+)\s([a-zA-Z]+)\b"
pairs.append([user3, [''], enter_name, None])

#Replying to the entered name
user4='(thanks|thank you|thanks a lot)'
pairs.append([user4, [''], enter_name, None])

user5='^(.+)$'
# bot7=[remove_prefix(data[33])+remove_prefix(data[34])]
pairs.append([user5, [''], similarity_check, None])

df_sim={}
#if medibot is a person
df_sim[questions[4]]=answers[5]
df_sim[questions[5]]=answers[6]
#questions[6] requires user_agree function
df_sim[questions[7]]=answers[8]
#questions[8] requires enter_name function
df_sim[questions[9]]=answers[10]
#questions[10 requires user_agree function
df_sim[questions[11]]=answers[12]
df_sim[questions[12]]=answers[13]
df_sim[questions[13]]=answers[14]
df_sim[questions[14]]=answers[15]
df_sim[questions[15]]=answers[16]
# df_sim[questions[16]]=answers[17] #single word yes question #answers requires replacing X with name
df_sim[questions[17]]=answers[18]
df_sim[questions[18]]=answers[19]
df_sim[questions[19]]=answers[20]
df_sim[questions[20]]=answers[21]
df_sim[questions[21]]=answers[22]
df_sim[questions[22]]=answers[23] #Question is single word Oh
df_sim[questions[23]]=answers[24]
# df_sim[questions[24]]=answers[25] #Single word yes
df_sim[questions[25]]=answers[26]
# df_sim[questions[26]]=answers[27] #single word yes
df_sim[questions[27]]=answers[28]
df_sim[questions[28]]=answers[29]
df_sim[questions[29]]=answers[30]
df_sim[questions[30]]=answers[31]
df_sim[questions[31]]=answers[32]



### Run chatbot
chat=MyChat(pairs, reflections)
# chat.converse()

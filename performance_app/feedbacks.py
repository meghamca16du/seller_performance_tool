from feedbacks_app.models import *
from nltk.tokenize import sent_tokenize,word_tokenize
from nltk.corpus import stopwords
from nltk import pos_tag
from nltk import WordNetLemmatizer
from nltk.corpus import sentiwordnet as swn

class polarity:
    def find_feedbacks(self):
        feedbacks_obj = FeedbackDetails.objects.all().filter(oid__sid='ank202').values('feedbackEntered')
        return feedbacks_obj

    def clean(self,feedback):
        clean_text=[]
        stop_words=set(stopwords.words("english"))
        negation_words=['not', 'no', 'rather', "couldn't", "wasn't", "didn't", "wouldn't", "shouldn't", "weren't",
         "don't", "doesn't", "haven't", "hasn't", 'won’t', 'wont', "hadn't", 'never', 'none', 'nobody', 'nothing', 
         'neither', 'nor', 'nowhere', "isn't", "can't", 'cannot', "mustn't", "mightn't", 'without', "needn't",
          "shan't"]
        for neg_word in negation_words:
            if neg_word in stop_words:
                stop_words.remove(neg_word)
        tokenize_text=word_tokenize(feedback)
        for token in tokenize_text:
            token=token.lower()
            if token not in stop_words:
                clean_text.append(token)
        return clean_text

    def tagging(self,clean_text):
        tagged_text=pos_tag(clean_text)
        return tagged_text


    def calc_senti_score(self,tagged_text):
        score_list=[]
        #score_list_neg=[]
        wnl = WordNetLemmatizer()
        #positive_score=0
        #negative_score=0
        count=0


        for word,tag in tagged_text:
            lemmatized=wnl.lemmatize(word)
            syn_score=0
            if tag.startswith('NN'):
                    newtag='n'
            elif tag.startswith('JJ'):
                newtag='a'
            elif tag.startswith('V'):
                newtag='v'
            elif tag.startswith('R'):
                newtag='r'
            else:
                newtag=''
            if(newtag!=''):
                synsets=list(swn.senti_synsets(lemmatized,newtag)) 
                if(len(synsets)>0):
                    syn_pos=0
                    syn_neg=0
                    for syn in synsets:
                        syn_score=syn_score+syn.pos_score()-syn.neg_score()
                    syn_score=syn_score/len(synsets)
                    #print(lemmatized)
                    #print(syn_score)
                    count+=1
            score_list.append(syn_score)
        total_score=sum(score_list)/count
        #print("total score of ", tagged_text," " ,total_score)
        if(total_score>=0):
            return True
        else:
            return False


    def call_functions(self):
        feedbacks_list=self.find_feedbacks()
        pos=0
        neg=0
        score=[]
        count=0
        for feedback_dict in feedbacks_list:
            clean_text=self.clean(feedback_dict['feedbackEntered'])
            tagged_text=self.tagging(clean_text)
            polarity=self.calc_senti_score(tagged_text)
            if polarity:
                pos+=1
            else:
                neg+=1
            count=count+1
        print(count)
        score.append((pos/count)*100)
        score.append((neg/count)*100)
        return score
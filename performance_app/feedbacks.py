from feedbacks_app.models import *
from nltk.tokenize import sent_tokenize,word_tokenize
from textblob import TextBlob
from nltk.corpus import stopwords
from nltk import pos_tag
from nltk import WordNetLemmatizer
from nltk.corpus import sentiwordnet as swn

class polarity:
    def find_feedbacks(self,from_date,to_date,current_sellerid):
        feedbacks_obj=Feedbacks.objects.all().filter(
                        product_id__sid=current_sellerid
                        ).filter(
                        feedback_date__gte=from_date
                        ).filter(
                        feedback_date__lte=to_date
                        ).values('feedback')
        return feedbacks_obj

        feedbacks_obj = Feedbacks.objects.all().filter(product_id__sid='S01REY').values('feedback')
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
        tokenize_text = word_tokenize(feedback)
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
        wnl = WordNetLemmatizer()  #plural-to-singular
        #positive_score=0
        #negative_score=0
        count=0


        for word,tag in tagged_text:
            lemmatized=wnl.lemmatize(word)
            syn_score=0
            if tag.startswith('NN'):  #noun
                    newtag='n'
            elif tag.startswith('JJ'):  #adjective
                newtag='a'
            elif tag.startswith('V'):  #verb
                newtag='v'
            elif tag.startswith('R'):  #adverb
                newtag='r'
            else:
                newtag=''
            if(newtag!=''):
                synsets=list(swn.senti_synsets(lemmatized,newtag)) 
                if(len(synsets)>0):
                    syn_pos=0
                    syn_neg=0
                    for syn in synsets:
                        syn_score = syn_score + syn.pos_score() - syn.neg_score()
                    syn_score = syn_score/len(synsets)  #taking average
                    #print(lemmatized)
                    #print(syn_score)
                    count+=1
            score_list.append(syn_score)
        total_score = sum(score_list) / count
        #print("total score of ", tagged_text," " ,total_score)
        if(total_score >= 0):
            return True
        else:
            return False

    def calc_positive_feedbacks(self,from_date,to_date,current_sellerid):
        feedbacks_list=self.find_feedbacks(from_date,to_date,current_sellerid)
        pos=0
        count=0
        for feedback_dict in feedbacks_list:
            clean_text=self.clean(feedback_dict['feedback'])
            tagged_text=self.tagging(clean_text)
            polarity=self.calc_senti_score(tagged_text)
            if polarity:
                pos+=1
            count+=1
        return round((pos/count)*100,2)

    def calc_negative_feedbacks(self,from_date,to_date,current_sellerid):
        feedbacks_list=self.find_feedbacks(from_date,to_date,current_sellerid)
        neg=0
        count=0
        for feedback_dict in feedbacks_list:
            clean_text=self.clean(feedback_dict['feedback'])
            tagged_text=self.tagging(clean_text)
            polarity=self.calc_senti_score(tagged_text)
            if not polarity:
                neg+=1
            count+=1
        return round((neg/count)*100,2)

    def negative_feedbacks(self,feedback_entered):
        negative_feedbacks = {}
        clean_text=self.clean(feedback_entered)
        tagged_text=self.tagging(clean_text)
        polarity=self.calc_senti_score(tagged_text)
        if not polarity:
            return True
        else:
            return False

    def positive_feedbacks(self,feedback_entered):
        positive_feedbacks = {}
        clean_text=self.clean(feedback_entered)
        tagged_text=self.tagging(clean_text)
        polarity=self.calc_senti_score(tagged_text)
        if polarity:
            return True
        else:
            return False
#
# Kerin Grewal
#
# Final Project

import math
class TextModel:

    def __init__(self, model_name):
        """a constructor for the TextModel class"""

        self.name = model_name
        self.words = {}
        self.word_lengths = {}
        self.stems={}
        self.sentence_lengths={}
        self.endings={}
        self.total = 0
        
    def __repr__(self):
        """returns the model name, number of words and number of word lengths
           in the dictionary
        """
        s= 'text model name: ' + self.name + '\n'
        s+= 'number of words: ' + str(len(self.words)) + '\n'
        s+='number of word lengths: ' + str(len(self.word_lengths))+'\n'
        s+='number of word stems: ' + str(len(self.stems)) + '\n'
        s+='number of sentence lengths: ' + str(len(self.sentence_lengths)) +'\n'
        s+='number of word suffixes: '+ str(len(self.endings))
        
        return s

    def add_string(self, s):
        """Analyzes the string txt and adds its pieces
           to all of the dictionaries in this text model.
        """
    
        words_list= clean_text(s)

        self.total=len(words_list)
        
        for w in words_list:
            if w not in self.words:
                self.words[w]= 1
            else:
                self.words[w]+= 1

        for w in words_list:
            if len(w) not in self.word_lengths:
                self.word_lengths[len(w)]= 1
            else:
                self.word_lengths[len(w)]+= 1
        
        for w in words_list:
            word_stem=stem(w)
            if word_stem not in self.stems:
                self.stems[word_stem]= 1
            else:
                self.stems[word_stem]+= 1

        for w in words_list:
            end=ending(w)
            if end != None:                
                if end not in self.endings:
                    self.endings[end]=1
                else:
                    self.endings[end]+=1

        count=0
        for r in s:
            if r ==' ':
                count +=1
            if r in '.!?':
                count+=1
                if count not in self.sentence_lengths:
                    self.sentence_lengths[count]=1
                else:
                    self.sentence_lengths[count]+=1
                count=0

         
            
    def add_file(self, filename):
        """Adds text from a file"""
        f = open(filename, 'r', encoding='utf8', errors='ignore')
        s = f.read()        
        self.add_string(s)


    def save_model(self):
        """saves an object self by writing its various feature dictionaries to
           files
        """
        filename=self.name + '_words'
        file_write(filename, self.words)

        filename2=self.name+'_word_lengths'
        file_write(filename2, self.word_lengths)

        filename3=self.name+'_stems'
        file_write(filename3, self.stems)

        filename4=self.sentence_lengths+'_sentence_lengths'
        file_write(filename4, self.sentence_lengths)

        filename5= self.endings+'_endings'
        file_write(filename5, self.endings)

     
    def read_model(self):
        """reads the stored dictionaries for the called file"""
        filename=self.name + '_words'
        self.words=file_read(filename)

        filename2= self.name+'_word_lengths'
        self.word_lengths=file_read(filename2)

        filename3=self.name+'_stems'
        self.stems=file_read(filename3)

        filename4=self.sentence_lengths+'_sentence_lengths'
        self.setence_lengths=file_read(filename4)

        filename5= self.endings+'_endings'
        self.endings=file_read(filename5)

    def similarity_scores(self, other):
        """returns a list of the similarities scores of all elements"""
        results = []

        words_score=compare_dictionaries(other.words, self.words)
        wordl_score=compare_dictionaries(other.word_lengths, self.word_lengths)
        stems_score=compare_dictionaries(other.stems, self.stems)
        sentl_score=compare_dictionaries(other.sentence_lengths, self.sentence_lengths)
        endings_score=compare_dictionaries(other.endings, self.endings)
        results+= [words_score]
        results+= [wordl_score]
        results+= [stems_score]
        results+= [sentl_score]
        results+= [endings_score]
        return results

    def classify(self, source1, source2):
        """compares two text models to see which is most likely the source of
           the called text"""

        scores1 = self.similarity_scores(source1)
        scores2 = self.similarity_scores(source2)
        
        print('scores for ' + source1.name +':' + str(self.similarity_scores(source1)))
        print('scores for ' + source2.name +':' + str(self.similarity_scores(source2)))
        
        source1_score=0
        source2_score=0

        for i in range(len(scores1)):
            if scores1[i]> scores2[i]:
                source1_score+=1
            elif scores2[i]>scores1[i]:
                source2_score+=1
                
        if source1_score > source2_score:
            win=source1.name
        else:
            win=source2.name

        print(self.name + ' is more likely to have come from ' + win)

        
def file_write(filename, dic):
    """A function that writes a Python dictionary to an easily-readable file.
    """
    d = dic 
    f = open(filename, 'w')      
    f.write(str(d))
    f.close()
    
def file_read(filename):
    """A function that reads a Python dictionary from a file.
    """
    f = open(filename, 'r')    
    d_str = f.read()      
    f.close()

    d = dict(eval(d_str))
    return d
      
            
def clean_text(txt):
    """cleans a string so that it does not have any punctuation or special
       characters
    """

    alphabet= 'abcdefghijklmnopqrstuvwxyz '

    ALPHABET= 'ABCDEFGHIJKLMNOPQRSTUVWXYZ '

    new_words=''
    
    for i in txt:
        if i in alphabet or i in ALPHABET:
            new_words+= i

    clean=new_words.lower().split()

    return clean
    

def stem(s):
    """Returns the stem of the given string"""
    if len(s)>4:
        if s[-4:] in 'able ency ship':
            s = s[:-4]
        elif s[-3:] in 'ing ily ies':
         
            if s[-3:] == 'ing':
                s = s[:-3]
            else:
                s = s[:-3] + 'y'
     
        
        elif s[-2:] in 'ed er es ly':
           s = s[:-2]
           if s[-1]=='i':
               s=s[:-1] + 'y'


        elif s[-1] in 's':
            s = s[:-1]

        if s[-1] == 's' or s[-2:] == 'ed' or s[-2:] == 'er' or s[-2:] == 'es' \
           or s[-2:] == 'ly' or s[-3:]=='ing' or s[-3:]=='ily' or s[-3:]=='ies'\
           or s[-4:] == 'able' or s[-4:] == 'ency' or s[-4:] == 'ship':
            stem_rest= stem(s)
        else:
            stem_rest=s

        return stem_rest
    else:
        return s

def ending(s):
    """checks for a suffix and returns it"""
    if len(s) > 4:
        if s[-2:] == 'ed':
            return 'ed'

        elif s[-2:] == 'er':
            return 'er'

        elif s[-3:]=='ing':
            return 'ing'

        elif s[-3:]=='ily':
            return 'ily'
            
        elif s[-2:] == 'ly':
            return 'ly'
            
        elif s[-3:]=='ies':
            return 'ies'
        
        elif s[-2:] == 'es':
            return 'es'
            
        elif s[-4:] == 'able':
            return 'able'

        elif s[-4:] == 'ency':
            return 'ency'

        elif s[-4:] == 'ship':
            return 'ship'

        elif s[-1] == 's':
            return 's'


            
def compare_dictionaries(d1, d2):
    """compares two dictionaries"""
    score=0
    total=0
 
    for x in d1:
        total+= d1[x]
    
    for c in d2:
        if c in d1:
            score+= d2[c] * math.log(d1[c]/total)
        else:
            score+= d2[c] * math.log(0.5/total)
    return round(score, 3)



def test():
    """ tests multiple different tests to see coorelation between documents """
    source1 = TextModel('source1')
    source1.add_string('It is interesting that she is interested.')

    source2 = TextModel('source2')
    source2.add_string('I am very, very excited about this!')

    mystery = TextModel('mystery')
    mystery.add_string('Is he interested? No, but I am.')
    mystery.classify(source1, source2)


    
def run_tests():
    """ runs tests so see coorelation between documents """
    source1 = TextModel('prep')
    source1.add_file('source_model_1.txt')
    
    source2 = TextModel('athletes')
    source2.add_file('source_model_2.txt')

    new1 = TextModel('my_writing')
    new1.add_file('my_writing.txt')
    new1.classify(source1, source2)

    # Add code for three other new models below.

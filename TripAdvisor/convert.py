import json
import os 
import emoji

class review_info:
    def __init__(self,name):
        self.name = name
        self.count = 1
        self.grades = [0,0,0,0,0] # 1,2,3,4,5
        self.likes = [0,0,0,0,0,0,0] #0,1,2,3,4,5,>5
        self.comment_length = [0,0,0,0,0]  #(0,100],(100,200],(200,300],(300,400],>400

    def parser(self,t):
        text = '"'+str(self.count)+'","'+t['Comment'].replace('"', '') +'"'
        text = text.replace("\n","")
        text += '\n'
        text = emoji.replace_emoji(text, replace='')
        return text
    
    def grades_decide(self,t):
        grade = int(t['Grades'])
        self.grades[grade-1] += 1
    
    def likes_decide(self,t):
        likes = int(t['Likes'].rstrip(' '))
        if likes <= 5:
            self.likes[likes] += 1
        else:
            self.likes[6] += 1
    
    def comment_length_decide(self,t):
        length = len(t['Comment'])
        if length > 0 and length <= 100:
            self.comment_length[0] += 1
        elif length > 100 and length <= 200:
            self.comment_length[1] += 1
        elif length > 200 and length <= 300:
            self.comment_length[2] += 1
        elif length > 300 and length <= 400:
            self.comment_length[3] += 1
        elif length > 400:
            self.comment_length[4] += 1

    def get_percent(self):
        self.grades_percent = [i/sum(self.grades) for i in self.grades]
        #print(self.grades_percent)
        self.comment_length_percent = [i/sum(self.comment_length) for i in self.comment_length]
        #print(self.comment_length_percent)
        self.likes_percent = [i/sum(self.likes) for i in self.likes]
        #print(self.likes_percent)

    def process(self,f,t):
        f.write(self.parser(t))
        self.count += 1
        self.grades_decide(t)
        self.likes_decide(t)
        self.comment_length_decide(t)
        

def write(mobile,not_mobile):
    with open("result.txt","w",encoding='utf-8') as f:
        f.write("#################################################################\n")
        temp = [mobile.count/(mobile.count+not_mobile.count),not_mobile.count/(mobile.count+not_mobile.count)]
        f.write("Whether Mobiles or Not Mobiles:\nYES\t{}\t{:.2%}\nNO\t{}\t{:.2%}\n".format(mobile.count,temp[0],not_mobile.count,temp[1]))
        f.write("#################################################################\n")
        f.write("How many Grades users gave:\n")
        f.write("-----------------------------------------------------------------\n")
        f.write("Mobile:\n")
        temp = [i/sum(mobile.grades) for i in mobile.grades]
        f.write("1\t{}\t{:.2%}\n2\t{}\t{:.2%}\n3\t{}\t{:.2%}\n4\t{}\t{:.2%}\n5\t{}\t{:.2%}\n".format(mobile.grades[0],mobile.grades_percent[0],mobile.grades[1],mobile.grades_percent[1],mobile.grades[2],mobile.grades_percent[2],mobile.grades[3],mobile.grades_percent[3],mobile.grades[4],mobile.grades_percent[4]))
        f.write("-----------------------------------------------------------------\n")
        f.write("Not_Mobile:\n")
        f.write("1\t{}\t{:.2%}\n2\t{}\t{:.2%}\n3\t{}\t{:.2%}\n4\t{}\t{:.2%}\n5\t{}\t{:.2%}\n".format(not_mobile.grades[0],not_mobile.grades_percent[0],not_mobile.grades[1],not_mobile.grades_percent[1],not_mobile.grades[2],not_mobile.grades_percent[2],not_mobile.grades[3],not_mobile.grades_percent[3],not_mobile.grades[4],not_mobile.grades_percent[4]))
        f.write("#################################################################\n")
        f.write("How many likes a review has recieved:\n")
        f.write("-----------------------------------------------------------------\n")
        f.write("Mobile:\n")
        f.write("0\t{}\t{:.2%}\n1\t{}\t{:.2%}\n2\t{}\t{:.2%}\n3\t{}\t{:.2%}\n4\t{}\t{:.2%}\n5\t{}\t{:.2%}\n>5\t{}\t{:.2%}\n".format(mobile.likes[0],mobile.likes_percent[0],mobile.likes[1],mobile.likes_percent[1],mobile.likes[2],mobile.likes_percent[2],mobile.likes[3],mobile.likes_percent[3],mobile.likes[4],mobile.likes_percent[4],mobile.likes[5],mobile.likes_percent[5],mobile.likes[6],mobile.likes_percent[6]))
        f.write("-----------------------------------------------------------------\n")
        f.write("Not_Mobile:\n")
        f.write("0\t{}\t{:.2%}\n1\t{}\t{:.2%}\n2\t{}\t{:.2%}\n3\t{}\t{:.2%}\n4\t{}\t{:.2%}\n5\t{}\t{:.2%}\n>5\t{}\t{:.2%}\n".format(not_mobile.likes[0],not_mobile.likes_percent[0],not_mobile.likes[1],not_mobile.likes_percent[1],not_mobile.likes[2],not_mobile.likes_percent[2],not_mobile.likes[3],not_mobile.likes_percent[3],not_mobile.likes[4],not_mobile.likes_percent[4],not_mobile.likes[5],not_mobile.likes_percent[5],not_mobile.likes[6],not_mobile.likes_percent[6]))
        f.write("#################################################################\n")
        f.write("The length of reviews (# of characters):\n")
        f.write("-----------------------------------------------------------------\n")
        f.write("Mobile:\n")
        f.write("(0,100]\t{}\t{:.2%}\n(100,200]\t{}\t{:.2%}\n(200,300]\t{}\t{:.2%}\n(300,400]\t{}\t{:.2%}\n>400\t{}\t{:.2%}\n".format(mobile.comment_length[0],mobile.comment_length_percent[0],mobile.comment_length[1],mobile.comment_length_percent[1],mobile.comment_length[2],mobile.comment_length_percent[2],mobile.comment_length[3],mobile.comment_length_percent[3],mobile.comment_length[4],mobile.comment_length_percent[4]))
        f.write("-----------------------------------------------------------------\n")
        f.write("Not_Mobile:\n")
        f.write("(0,100]\t{}\t{:.2%}\n(100,200]\t{}\t{:.2%}\n(200,300]\t{}\t{:.2%}\n(300,400]\t{}\t{:.2%}\n>400\t{}\t{:.2%}\n".format(not_mobile.comment_length[0],not_mobile.comment_length_percent[0],not_mobile.comment_length[1],not_mobile.comment_length_percent[1],not_mobile.comment_length[2],not_mobile.comment_length_percent[2],not_mobile.comment_length[3],not_mobile.comment_length_percent[3],not_mobile.comment_length[4],not_mobile.comment_length_percent[4]))
        #print(not_mobile.comment_length_percent[4])
        
def convert():
    mobile = review_info("Mobile")
    not_mobile = review_info("NotMobile")
    with open('Mobile.csv','w',encoding='utf-8') as f:
        with open('NotMobile.csv','w',encoding='utf-8') as nf:
            f.write('"","documents"\n')
            nf.write('"","documents"\n')
            for filename in os.listdir('./jsons'):
                if "json" in filename:
                    #print(filename)
                    with open('./jsons/' + filename, 'r', encoding='utf-8') as fjson:
                        data = json.load(fjson)
                    for t in data:
                        if t['ViaMobiles'] == "True":
                            mobile.process(f,t)
                        elif t['ViaMobiles'] == "False":
                            not_mobile.process(nf,t)
                else:
                    pass
    mobile.get_percent()
    not_mobile.get_percent()
    #print(mobile.grades)
    write(mobile,not_mobile)

if __name__ == '__main__':
    convert()


"""
f.write('"","ReviewerName","ReviewerBadge","Grades","RatingDate","VisitDate","Likes","ViaMobiles","Title","documents","Restaurant"\n')
text = '"'+str(count)+'","'+t['ReviewerName']+'","'+t['ReviewerBadge']+'",'+t['Grades']+',"'+t['RatingDate']+'","'+t['VisitDate'] + '",' + t['Likes'].strip(' ')+',"'+t['ViaMobiles']+'","' + t['Title'].replace('"', '')+'","' +  t['Comment'].replace('"', '') + '","' + filename.strip(".json") + '"'
"""
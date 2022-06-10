def find_dup(filename):
    with open(filename,'r',encoding="utf-8") as f:
        existed_topics = []
        duplicate_topics = []
        contents = f.readlines()
        for content in contents:
            content = content.strip("\n")
            topics = content.split(",")
            for topic in topics:
                topic = topic.strip()
                if topic not in existed_topics:
                    existed_topics.append(topic)
                else:
                    if topic not in duplicate_topics:
                        duplicate_topics.append(topic)
    print(duplicate_topics)
    with open("./dup_topics.txt","w",encoding='utf-8') as f:
        for topic in duplicate_topics:
            f.write("\"" + topic + "\",")
        #print(duplicate_topics)  
    
if __name__ == '__main__':
    filename = "./in.txt"
    find_dup(filename)
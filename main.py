import math
import os
import re
import csv

def classify_nb():
    truepos = 0
    trueneg = 0
    falsepos = 0
    falseneg = 0
    pos_likelihood = {}
    neg_likelihood = {}

    f = open("pos.csv")
    for key, val in csv.reader(f):
        pos_likelihood[key] = float(val)
    f.close()

    f = open("neg.csv")
    for key, val in csv.reader(f):
        neg_likelihood[key] = float(val)
    f.close()

    for mode in ("neg", "pos"):
        filepath = "aclImdb/test/" + mode + "/"
        for file in sorted(os.listdir(filepath),
               key=lambda x: (int(re.sub('\D(.*)', '', x)), x)):
            document = open(filepath+file, encoding='UTF-8')

            words = re.sub("(<.*?>|[^a-zA-Z'])+", ' ', document.readline()).lower()
            words = words.split()
            #words = document.read().split()
            new_words = []
            for word in words:
                if word in pos_likelihood.keys():
                    new_words.append(word)

            pos_score = 0
            neg_score = 0
            for word in new_words:
                pos_score += pos_likelihood[word]
                neg_score += neg_likelihood[word]

            print("pos: "+str(pos_score), "neg: "+str(neg_score))
            if pos_score > neg_score:
                if mode == "pos":
                    truepos+=1
                else:
                    falsepos+=1
            else:
                if mode == "pos":
                    falseneg+=1
                else:
                    trueneg+=1
    print("total: "+str(25000))
    print("processed: "+str(trueneg+truepos+falseneg+falsepos))
    print("acc: "+str((trueneg+truepos)/(trueneg+truepos+falseneg+falsepos)))
    print("precision: "+str(truepos/(truepos+falsepos)))
    print("recall: "+str(truepos/(truepos+falseneg)))
    return


def train_nb():
    pos_counts = {}
    neg_counts = {}

    for mode in ("neg", "pos"):
        filepath = "aclImdb/train/" + mode
        for file in sorted(os.listdir(filepath),
                           key=lambda x: (int(re.sub('\D(.*)', '', x)), x)):
            f = open(filepath + '/' + file, encoding='UTF-8')
            print(filepath+file)
            words = re.sub("(<.*?>|[^a-zA-Z'])+", ' ', f.readline()).lower()
            words = words.split()
            for word in words:
                if word not in pos_counts:
                    pos_counts[word] = 1
                if word not in neg_counts:
                    neg_counts[word] = 1

                if mode == "pos":
                    pos_counts[word] += 1
                elif mode == "neg":
                    neg_counts[word] += 1

            # print(words)
            f.close()

    pos_likelihood = dict(map(lambda t: (t[0], math.log(t[1]/ len(pos_counts))), pos_counts.items()))
    neg_likelihood = dict(map(lambda t: (t[0], math.log(t[1]/ len(neg_counts))), neg_counts.items()))

    f = open("pos.csv", "w", newline="")
    w = csv.writer(f)
    for key, val in pos_likelihood.items():
        w.writerow([key, val])
    f.close()

    f = open("neg.csv", "w", newline="")
    w = csv.writer(f)
    for key, val in neg_likelihood.items():
        w.writerow([key, val])
    f.close()

    # print(len(vocab))
    # print(len(neg_counts))
    # print(len(pos_counts))
    # print(pos_likelihood)
    # print(neg_likelihood)
    #print(vocab - word_list)

if __name__ == "__main__":
    #train_nb()
    classify_nb()


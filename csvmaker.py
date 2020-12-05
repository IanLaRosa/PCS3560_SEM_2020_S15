import csv, os, re
from os import listdir

def text_treatment(test_str):
    ret = ''
    skip1c = 0
    skip2c = 0
    for i in test_str:
        if i == '[':
            skip1c += 1
        elif i == '(':
            skip2c += 1
        elif i == ']' and skip1c > 0:
            skip1c -= 1
        elif i == ')'and skip2c > 0:
            skip2c -= 1
        elif skip1c == 0 and skip2c == 0:
            ret += i
    ret = ret.replace('\"','').replace('“','').replace('ʽ','').replace('ʼ','').replace('”','').replace('?','').replace('!','').replace('\'','').replace('*','').replace('\n', ' ')
    temp_list = list(ret.split())
    temp_list = [x for x in temp_list if "http" not in x and "www" not in x and ".com" not in x and ".br" not in x]
    ret = ' '.join(temp_list)
    ret = re.sub(r"(?<!\d)\.(?!\d)", ' . ', ret)
    ret = ret.replace(',',' , ').replace(':','')
    if not ret.endswith('.') or not ret.endswith(' . '):
        ret = ret + ' . '
    return ret

text_files_dir = os.getcwd() + '\\artigos'
raw_text_files = [f for f in listdir(text_files_dir)]

sentence_counter = 1
word_list = []
sentence_count_list = []

for text_file in raw_text_files :
    with open(text_files_dir +'\\'+ text_file,'r', encoding='utf-8', errors='ignore') as file:
        word_list.extend(list(text_treatment(file.read()).split()))

word_list = list(filter(None, word_list))
word_list = [v for i, v in enumerate(word_list) if i == 0 or (v != word_list[i-1] or v != '.')]

for word in word_list :
    sentence_count_list.append(sentence_counter)
    if word == '.' :
        sentence_counter += 1

text_file = open(os.getcwd() + '\\ner_dataset3.txt',"w", encoding="utf-8")
for i in range(len(word_list)) :
    text_file.write(str(sentence_count_list[i])+';'+str(word_list[i])+';0'+'\n')
text_file.flush()
text_file.close()
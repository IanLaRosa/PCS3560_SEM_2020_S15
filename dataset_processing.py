import csv, os, re, sys
from os import listdir

text_files_dir = os.getcwd()
text_file_raw = 'ner_dataset3_RAW_COMB2.txt'
text_file_cooked = 'ner_dataset_final_v2.txt'
raw_lines = []
with open(text_files_dir +'\\'+ text_file_raw,'r', encoding='utf-8', errors='ignore') as file:
    raw_lines = file.readlines()
    print('\nFile : ' + text_file_raw +'\nRead ' + str(len(raw_lines)) + ' lines')

cooked_lines = []
i = 1
seq_num_offset = 0
set_tags = []
temp = []
try:
    for line in raw_lines:
        line = line.replace(';;',';')
        temp = line.split(';')
        # seq_num = temp[0]
        # text = temp[1]
        # tag = temp[2]
        seq_num , text , tag = line.split(';')
        temp_tag = tag[:-1]
        if temp_tag == '041' or temp_tag == '031' or temp_tag == '047' or temp_tag == '032' or temp_tag == '043' or temp_tag == '045' or temp_tag == '067':
            tag = tag[:-2] + tag[3]
        seq_num = str(int(seq_num) + seq_num_offset)
        if 'i' in tag:
            print(line + ' IGNORED----')
            seq_num_offset = seq_num_offset - 1
            continue
        if not tag.startswith('0') or tag.endswith('0') or len(tag) == 1:
            raise Exception(line + "TAG DOES NOT START WITH 0 OR ENDS WITH 0 OR TAG LEN 1")
        if text == '-':
            print(line + ' -> ONLY HIFEN')
            text = ','
        if text.startswith('-'):
            print(line + ' -> STARTS WITH HIFEN')
            text = text[1:]
            cooked_lines.append(seq_num + ';,;0')
        if text.endswith('-'):
            print(line + ' -> ENDS WITH HIFEN')
            text = text[:-1]
            cooked_lines.append(seq_num + ';' + text + ';' + tag)
            cooked_lines.append(seq_num + ';,;0')
        elif text != '.' and text.endswith('.'):
            print(line + ' -> ENDS WITH PERIOD ')
            text = text[:-1]
            cooked_lines.append(seq_num + ';' + text + ';' + tag)
            seq_num_offset = seq_num_offset + 1
            seq_num = str(int(seq_num) + 1)
            cooked_lines.append(seq_num + ';.;0')
        elif text != ',' and text.endswith(','):
            print(line + ' -> ENDS WITH COMMA ')
            text = text[:-1]
            cooked_lines.append(seq_num + ';' + text + ';' + tag)
            cooked_lines.append(seq_num + ';,;0')
        else:
            cooked_lines.append(seq_num + ';' + text + ';' + tag)
        if tag not in set_tags:
            set_tags.append(tag)
        i = i + 1
except Exception as err:
    
    print('\n\n' + str(i) + ' ERROR ' + raw_lines[i-1])
    print(temp)
    print('line = ' + line)
    print('\n Error: \n ' + str(err))

temp_lines = []
actual_seq = '1'
seq_old = '1'
for line in cooked_lines:
    seq_num , text , tag = line.split(';')
    if seq_num != seq_old:
        seq_old = seq_num
        actual_seq = str(int(actual_seq) + 1)
    #if text != 'e' and text != 'E' and text != ',':
    temp_lines.append(actual_seq + ';' + text + ';' + tag)
        
cooked_lines = temp_lines

print(set_tags)
print(len(cooked_lines))

with open(text_files_dir +'\\'+ text_file_cooked,'w', encoding='utf-8', errors='ignore') as file:
    for line in cooked_lines:
        if not line.endswith('\n'):
            file.write("%s\n" % line)
        else:
            file.write("%s" % line)

with open(text_files_dir +'\\'+ text_file_cooked,'r', encoding='utf-8', errors='ignore') as file:
    validate_lines = file.readlines()
    for line in validate_lines:
        x, y, z = line.split(';')


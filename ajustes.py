import csv, os, re, sys
from os import listdir

text_files_dir = os.getcwd()
text_file_raw = 'ner_dataset_final_v2.txt'
text_file_cooked = 'ner_dataset_final_v3.txt'
raw_lines = []
with open(text_files_dir +'\\'+ text_file_raw,'r', encoding='utf-8', errors='ignore') as file:
    raw_lines = file.readlines()
    print('\nFile : ' + text_file_raw +'\nRead ' + str(len(raw_lines)) + ' lines')

cooked_lines = []
seq_antigo = "1"
len_atual = 0
set_tags = []
temp = []
len_dict = {}
seq_dict = {}
i = 1

seq_delta = 0
print('BEFORE LEN ' + str(len(raw_lines)))

for line in raw_lines:
    seq_num , text , tag = line.split(';')
    seq_num = str( int(seq_num) + seq_delta)
    if text.endswith('.') and text != '.':
        print('BREAK ' + seq_num)
        text = text[:-1]
        cooked_lines.append(seq_num + ';' + text + ';' + tag)
        cooked_lines.append(seq_num + ';' + '.' + ';' + tag)
        seq_delta = seq_delta + 1
    else:
        cooked_lines.append(seq_num + ';' + text + ';' + tag)

print('AFTER LEN ' + str(len(cooked_lines)))

try:
    for line in cooked_lines:
        seq_num , text , tag = line.split(';')
        if seq_num == seq_antigo:
            len_atual = len_atual + 1
        else:
            if len_atual not in len_dict.keys():
                len_dict[len_atual] = 1
                seq_dict[len_atual] = [seq_antigo]
            else:
                len_dict[len_atual] = len_dict[len_atual] + 1
                seq_dict[len_atual].append(seq_antigo)
            len_atual = 1
            seq_antigo = seq_num
        i = i + 1
except Exception as err:
    
    print(str(i) + ' ERROR ' + cooked_lines[i-1])
    print(temp)
    print('\n Error: \n ' + str(err))

print('Dict Length :' + str(len(len_dict.keys())))

keyset = list(len_dict.keys())
keyset.sort(reverse=True)

for key in keyset:
    seqs = ''
    i = 0
    for seq in seq_dict[key]:
        seqs = seqs + seq + '  '
        if i == 10:
            break
        i = i + 1
    print(str(key) + ' -> ' + str(len_dict[key]) + ' : ' + seqs)

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


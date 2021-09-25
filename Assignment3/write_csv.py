import os
import csv

with open('GA_Results.csv', mode='a', newline='', encoding='utf-8') as csvf:
    csv_writer = csv.writer(csvf, delimiter=',',
                            quotechar='"', quoting=csv.QUOTE_MINIMAL)
    csv_writer.writerow(['group', 'n', 'weight', 'value', 'item'])
def EDA(lines):
    n_arr,weights_arr,values_arr,item_arr,group_arr=[],[],[],[],[]
    for i in range(0,len(lines)):
        index=i+1

        if index%5==2:
            n = ""
            for j in range(6,len(lines[i])):
                char=lines[i][j]
                if char >='0' and char<='9':
                    n+=char
                else:
                    break
            n_arr.append(int(n))
        if index%5==3:
            values=lines[i][14:]
            values_arr.append(int(values))
        if index%5==4:
            weights=lines[i][15:]
            weights_arr.append(int(weights))
        if index%5==0:
            item=lines[i][21:]
            item_arr.append(int(item))
        if index%5==1:
            group=lines[i].split('/')[2]
            group_arr.append(group)
    return n_arr,weights_arr,values_arr,item_arr,group_arr



for file in os.listdir('_GA_Results'):
    print(file)
    with open('_GA_Results'+'/'+file) as f:
        print(file)
        lines=f.readlines()
        lines = map(lambda s: s.replace('\n', ''), lines)
        lines = filter(lambda s: s != '', lines)
        lines = list(lines)
        print(lines)
    n_arr,weights_arr,values_arr,item_arr,group_arr=EDA(lines)
    with open('GA_Results.csv', mode='a', newline='', encoding='utf-8') as csvf:
        csv_writer = csv.writer(csvf, delimiter=',',
                                quotechar='"', quoting=csv.QUOTE_MINIMAL)

        for i in range(len(n_arr)):
            row=[group_arr[i],n_arr[i],weights_arr[i],values_arr[i],item_arr[i]]
            csv_writer.writerow(row)


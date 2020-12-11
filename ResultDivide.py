import os

folder_dir = 'results/'

file_count = 0
file_no = 0
for src_dir in os.listdir(folder_dir):
    print(src_dir)

    if '.txt' in src_dir:
        fr = open(folder_dir + src_dir, 'r', encoding='utf-8')
        for user_id in fr:
            file_count += 1
            if file_count == 1000:
                file_count = 0
                file_no += 1
            fw = open('results/validusers/user_list_'+str(file_no)+'.txt', 'a', encoding='utf-8')
            fw.write(user_id[:17]+'\n')
            fw.close()
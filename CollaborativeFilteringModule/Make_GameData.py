import os


src_dir = '../SteamDataCrawlingModule/results/userdata/'

game_src_dir = '../SteamDataCrawlingModule/results/GameData/'

file_list = os.listdir(src_dir)


game_dic = dict()

for i in file_list :

    file_dir = src_dir + i

    f = open(file_dir,'r',encoding='utf-8')
    game_flag = False
    for row in f :
        if row == '@@GAME\n' :
            game_flag = True
            continue
        if row == '@@REVIEW\n' :
            game_flag = False
            continue

        if game_flag :
            temp = row.split('##')
            game_score = 0
            tags = []
            try :
                a = open(game_src_dir + temp[0]+'.txt','r',encoding='utf-8')
                for row2 in a :
                    if '@@Total Review' in row2 :
                        temp2 = row2.split('##')
                        game_score = temp2[1]
                    if '@@Tags' in row2 :
                        temp2 = row2.split('##')
                        for tag_it in range(1,len(temp2)) :
                            tags.append(temp2[tag_it])
                        
            except :
                pass


            if temp[0] not in game_dic.keys() :
                if int(temp[2]) > 0 :
                    game_dic[temp[0]] = [temp[1],int(temp[2]),1,game_score,tags]
            else :
                if int(temp[2]) > 0 :
                    game_dic[temp[0]][1] += int(temp[2])
                    game_dic[temp[0]][2] +=1
    f.close()


game_ids = game_dic.keys()

print(game_dic)


f = open('gamedata.txt','w',encoding='utf-8')
total_score = 0
total_count = 0
for game_id in game_ids :
    
    total_score += int(game_dic[game_id][3])

    if int(game_dic[game_id][3]) != 0 :
        total_count +=1



for game_id in game_ids :
    data = game_id + '##'+game_dic[game_id][0]+'##'
    if int(game_dic[game_id][3]) != 0 :
        avg = str(game_dic[game_id][1]/game_dic[game_id][2]) +'##' + str(game_dic[game_id][3])+'##'
    else :
        avg = str(game_dic[game_id][1]/game_dic[game_id][2]) +'##' + str(total_score/total_count)+'##'
    tag = ''
    if game_dic[game_id][4] :
        for i in range(len(game_dic[game_id][4])) :
            if i == len(game_dic[game_id][4]) -1 :
                tag += str(game_dic[game_id][4][i])
            else :
                tag += str(game_dic[game_id][4][i]) + '$$'
    else :
        tag +='\n'
    
    f.write(data + avg+ tag )
#281990
f.close()

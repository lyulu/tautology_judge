wff = input("論理式を入れてください。") # 命題記号はAから順に、 ()を用いて優先順位をわかりやすく。¬だけにも()を使う。余計な()は用いない。
# 例：(A→B)→((¬B)→(¬A)), ((A∧B)→C)→((A→C)∨(B→C)), (×∧A)→((C∨D)∨(¬B))
nwff = 0 # 使われている文字の個数（A〜Z）
ntree = 0 # 使うbool値の数
floor = 0 # ()の個数管理、木の深さ
contradiction = 0
tmpprocess = [] # 記号の処理順
process = [] # 処理順
tautology = True
for i in range(len(wff)): # wffは入力した論理式の文字列
    if wff[i] >= "A" and wff[i] <= "Z": # 論理式のi文字目が命題記号であった場合
        nwff = max(nwff, ord(wff[i]) - ord("A") + 1) # 命題記号の種類数(nwff)の把握
        process.append([ntree, ord(wff[i]) - ord("A")]) # 命題記号の位置と種類の記録
        ntree += 1 # 木構造の頂点数(ntree)の把握
    elif wff[i] == "(":
        floor += 1 # 木構造の深さ(floor)の把握
    elif wff[i] == ")":
        floor -= 1 # 木構造の深さ(floor)の把握
    elif wff[i] == "×": # 論理式のi文字目が矛盾記号であった場合
        process.append([ntree]) # 矛盾記号の位置の記録
        ntree += 1 # 木構造の頂点数(ntree)の把握
    else: # 論理式のi文字目が論理演算子であった場合
        tmpprocess.append([floor, ntree, i])
        ntree += 1 # 木構造の頂点数(ntree)の把握
for i in range(len(tmpprocess)):
    tmpfloor = tmpprocess[i][0] # 現在みている論理演算子の深さ
    tmpplace = tmpprocess[i][1] # 現在みている論理演算子の位置
    tmpx = tmpprocess[i][2] # 現在みている論理演算子の文字列中での位置
    tmpleft = 0 # 現在みている論理演算子の左側の子の位置 ¬の場合は無視
    tmpright = 0 # 現在みている論理演算子の右側の子の位置
    if wff[tmpx] != "¬": # tmpleftを求める
        if (wff[tmpx-1] >= "A" and wff[tmpx-1] <= "Z") or wff[tmpx-1] == "×":
            tmpleft = tmpplace - 1
        else:
            j = i - 1
            while j >= 0:
                if len(tmpprocess[j]) != 2 and tmpprocess[j][0] == tmpfloor + 1:
                    tmpleft = tmpprocess[j][1]
                    break
                else:
                    j -= 1
    if (wff[tmpx+1] >= "A" and wff[tmpx+1] <= "Z") or wff[tmpx+1] == "×": # tmprightを求める
        tmpright = tmpplace + 1
    else:
        j = i + 1
        while j < len(tmpprocess):
            if len(tmpprocess[j]) != 2 and tmpprocess[j][0] == tmpfloor + 1:
                tmpright = tmpprocess[j][1]
                break
            else:
                j += 1
    tmpprocess[i] = [tmpfloor, tmpplace, tmpleft, tmpright, tmpx] # 記録
tmpprocess.sort()
tmpprocess.reverse() # ここの2行で論理演算子を深い順に並べる
for i in range(len(tmpprocess)):
    process.append(tmpprocess[i]) # 先に全ての命題記号が入れられ真理表の各場合わけによって真偽値を順番に当てはめる その後論理演算子により順番に演算 processはその記録

# bit全探索で解く
for i in range(2**nwff):
    makearray = i
    tmparray = [False]
    wfftree = []
    for j in range(nwff):
        if makearray % 2 == 1:
            tmparray.append(True)
        else:
            tmparray.append(False)
        makearray //= 2
    for j in range(ntree):
        wfftree.append(True)
    for j in range(ntree):
        if len(process[j]) == 1:
            wfftree[process[j][0]] = False
        elif len(process[j]) == 2:
            wfftree[process[j][0]] = tmparray[process[j][1] + 1]
        else:
            tp = process[j][1]
            tl = process[j][2]
            tr = process[j][3]
            tx = process[j][4]
            if wff[tx] == "¬":
                wfftree[tp] = not(wfftree[tr])
            elif wff[tx] == "∧":
                wfftree[tp] = wfftree[tl] and wfftree[tr]
            elif wff[tx] == "∨":
                wfftree[tp] = wfftree[tl] or wfftree[tr]
            elif wff[tx] == "→":
                wfftree[tp] = not(wfftree[tl]) or wfftree[tr]
        if j == ntree - 1 and wfftree[tp] == False:
            autology = False
    if tautology == False:
        break

if tautology:
    print("この論理式はトートロジーです。")
else:
    print("この論理式はトートロジーではありません。")

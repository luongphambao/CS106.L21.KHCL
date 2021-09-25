import sys
import collections
import numpy as np
import heapq
import time
import numpy as np
global posWalls, posGoals
class PriorityQueue:
    """Define a PriorityQueue data structure that will be used"""
    def  __init__(self):
        self.Heap = []
        self.Count = 0
        self.len = 0

    def push(self, item, priority):
        entry = (priority, self.Count, item)
        heapq.heappush(self.Heap, entry)
        self.Count += 1

    def pop(self):
        (_, _, item) = heapq.heappop(self.Heap)
        return item

    def isEmpty(self):
        return len(self.Heap) == 0

"""Load puzzles and define the rules of sokoban"""

def transferToGameState(layout):
    """Transfer the layout of initial puzzle"""
    layout = [x.replace('\n','') for x in layout]
    layout = [','.join(layout[i]) for i in range(len(layout))]
    layout = [x.split(',') for x in layout]
    maxColsNum = max([len(x) for x in layout])
    for irow in range(len(layout)):
        for icol in range(len(layout[irow])):
            if layout[irow][icol] == ' ': layout[irow][icol] = 0   # free space
            elif layout[irow][icol] == '#': layout[irow][icol] = 1 # wall
            elif layout[irow][icol] == '&': layout[irow][icol] = 2 # player
            elif layout[irow][icol] == 'B': layout[irow][icol] = 3 # box
            elif layout[irow][icol] == '.': layout[irow][icol] = 4 # goal
            elif layout[irow][icol] == 'X': layout[irow][icol] = 5 # box on goal
        colsNum = len(layout[irow])
        if colsNum < maxColsNum:
            layout[irow].extend([1 for _ in range(maxColsNum-colsNum)]) 

    # print(layout)
    return np.array(layout)
def transferToGameState2(layout, player_pos):
    """Transfer the layout of initial puzzle"""
    maxColsNum = max([len(x) for x in layout])
    temp = np.ones((len(layout), maxColsNum))
    for i, row in enumerate(layout):
        for j, val in enumerate(row):
            temp[i][j] = layout[i][j]

    temp[player_pos[1]][player_pos[0]] = 2
    return temp

def PosOfPlayer(gameState):
    """Return the position of agent"""
    return tuple(np.argwhere(gameState == 2)[0]) # e.g. (2, 2)

def PosOfBoxes(gameState):
    """Return the positions of boxes"""
    return tuple(tuple(x) for x in np.argwhere((gameState == 3) | (gameState == 5))) # e.g. ((2, 3), (3, 4), (4, 4), (6, 1), (6, 4), (6, 5))

def PosOfWalls(gameState):
    """Return the positions of walls"""
    return tuple(tuple(x) for x in np.argwhere(gameState == 1)) # e.g. like those above

def PosOfGoals(gameState):
    """Return the positions of goals"""
    return tuple(tuple(x) for x in np.argwhere((gameState == 4) | (gameState == 5))) # e.g. like those above

def isEndState(posBox):
    """Check if all boxes are on the goals (i.e. pass the game)"""
    return sorted(posBox) == sorted(posGoals)#kiểm tra các hộp đã vào đúng vị trí hay chưa

def isLegalAction(action, posPlayer, posBox):#kiểm tra hành động di chuyển có đúng hay không
    """Check if the given action is legal"""
    xPlayer, yPlayer = posPlayer#vị trí người chơi
    if action[-1].isupper(): # the move was a push,kiểm tra hành động vừa mới thực hiện
        x1, y1 = xPlayer + 2 * action[0], yPlayer + 2 * action[1]
    else:
        x1, y1 = xPlayer + action[0], yPlayer + action[1]
    return (x1, y1) not in posBox + posWalls #vi tri hop khac voi vi tri Wall sau khi di chuyen

def legalActions(posPlayer, posBox):
    """Return all legal actions for the agent in the current game state"""
    allActions = [[-1,0,'u','U'],[1,0,'d','D'],[0,-1,'l','L'],[0,1,'r','R']]
    xPlayer, yPlayer = posPlayer
    legalActions = []
    for action in allActions:
        x1, y1 = xPlayer + action[0], yPlayer + action[1]
        if (x1, y1) in posBox: # the move was a push
            action.pop(2) # drop the little letter
        else:
            action.pop(3) # drop the upper letter
        if isLegalAction(action, posPlayer, posBox):
            legalActions.append(action)
        else: 
            continue     
    return tuple(tuple(x) for x in legalActions) # e.g. ((0, -1, 'l'), (0, 1, 'R'))

def updateState(posPlayer, posBox, action):
    """Return updated game state after an action is taken"""
    xPlayer, yPlayer = posPlayer # the previous position of player
    newPosPlayer = [xPlayer + action[0], yPlayer + action[1]] # the current position of player
    posBox = [list(x) for x in posBox]
    if action[-1].isupper(): # if pushing, update the position of box
        posBox.remove(newPosPlayer)
        posBox.append([xPlayer + 2 * action[0], yPlayer + 2 * action[1]])
    posBox = tuple(tuple(x) for x in posBox)
    newPosPlayer = tuple(newPosPlayer)
    return newPosPlayer, posBox

def isFailed(posBox):
    """This function used to observe if the state is potentially failed, then prune the search"""
    rotatePattern = [[0,1,2,3,4,5,6,7,8],
                    [2,5,8,1,4,7,0,3,6],
                    [0,1,2,3,4,5,6,7,8][::-1],
                    [2,5,8,1,4,7,0,3,6][::-1]]
    flipPattern = [[2,1,0,5,4,3,8,7,6],
                    [0,3,6,1,4,7,2,5,8],
                    [2,1,0,5,4,3,8,7,6][::-1],
                    [0,3,6,1,4,7,2,5,8][::-1]]
    allPattern = rotatePattern + flipPattern

    for box in posBox:
        if box not in posGoals:
            board = [(box[0] - 1, box[1] - 1), (box[0] - 1, box[1]), (box[0] - 1, box[1] + 1), 
                    (box[0], box[1] - 1), (box[0], box[1]), (box[0], box[1] + 1), 
                    (box[0] + 1, box[1] - 1), (box[0] + 1, box[1]), (box[0] + 1, box[1] + 1)]
            for pattern in allPattern:
                newBoard = [board[i] for i in pattern]
                if newBoard[1] in posWalls and newBoard[5] in posWalls: return True
                elif newBoard[1] in posBox and newBoard[2] in posWalls and newBoard[5] in posWalls: return True
                elif newBoard[1] in posBox and newBoard[2] in posWalls and newBoard[5] in posBox: return True
                elif newBoard[1] in posBox and newBoard[2] in posBox and newBoard[5] in posBox: return True
                elif newBoard[1] in posBox and newBoard[6] in posBox and newBoard[2] in posWalls and newBoard[3] in posWalls and newBoard[8] in posWalls: return True
    return False

"""Implement all approcahes"""

def depthFirstSearch(gameState):
    """Implement depthFirstSearch approach"""
    beginBox = PosOfBoxes(gameState)# vị trí của các hộp
    beginPlayer = PosOfPlayer(gameState)#vị trí của người chơi

    startState = (beginPlayer, beginBox)# trạng thái của bản đồ (lưu trữ các thứ thay đổi beginPlayer,beginBox)
    frontier = collections.deque([[startState]])# store states,tạo hàng đợi frontier với điểm ban đầu trong hàng đợi là trạng thái của trò choi
    exploredSet = set()# tập lưu trữ các điểm đã khám phá (đã được thêm vào đường đi)
    actions = [[0]] # đi tiếp đường đi nên sẽ lưu dưới dạng mảng để dễ truy xuất phần tử
    temp = []
    while frontier:# kiểm tra frontier có rỗng hay không
        node = frontier.pop()#lấy phần tử cuối ra trong mảng và xóa nó khỏi mảng f
        node_action = actions.pop()# lấy hành động cuối trong mảng và xóa nó khỏi mảng
        if isEndState(node[-1][-1]):# nếu trạng thái hiện thại (ứng với node cuối) giống với goalState thì ta sẽ cộng vào temp các action đã đi qua
            temp += node_action[1:]# cộng vào đường đi đã tìm được
            break
        if node[-1] not in exploredSet:# nếu node cuối không nằm trong tập đã đi qua
            exploredSet.add(node[-1])# thêm nó vào
            for action in legalActions(node[-1][0], node[-1][1]):# ứng với các trạng thái
                newPosPlayer, newPosBox = updateState(node[-1][0], node[-1][1], action)# cập nhật trạng thái trò chơi
                if isFailed(newPosBox):#kiểm tra kết quả trò chơi,
                    continue
                frontier.append(node + [(newPosPlayer, newPosBox)])# thêm vị trí mới vào mảng frontier
                actions.append(node_action + [action[-1]])#thêm  hành động đã đi vào mảng action
    return temp

def breadthFirstSearch(gameState):
    """Implement breadthFirstSearch approach"""
    beginBox = PosOfBoxes(gameState)#vị trí của các hộp hiện tại(array)
    beginPlayer = PosOfPlayer(gameState)# vị trí đứng của người chơi

    startState = (beginPlayer, beginBox)  # e.g. ((2, 2), ((2, 3), (3, 4), (4, 4), (6, 1), (6, 4), (6, 5)))#trạng thái của bản đồ
    frontier = collections.deque([[startState]])  # store states,tạo hàng đợi frontier với điểm ban đầu trong hàng đợi là vị trí người chơi
    actions = collections.deque([[0]])  # store actions ,ta xem vị trí ban đầu là trạng thái 0(tượng trưng cho node ban đầu)
    exploredSet = set()# tập các giá trị điểm đã đi qua ,dễ thấy rằng nếu đường đi có sự lặp lại sẽ dẫn đến cây tìm kiếm dài vô hạn
    #từ đó ta sẽ sử dụng set để lưu trữ các điểm đã đi qua(set là một hashtable có thể thay đổi nhưng không lưu chỉ mục và không chấp nhận sự trùng lặp)
    temp=[]# lưu trữ đường đi đúng (trace-back)
    while frontier:
        node = frontier.popleft()#lấy điểm đầu tiên bên trái  trong frontier và xóa nó đi(BFS tìm kiếm từ trái trên phải)
        node_action = actions.popleft()#lấy action đầu tiên bên trái trong action và xóa action đó đi
        if isEndState(node[-1][-1]):# nếu node cuối cùng giống với goal thì ta lấy cộng vào temp đường đi đó
            temp += node_action[1:] # cộng array lưu trữ đường đi
            print('BFS done')
            break
        if node[-1] not in exploredSet:#nếu node  không tồn tại trong tập điểm đã đi thì thêm vào
            exploredSet.add(node[-1])#thêm node[-1] vào đầu exploredSet
            for action in legalActions(node[-1][0], node[-1][1]):# tạo ra tập các đường đi (left,right,top,bottom)
                newPosPlayer, newPosBox = updateState(node[-1][0], node[-1][1], action)#cập nhật tọa độ của Hộp và người chơi( đại lượng thay đổi )
                if isFailed(newPosBox):# nếu vị trí  chiếc hộp đúng
                    continue
                frontier.append(node + [(newPosPlayer, newPosBox)])#thêm vị trí của game( ) vào frontier(khôi phục vị trí của node sau vị trí mới)
                actions.append(node_action + [action[-1]]) #thêm hành động vào action (khôi phục hành động đã loại bỏ)
    return temp
    
def cost(actions):
    """A cost function"""
    return len([str(x) for x in actions if x.islower()])#chi phi di chuyen bang so luong cac phep di chuyen hop le

def uniformCostSearch(gameState):
    """Implement uniformCostSearch approach"""
    beginBox = PosOfBoxes(gameState)  # vị trí của hộp
    beginPlayer = PosOfPlayer(gameState)  # vị trí của player

    startState = (beginPlayer, beginBox)  # trạng thái game
    frontier = PriorityQueue()  # tạo hàng đợi ưu tiên vì ý tưởng của ucs là đi dựa trên việc xếp theo giá trị Cost
    frontier.push([startState], 0)  # chi phí ban đầu là 0(chưa đi)
    exploredSet = set()  # tập các điểm đã đi qua (không  lập lại trong suốt đường đi)
    actions = PriorityQueue()  # tạo hàng đợi hành động
    actions.push([0], 0)  # bắt đầu node 0 với chi phí 0
    temp = []
    ### Implement uniform cost search here
    while frontier:
        node = frontier.pop()  # lấy ra khỏi hàng đợi điểm cuối  và xóa nó
        node_action = actions.pop()  # lấy ra khỏi hàng đợi action cuối  và xóa nó
        if isEndState(node[-1][-1]):  # nếu node cuối có cost=0
            temp += node_action[1:]  # thêm các hành động đã đi của đường đi đó vào temp
            print('UCS Done')
            break
        if node[-1] not in exploredSet:  # nếu node cuối chưa nằm trong tập đã đi
            exploredSet.add(node[-1])  # thêm nó vào tap duong di
            Cost = cost(node_action[1:])# chi phí tính từ ban đầu đến node hiện tại
            for action in legalActions(node[-1][0], node[-1][1]):
                newPosPlayer, newPosBox = updateState(node[-1][0], node[-1][1], action)#cap nhat vi ti nguoi choi va box
                if isFailed(newPosBox):
                    continue
                frontier.push(node + [(newPosPlayer, newPosBox)],Cost)#them vao hang doi frontier chi phi di va node do
                actions.push(node_action + [action[-1]],Cost)#them action ,cost action vao
    return temp
"""Read command"""
def readCommand(argv):
    from optparse import OptionParser
    
    parser = OptionParser()
    parser.add_option('-l', '--level', dest='sokobanLevels',
                      help='level of game to play', default='level6.txt')
    parser.add_option('-m', '--method', dest='agentMethod',
                      help='research method', default='bfs')
    args = dict()
    options, _ = parser.parse_args(argv)
    with open('assets/levels/' + options.sokobanLevels,"r") as f: 
        layout = f.readlines()
    args['layout'] = layout
    args['method'] = options.agentMethod
    return args

def get_move(layout, player_pos, method):
    time_start = time.time()
    global posWalls, posGoals
    # layout, method = readCommand(sys.argv[1:]).values()
    gameState = transferToGameState2(layout, player_pos)
    posWalls = PosOfWalls(gameState)
    posGoals = PosOfGoals(gameState)
    if method == 'dfs':
        result = depthFirstSearch(gameState)
    elif method == 'bfs':
        result = breadthFirstSearch(gameState)    
    elif method == 'ucs':
        result = uniformCostSearch(gameState)
    else:
        raise ValueError('Invalid method.')
    time_end=time.time()
    print('Runtime of %s: %.2f second.' %(method, time_end-time_start))
    print(result)
    return result

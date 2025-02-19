import os
import sys
import keyboard
import beaupy as tui
os.system("")
class col:
 

	reset = '\033[0m'
	bold = '\033[01m'
	disable = '\033[02m'
	underline = '\033[04m'
	reverse = '\033[07m'
	strikethrough = '\033[09m'
	invisible = '\033[08m'
 
	class fg:
		black = '\033[30m'
		red = '\033[31m'
		green = '\033[32m'
		orange = '\033[33m'
		blue = '\033[34m'
		purple = '\033[35m'
		cyan = '\033[36m'
		lightgrey = '\033[37m'
		darkgrey = '\033[90m'
		lightred = '\033[91m'
		lightgreen = '\033[92m'
		yellow = '\033[93m'
		lightblue = '\033[94m'
		pink = '\033[95m'
		lightcyan = '\033[96m'
 
	class bg:
		black = '\033[40m'
		red = '\033[41m'
		green = '\033[42m'
		orange = '\033[43m'
		blue = '\033[44m'
		purple = '\033[45m'
		cyan = '\033[46m'
		lightgrey = '\033[47m'

RoomIdList = []
RoomNameList = []
RoomLocX = []
RoomLocY = []
RoomTextList = []

GameMap = []
LocationRef = []
RoomRef = []
title = ""
cursor = ""
nulltext = ""

global playerY
global playerX
playerX = 0
playerY = 0


global InRoom
InRoom = False




def find_between( s, first, last ):
		try:
			start = s.index( first ) + len( first )
			end = s.index( last, start )
			return s[start:end]
		except ValueError:
			return ""

def Config(line):
	global title
	global GameMap
	global cursor
	global nulltext
	global playerX
	global playerY
	global ExitKey
	global MapNullText
	global Map
	global PlayerRep
	if("(") in line:
		identifier = line.split("(")[0]
		if identifier == "MapSize":
			args = (find_between(line, "(", ")"))
			w = int(args.split(",")[0].strip())
			h = int(args.split(",")[1].strip())
			GameMap = [["0"] * w for _ in range(h)]
		if identifier == "MapNullText":
			args = (find_between(line, "(\"", "\")"))
			MapNullText = args
		if identifier == "MapPlayerText":
			args = (find_between(line, "(\"", "\")"))
			PlayerRep = args
		if identifier == "ShowMap":
			args = (find_between(line, "(", ")"))
			if args == "True":
				Map = True
			if args == "False":
				Map = False

		if identifier == "GameTitle":
			if "\"" in line:
				title = find_between(line, "(\"", "\")")
			elif "'" in line:
				title = find_between(line, "('", "')")

		if identifier == "Cursor":
			if "\"" in line:
				cursor = find_between(line, "(\"", "\")")
			elif "'" in line:
				cursor = find_between(line, "('", "')")
		if identifier == "MakePlayer":
			args = (find_between(line, "(", ")"))
			x = int(args.split(",")[0].strip())
			y = int(args.split(",")[1].strip())
			playerX = x
			playerY = y
			GameMap[y][x] = "Player"
		if identifier == "NullText":
			if "\"" in line:
				nulltext = find_between(line, "(\"", "\")")
			elif "'" in line:
				nulltext = find_between(line, "('", "')")
		if identifier == "ExitKey":
			ExitKey = (find_between(line, "(", ")")).lower()

def MakeRoom(LineList, line):
	inside_room = False
	current_room = ""
	for line in LineList:
		if line.startswith("MakeRoom{"):  
			inside_room = True  
			current_room = ""
		elif inside_room:
			current_room += line + "\n"
			if line.strip() == "}":  
				inside_room = False
				RoomRef.append(current_room)

def InitRoom(FullArgs):
	Arguments = str(FullArgs).splitlines()
	RoomId = Arguments[0].split("=")[1].strip()
	
	RoomLoc = Arguments[1].split("=")[1].strip()
	RoomGreetText = Arguments[2].split("=")[1].strip()

	RoomX = RoomLoc.split(",")[0].strip()
	RoomY = RoomLoc.split(",")[1].strip()

	RoomIdList.append(RoomId)
	
	RoomLocX.append(int(RoomX))
	RoomLocY.append(int(RoomY))
	RoomTextList.append(RoomGreetText.replace("\"", "").strip())
	GetLoc = GameMap[int(RoomY)][int(RoomX)]
	if str(GetLoc) != "Player":
		GameMap[int(RoomY)][int(RoomX)] = RoomId
	else:
		GameMap[int(RoomY)][int(RoomX)] = "Player @ "+RoomId
	
	


FileName = sys.argv[1]
with open(FileName, "r") as f:
	content = f.read()
	f.close()

Lines = content.splitlines()
configFile = Lines[0]
if configFile.startswith("@"):
	File = configFile.split("@")[1].strip()
	
with open(File, "r") as f:
	configContent = f.read()
	f.close()
Lines = configContent.splitlines()

for i, line in enumerate(Lines):
	if line.startswith("MakeRoom{") == False:
		Config(line)
MakeRoom(Lines, line)



for i, room in enumerate(RoomRef):
	InitRoom(room)
	



for num, loc, in enumerate(GameMap[0]):
	LocationRef.append(num)
	


def ShowMap():
	
	for num, loc, in enumerate(GameMap):
		MapLine = "".join(loc).replace("0", MapNullText)
		for i, Name in enumerate(RoomIdList):
			if Name in MapLine:
				MapLine = MapLine.replace(Name, RoomTextList[i])
		print(MapLine.replace("Player", PlayerRep))
		



def Play():
	
	def Code():
		global IdentList
		global OnList
		global ActionList
		global ValList
		global PromptList
		global PromptIdList
		global PromptTextList
		global PromptOptList
		global PromptReturnList
		PromptIdList = []
		PromptTextList = []
		PromptOptList = []
		PromptReturnList = []
		argList = []
		
		IdentList = []
		OnList = []
		ActionList = []
		ValList = []
		PromptList = []

		LineList = content.splitlines()
		inCode = False
		CurrentCode = ""
		for line in LineList:
			if line.startswith("OnEntry") or line.startswith("OnMove"):
				argument = line
				
				inCode = True  
				CurrentCode = ""
			elif inCode:
				CurrentCode += line + "\n"
				if line.strip() == "}":  
					inCode = False
					
					argList.append(argument+CurrentCode)
		for i, item in enumerate(argList):
			Lines = str(item).splitlines()
			Call = Lines[0].split("{")[0].split(".")
			IdentList.append(Call[1])
			OnList.append(Call[0])
			Execute = find_between(item, "{", "}").splitlines()
			toappend = []
			if "prompt(" in item:
				toappend.append("PROMPT")
				promptArgs = find_between(item, "prompt(", ")").splitlines()
				PromptList.append(promptArgs)
			if "write(" in item:
				toappend.append("PRINT")
				value = find_between(item, "write(", ")").splitlines()
				ValList.append(value)
			ActionList.append(toappend)

		
					
				

		

	
	def CheckForRoom():
		global InRoom
		global textToPrint
		textToPrint = ""
		InRoom = False
		for i, item in enumerate(RoomIdList):
			if playerX == RoomLocX[i] and playerY == RoomLocY[i]:
				InRoom = True
				CurRoom = item
				for a, room in enumerate(IdentList):
					if CurRoom == room:
						
						CurAction = ActionList[a]
						
						for b, action in enumerate(CurAction):
							if action == "PROMPT":
								
								
								Code = (PromptList[a])
								
								
								for c, tokens in enumerate(Code):
									if "ID" in tokens:
										IdStatement = tokens.strip()
										PromptId = str(IdStatement).split("=")[1].strip()
										PromptIdList.append(PromptId)
										
									elif "Text" in tokens:
										Text2 = tokens.strip()
										Text2 = str(Text2).split("=")[1].strip()
										PromptTextList.append(Text2)
										
									elif "Options" in tokens:
										Opt = tokens.strip()
										
										Opt = str(Opt).split("=")[1].strip().replace("\"", "").strip().replace("[", "").strip().replace("]", "").strip()
										PromptOptList.append(Opt)
										OptionsForUse = Opt.split(",")
										for num, option in enumerate(OptionsForUse):
											OptionsForUse[num] = option.strip()
									elif "Return" in tokens:
										ret = tokens.strip()
										
										ret = str(ret).split("=")[1].strip().replace("\"", "").strip().replace("[", "").strip().replace("]", "").strip()
										PromptReturnList.append(ret)
										ReturnForUse = ret.split(",")
										for num, returnVals in enumerate(ReturnForUse):
											ReturnForUse[num] = returnVals.strip()
										
										
							elif action == "PRINT":
								textToPrint = "".join(ValList[a]).replace("\"", "").strip()

						if OnList[a] == "OnEntry":
							print(textToPrint)
							print(Text2.replace("\"", ""))
							choice = tui.select(OptionsForUse, cursor=cursor)
							index = (OptionsForUse.index(choice))
							print(ReturnForUse[index])

					
						
							

										
										
				
		if InRoom == False:
			print(nulltext)
		
		
		

	def MovePlayer(dir):
		
		global playerY
		global playerX
		if dir == "up":
			Current = (GameMap[playerY][playerX])
			if playerY-1 < 0:
				MoveTo = (GameMap[playerY][playerX])
				CheckForRoom()
			else:

				try:
					MoveTo = (GameMap[playerY-1][playerX])
					if "@" in Current:
						GameMap[playerY][playerX] = Current.split("@")[1].strip()
					elif Current == "Player":
						GameMap[playerY][playerX] = "0"
					if MoveTo == "0":
						GameMap[playerY-1][playerX] = "Player"
						playerY = playerY-1
						CheckForRoom()
					else:
						GameMap[playerY-1][playerX] = "Player @ "+GameMap[playerY-1][playerX]
						playerY = playerY-1
						CheckForRoom()

				except IndexError:
					(GameMap[playerY][playerX]) = (GameMap[playerY][playerX])
					CheckForRoom()

		elif dir == "down":
			
			Current = (GameMap[playerY][playerX])
			
			try:
				MoveTo = (GameMap[playerY+1][playerX])
				if "@" in Current:
					GameMap[playerY][playerX] = Current.split("@")[1].strip()
				elif Current == "Player":
					GameMap[playerY][playerX] = "0"
				if MoveTo == "0":
					GameMap[playerY+1][playerX] = "Player"
					playerY = playerY+1
					CheckForRoom()
				else:
					GameMap[playerY+1][playerX] = "Player @ "+GameMap[playerY+1][playerX]
					playerY = playerY+1
					CheckForRoom()

			except IndexError:
				(GameMap[playerY][playerX]) = (GameMap[playerY][playerX])
				CheckForRoom()
		
		

			
			
			

		elif dir == "left":
			
			Current = (GameMap[playerY][playerX])
			try:
				if playerX-1 < 0:
					MoveTo = (GameMap[playerY][playerX])
					CheckForRoom()
				else:
					MoveTo = (GameMap[playerY][playerX-1])
					if "@" in Current:
						GameMap[playerY][playerX] = Current.split("@")[1].strip()
					elif Current == "Player":
						GameMap[playerY][playerX] = "0"
					if MoveTo == "0":
						GameMap[playerY][playerX-1] = "Player"
						playerX = playerX-1
						CheckForRoom()
					else:
						GameMap[playerY][playerX-1] = "Player @ "+GameMap[playerY][playerX-1]
						playerX = playerX-1
						CheckForRoom()

			except IndexError:
				(GameMap[playerY][playerX]) = (GameMap[playerY][playerX])
				CheckForRoom()
		
		elif dir == "right":
			
			Current = (GameMap[playerY][playerX])
			try:
				if playerX+1 < 0:
					MoveTo = (GameMap[playerY][playerX])
					CheckForRoom()
				else:
					MoveTo = (GameMap[playerY][playerX+1])
					if "@" in Current:
						GameMap[playerY][playerX] = Current.split("@")[1].strip()
					elif Current == "Player":
						GameMap[playerY][playerX] = "0"
					if MoveTo == "0":
						GameMap[playerY][playerX+1] = "Player"
						playerX = playerX+1
						CheckForRoom()
					else:
						GameMap[playerY][playerX+1] = "Player @ "+GameMap[playerY][playerX+1]
						playerX = playerX+1
						CheckForRoom()

			except IndexError:
				(GameMap[playerY][playerX]) = (GameMap[playerY][playerX])
				CheckForRoom()

	
	
	
	def Game():
		
		CheckForRoom()	
		sys.stdout.write(cursor + " ")
		sys.stdout.flush()

    # Main loop to detect movement
		while True:
			
			
			event = keyboard.read_event(suppress= True)
			
			if event.event_type == keyboard.KEY_DOWN:
				
				sys.stdout.write("\r" + " " * len(cursor) + "\r")
				sys.stdout.flush()
				
				if event.name == "up":
					
					MovePlayer("up")
					if Map == True:
						ShowMap()
				elif event.name == "down":
					
					MovePlayer("down")
					if Map == True:
						ShowMap()
				elif event.name == "left":
					
					MovePlayer("left")
					if Map == True:
						ShowMap()
				elif event.name == "right":
					
					MovePlayer("right")
					if Map == True:
						ShowMap()
				
				
				elif event.name == ExitKey or event.name == ExitKey.upper():
					break
		
				

				sys.stdout.write(cursor + " ")
				sys.stdout.flush()
	Code()
	Game()
if Map == True:
						ShowMap()
Play()


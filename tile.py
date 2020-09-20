import json
from math import sin, cos, radians

theAngle = {
    'R': 0,
    'J': 30,
    'E': 45,
    'T': 60,
    'U': 90,
    'G': 120,
    'Q': 135,
    'H': 150,
    'L': 180,
    'N': 210,
    'Z': 225,
    'F': 240,
    'D': 270,
    'B': 300,
    'C': 315,
    'M': 330
}

ang180 = {
    'R': 0,
    'L': 180,
    'U': 90,
    'D': 270
}

def nOrE(a):
    if a % 2 == 0:
        return "red"
    else:
        return "blue"
def zOrH(a):
    if a <= 2:
        return 100
    else:
        return 0
fileName = input("type a name of ADOFAI file (with .adofai): ")
data = open(fileName, mode='r',encoding='utf-8-sig').read()
data = data.replace(', ,', ',')
data = data.replace('}\n		{', '},\n		{')
data = data.replace(',\n	]', '\n	]')
data = json.loads(data)

tiles = data["pathData"]
actions = data['actions']
twirls = []
for i in actions:
    if i["eventType"] == "Twirl":
        twirls.append(i["floor"])

tileDecos = []
ballDecos = []
ballRotas = []
firstTile = []
tw = 0

for i in range(len(tiles)):
    if i == 0:
        pre = 0
    else:
        pre = theAngle[tiles[i-1]]
    this = theAngle[tiles[i]]
    try:
        tile = ang180[tiles[i]]
    except KeyError:
        print("%dth tile has unsupported angle" % (i))
        exit()
    try:
        nex = theAngle[tiles[i+1]]
    except IndexError:
        nex = theAngle[tiles[i]]
    angle = (pre - this) % 360
    if i+1 in twirls:
        tw += 1
    #여기부터 타일
    if angle == 270:
        angle2 = (ang180[tiles[i]] - angle) % 360
        tileDecos.append({ "floor": i, "eventType": "AddDecoration", "decorationImage": "90.png", "position": [0, 0], "relativeTo": "Tile", "pivotOffset": [0, 0], "rotation": angle2, "scale": 222, "depth": 0, "tag": str(i) })
    elif angle == 90:
        angle2 = (angle + ang180[tiles[i]] - 90) % 360
        tileDecos.append({ "floor": i, "eventType": "AddDecoration", "decorationImage": "90.png", "position": [0, 0], "relativeTo": "Tile", "pivotOffset": [0, 0], "rotation": angle2, "scale": 222, "depth": 0, "tag": str(i) })
    elif angle == 0:
        angle2 = (ang180[tiles[i]]) % 360
        tileDecos.append({ "floor": i, "eventType": "AddDecoration", "decorationImage": "180.png", "position": [0, 0], "relativeTo": "Tile", "pivotOffset": [0, 0], "rotation": angle2, "scale": 222, "depth": 0, "tag": str(i) })
    #여기부터 공 옵젝
    ballDecos.append({ "floor": i+1, "eventType": "AddDecoration", "decorationImage": "%s.png" % nOrE(i), "position": [0, 0], "relativeTo": "Tile", "pivotOffset": [-cos(radians(this)), -sin(radians(this))], "rotation": 0, "scale": zOrH(i+1), "depth": -1, "tag": 'b'+str(i+1) })
    ballDecos.append({ "floor": i+1, "eventType": "MoveDecorations", "duration": 0, "tag": 'b'+str(i-1), "positionOffset": [0, 0], "rotationOffset": 0, "scale": 0, "angleOffset": 0, "ease": "Linear", "eventTag": "" })
    ballDecos.append({ "floor": i+1, "eventType": "MoveDecorations", "duration": 0, "tag": 'b'+str(i+1), "positionOffset": [0, 0], "rotationOffset": 0, "scale": 100, "angleOffset": 0, "ease": "Linear", "eventTag": "" })
    #여기부터 공 회전
    if tw % 2 == 0:
        dur = (180 - (nex - this)) % 360
        ballRotas.append({ "floor": i+1, "eventType": "MoveDecorations", "duration": (dur/180) % 2, "tag": 'b'+str(i+1), "positionOffset": [0, 0], "rotationOffset": -(dur % 360), "scale": 100, "angleOffset": 0, "ease": "Linear", "eventTag": "" })
    else:
        dur = 180-(this-nex) % 360
        ballRotas.append({ "floor": i+1, "eventType": "MoveDecorations", "duration": (dur/180) % 2, "tag": 'b'+str(i+1), "positionOffset": [0, 0], "rotationOffset": (dur % 360), "scale": 100, "angleOffset": 0, "ease": "Linear", "eventTag": "" })
tileDecos.append({ "floor": i+1, "eventType": "AddDecoration", "decorationImage": "180.png", "position": [0, 0], "relativeTo": "Tile", "pivotOffset": [0, 0], "rotation": angle2, "scale": 222, "depth": 0, "tag": str(i) })
firsttile = [
    	{ "floor": 0, "eventType": "MoveTrack", "startTile": [0, "Start"], "endTile": [0, "End"], "duration": 0, "positionOffset": [0, 0], "rotationOffset": 0, "scale": 150, "opacity": 100, "angleOffset": 0, "ease": "Linear", "eventTag": "" },
		{ "floor": 0, "eventType": "RecolorTrack", "startTile": [0, "Start"], "endTile": [0, "End"], "trackColorType": "Single", "trackColor": "ffffff00", "secondaryTrackColor": "ffffff", "trackColorAnimDuration": 2, "trackColorPulse": "None", "trackPulseLength": 10, "trackStyle": "Standard", "angleOffset": 0, "eventTag": "" },
		{ "floor": 0, "eventType": "ColorTrack", "trackColorType": "Single", "trackColor": "ffffff00", "secondaryTrackColor": "ffffff", "trackColorAnimDuration": 2, "trackColorPulse": "None", "trackPulseLength": 10, "trackStyle": "Standard" },
]
data['actions'] = firsttile+tileDecos+ballDecos+ballRotas+actions
json.dump(data, open("%s_edited.adofai" % fileName, mode='w'))
print("Saved as %s_edited.adofai" % fileName)
import re
import json

n=1

filename = f"./sonarLog{n}.txt"
#filename = "WALL.txt"
savefilename = f"./log{n}.json"
#savefilename = "WALL.json"

with open(filename, "r") as f:
    lines = f.readlines()

xval = 0
yval = 0
angleval = 0
distval = 0

DataArray = []
dataLen = len(lines)
title = lines[0]

i = 0

def getVal(unit,i) -> float:
    value = None
    for type in unit[1].split(" "):
        try: 
            value = float(type)
            return value, i
        except: pass

    
for line in lines[2:]:
    line = line.split(",")
    i= i + 1
    for unit in line:
        unit = unit.split(":")
        topic = unit[0].replace(" ","")
        match topic:
            case "X":
                xval, i = getVal(unit,i)
            case "Y":
                yval, i = getVal(unit,i)
            case "angle":
                angleval, i = getVal(unit,i)
            case "dist":
                distval, i = getVal(unit,i)
            case _:
                print(f"error at line : {line}")
    data = {
        "Line" : i,
        "X" : xval,
        "Y" : yval,
        "angle" : angleval,
        "dist" : distval
    }
    
    DataArray.append(data)

if (dataLen)-2 != len(DataArray):
    print("Error something went very wrong data is missing")
else:
    print(f"{dataLen-2} / {len(DataArray)}")


def dataVerify(DataArray):
    oldline = 0
    for data in DataArray:
        newline = data.get("Line")
        print("Line:", data.get("Line"), 
            "X:", data.get("X"), 
            "Y:", data.get("Y"), 
            "angle:", data.get("angle"), 
            "dist:", data.get("dist"))
        if (oldline+1) != newline:
            print("ERROR")
            break
        oldline = data.get("Line")


dataVerify(DataArray)

output = {
    "title": title,
    "data": DataArray
}

with open(savefilename, "w") as outfile:
    json.dump(output, outfile, indent=4)
    print(f'Converted : {filename}, saved as : {savefilename}')
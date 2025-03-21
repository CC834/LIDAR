import json
import matplotlib.pyplot as plt
from filter import filter_point
debug = False
DataArray = []
lines   = []
n = 3
def saveDatatojson(Line,xval,yval,distval):
    data = {
    "Line" : Line,
    "X" : xval,
    "Y" : yval,
    "dist" : distval
    } 
    DataArray.append(data)

def dataVerify(DataArray, printf=False):
    oldline = 0
    for data in DataArray:
        newline = data.get("Line")
        if printf:
            print("Line:", data.get("Line"), 
                  "X:", data.get("X"), 
                  "Y:", data.get("Y"), 
                  "angle:", data.get("angle"), 
                  "dist:", data.get("dist"))
        if (oldline + 1) != newline:
            print("ERROR")
            break
        oldline = data.get("Line")


def make_loadingPercentage():
    # Set thresholds for 33%, 66%, and 100%
    thresholds = [0.10, 0.20, 0.30, 0.40, 0.50, 0.60, 0.70, 0.8, 0.90, 1.0]
    def loadingPercentage(line: int, lines: int):
        nonlocal thresholds
        progress = line / lines
        if thresholds and progress >= thresholds[0]:
            percent = int(thresholds[0] * 100)
            print(f"Loading: {percent}%")
            thresholds.pop(0)
    return loadingPercentage
loadingPercentage = make_loadingPercentage()

def plot_lidar_data(filename):
    with open(filename, "r") as f:
        data = json.load(f)

    title = data.get("title", "")
    payload = data.get("data", [])
    x_vals = []
    y_vals = []
    angles = []
    dists = []


    dataVerify(payload)


    for data in payload:
        line = data.get("Line")
        loadingPercentage(line, len(payload))
        #print(line)
        x_val = data.get("X")
        y_val = data.get("Y")
        angle = data.get("angle")
        dist = data.get("dist")

        x_val, y_val, angle, dist = filter_point(x_val, y_val, angle, dist, line, dist)
        if x_val is None:
            continue

        x_vals.append(x_val)
        y_vals.append(y_val)
        angles.append(angle)
        dists.append(dist)

        lines.append(line)
        saveDatatojson(line,x_val,y_val,dist)

    # Plotting
    plt.figure(figsize=(8, 6))
    plt.scatter(x_vals, y_vals, c='blue', marker='o')
    plt.title(title)
    plt.xlabel("X (mm)")
    plt.ylabel("Y (mm)")
    plt.grid(True)

    output = {
        "title": title,
        "data": DataArray
    }

    with open(f"./Filterd_log{n}.json", "w") as outfile:
        json.dump(output, outfile, indent=4)

    plt.show()

if __name__ == "__main__":
    print("starting...")
    plot_lidar_data(f"./log{n}.json")
    #plot_lidar_data(f"./WALL.json")

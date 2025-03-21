import json
import matplotlib.pyplot as plt
from filter import filter_point

filename = "./log1.json"

n = 2
filename = f"./Filterd_log{n}.json"
filename = f"./log{n}.json"

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
        
        x_val = data.get("X")
        y_val = data.get("Y")
        angle = data.get("angle")
        dist = data.get("dist")

        x_vals.append(x_val)
        y_vals.append(y_val)
        angles.append(angle)
        dists.append(dist)


    # Plotting
    plt.figure(figsize=(8, 6))
    plt.scatter(x_vals, y_vals, c='blue', marker='o')
    plt.title(title)
    plt.xlabel("X (mm)")
    plt.ylabel("Y (mm)")
    plt.grid(True)




    plt.show()

if __name__ == "__main__":
    plot_lidar_data(filename)

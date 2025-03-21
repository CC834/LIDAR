
import math
import json

class LIDAR_Filter:
  def __init__(self, name, age):

    self.debug = False
    self.MAX_TYPE = "X"
    self.MAX_VALUE = 850
    self.WALL_ON = False

    pass
  
  def removePoint(self, error: int, x, y, xw, yw,dist,line):
    dist = math.dist([0,0],[x,y])

    # Calculate the tolerance offset using the absolute value of the wall coordinates
    xw_r = abs(xw) * (error / 100.0)
    # Ensure lower and upper bounds are in the correct order
    xw_lower = min(xw - xw_r, xw + xw_r)
    xw_upper = max(xw - xw_r, xw + xw_r)

    yw_r = abs(yw) * (error / 100.0)
    yw_lower = min(yw - yw_r, yw + yw_r)
    yw_upper = max(yw - yw_r, yw + yw_r)

    if (xw_lower < x < xw_upper) and (yw_lower < y < yw_upper):
        return True

    return False
  
  def filter_point(self,X, Y, A, D, line,dist):
    match self.MAX_TYPE:
        case "X":
            if X > self.MAX_VALUE: 
                if elf.debug: print("removed due to distance on line", line)
                return None, None, None, None
        case "dist":
            if dist > MAX_VALUE:
                if elf.debug: print("removed due to distance on line", line)
                return None, None, None, None
    
    with open("WALL.json", "r") as f:
        data = json.load(f)
    payload = data.get("data", [])

    if self.WALL_ON: return X, Y, A, D
    # Check every wall point
    for wall in payload:
        xw = wall.get("X")
        yw = wall.get("Y")
        if self.removePoint(1, X, Y, xw, yw,dist,line):
            if self.debug: print("removed ", line)
            return None, None, None, None

    # If no match, return the original data.
    return X, Y, A, D



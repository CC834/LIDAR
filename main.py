import json
import threading
import matplotlib.pyplot as plt
from filter import filter_point  # Make sure this function is accessible in your project

class LidarData:
    """
    Class to load, verify, and process LIDAR JSON data.
    """
    def __init__(self, json_filename, debug=False):
        self.json_filename = json_filename
        self.debug = debug
        self.title = ""
        self.raw_data = []         # Data loaded from the JSON file
        self.processed_data = []   # Data after filtering
        self.x_vals = []
        self.y_vals = []
        self.angles = []
        self.dists = []
        self.load_data()

    def load_data(self):
        """Load JSON data from file."""
        try:
            with open(self.json_filename, "r") as f:
                data = json.load(f)
            self.title = data.get("title", "Lidar Data")
            self.raw_data = data.get("data", [])
        except Exception as e:
            print(f"Error loading data: {e}")

    def data_verify(self):
        """Verify that line numbers are sequential."""
        old_line = 0
        for d in self.raw_data:
            current_line = d.get("Line")
            if self.debug:
                print(f"Verifying Line {current_line}: {d}")
            if (old_line + 1) != current_line:
                print(f"Data verification error at line: {current_line}")
                break
            old_line = current_line

    def process_data(self):
        """
        Process the raw data by applying filtering and collecting valid points.
        A simple progress indicator is printed as a percentage.
        """
        total = len(self.raw_data)
        # Define progress thresholds
        thresholds = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]

        for idx, d in enumerate(self.raw_data, start=1):
            progress = idx / total
            if thresholds and progress >= thresholds[0]:
                percent = int(thresholds[0] * 100)
                print(f"Loading: {percent}%")
                thresholds.pop(0)

            line = d.get("Line")
            x_val = d.get("X")
            y_val = d.get("Y")
            angle = d.get("angle")
            dist = d.get("dist")
            # Apply filter from filter.py. If the filter returns None, skip the point.
            x_val, y_val, angle, dist = filter_point(x_val, y_val, angle, dist, line, dist)
            if x_val is None:
                continue

            self.x_vals.append(x_val)
            self.y_vals.append(y_val)
            self.angles.append(angle)
            self.dists.append(dist)
            self.processed_data.append({
                "Line": line,
                "X": x_val,
                "Y": y_val,
                "angle": angle,
                "dist": dist
            })

class LidarPlotter:
    """
    Class to handle plotting of processed LIDAR data.
    The plotting is done in a separate thread to avoid freezing the main application.
    """
    def __init__(self, lidar_data: LidarData, save_json_filename=None):
        self.lidar_data = lidar_data
        self.save_json_filename = save_json_filename

    def plot_data(self):
        """Plot the LIDAR data using matplotlib and optionally save the processed data."""
        if not self.lidar_data.processed_data:
            print("No processed data available. Please run process_data() first.")
            return

        plt.figure(figsize=(8, 6))
        plt.scatter(self.lidar_data.x_vals, self.lidar_data.y_vals, c='blue', marker='o')
        plt.title(self.lidar_data.title)
        plt.xlabel("X (mm)")
        plt.ylabel("Y (mm)")
        plt.grid(True)
        plt.show()

        # Optionally, save processed data to JSON.
        if self.save_json_filename:
            output = {
                "title": self.lidar_data.title,
                "data": self.lidar_data.processed_data
            }
            try:
                with open(self.save_json_filename, "w") as outfile:
                    json.dump(output, outfile, indent=4)
                print(f"Processed data saved to {self.save_json_filename}")
            except Exception as e:
                print(f"Error saving processed data: {e}")

    def start_plotting(self):
        """Run the plot_data method in a separate thread."""
        plot_thread = threading.Thread(target=self.plot_data)
        plot_thread.start()
        return plot_thread

# Example usage:
"""if __name__ == "__main__":
    # Create a LidarData instance using the JSON file generated (e.g., by dataojson.py)
    data_handler = LidarData("log1.json", debug=True)
    data_handler.data_verify()      # Verify raw data (optional)
    data_handler.process_data()     # Process (filter) the data

    # Create a LidarPlotter instance and start plotting in a new thread.
    plotter = LidarPlotter(data_handler, save_json_filename="Filtered_log1.json")
    plotter.start_plotting()
"""
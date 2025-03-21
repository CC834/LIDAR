import re
import statistics

def process_log_file(filename):
    tests = {}  # Dictionary to store measurements for each test
    current_test = None

    with open(filename, "r") as file:
        for line in file:
            line = line.strip()
            # Look for test header lines like "TEST 1 : DISTANCE 28 cm"
            header_match = re.match(r"TEST\s+(\d+)\s*:\s*DISTANCE\s+(\d+)\s*cm", line, re.IGNORECASE)
            if header_match:
                test_number = header_match.group(1)
                nominal_distance = header_match.group(2)
                current_test = f"TEST {test_number} (Nominal {nominal_distance} cm)"
                tests[current_test] = []
                continue

            # Look for measurement lines like "1 Distance: 99.61 cm"
            measurement_match = re.search(r"Distance:\s+([\d.]+)\s*cm", line, re.IGNORECASE)
            if measurement_match and current_test:
                distance = float(measurement_match.group(1))
                tests[current_test].append(distance)
    
    # Compute statistics for each test
    results = {}
    for test, distances in tests.items():
        if distances:
            mean_val = statistics.mean(distances)
            # Using sample standard deviation; for population stdev, use statistics.pstdev(distances)
            stddev_val = statistics.stdev(distances)
            results[test] = {"count": len(distances), "mean": mean_val, "stddev": stddev_val}
    return results

print("TEST 2 : Glass")
filename = "./log2"  # Ensure your log file is named log.txt in the same directory as this script.
stats = process_log_file(filename)
for test, res in stats.items():
    print(f"{test}:")
    print(f"  Number of readings: {res['count']}")
    print(f"  Mean distance: {res['mean']:.2f} cm")
    print(f"  Standard Deviation: {res['stddev']:.2f} cm")


print("TEST 3 : Clothing")
filename = "./log3"  # Ensure your log file is named log.txt in the same directory as this script.
stats = process_log_file(filename)
for test, res in stats.items():
    print(f"{test}:")
    print(f"  Number of readings: {res['count']}")
    print(f"  Mean distance: {res['mean']:.2f} cm")
    print(f"  Standard Deviation: {res['stddev']:.2f} cm")

print("TEST 1 : Cardboard")
filename = "./log1"  # Ensure your log file is named log.txt in the same directory as this script.
stats = process_log_file(filename)
for test, res in stats.items():
    print(f"{test}:")
    print(f"  Number of readings: {res['count']}")
    print(f"  Mean distance: {res['mean']:.2f} cm")
    print(f"  Standard Deviation: {res['stddev']:.2f} cm")

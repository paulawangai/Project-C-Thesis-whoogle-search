import re
import statistics
import os
import subprocess

# Get the current file's directory
current_dir = os.path.dirname(os.path.abspath(__file__))
metrics_dir = os.path.join(current_dir, 'metrics', 'final_metrics')

# Get all filenames in the directory
try:
    result = subprocess.run(['ls', metrics_dir], capture_output=True, text=True, check=True)
    files = result.stdout.strip().split('\n')
    print(f"Files in directory:")
    for i, file in enumerate(files):
        print(f"  {i}: '{file}'")
    
    # Find the halstead metrics file
    halstead_files = [f for f in files if 'halstead_metrics_after_with_tests.txt' in f]
    if halstead_files:
        halstead_file = halstead_files[0]
        print(f"Found halstead file: '{halstead_file}'")
        
        # Use subprocess to read the file
        file_path = os.path.join(metrics_dir, halstead_file)
        print(f"Reading file with cat command: {file_path}")
        
        result = subprocess.run(['cat', file_path], capture_output=True, text=True)
        content = result.stdout
        
        print(f"File content length: {len(content)} chars")
        print(f"First 100 chars: {content[:100]}")
        
        # Process the content directly from the subprocess output
        lines = content.split('\n')
        
        # Initialize lists to store values for each metric
        h1, h2, N1, N2, vocabulary, length, calculated_length = [], [], [], [], [], [], []
        volume, difficulty, effort, time, bugs = [], [], [], [], []
        
        current_file = None
        for line in lines:
            line = line.strip()
            
            if line and not line.startswith(' ') and ':' not in line:
                # This is a filename line
                current_file = line
            elif 'h1:' in line:
                value = re.search(r'h1: ([\d.]+)', line)
                if value:
                    h1.append(float(value.group(1)))
            elif 'h2:' in line:
                value = re.search(r'h2: ([\d.]+)', line)
                if value:
                    h2.append(float(value.group(1)))
            elif 'N1:' in line:
                value = re.search(r'N1: ([\d.]+)', line)
                if value:
                    N1.append(float(value.group(1)))
            elif 'N2:' in line:
                value = re.search(r'N2: ([\d.]+)', line)
                if value:
                    N2.append(float(value.group(1)))
            elif 'vocabulary:' in line:
                value = re.search(r'vocabulary: ([\d.]+)', line)
                if value:
                    vocabulary.append(float(value.group(1)))
            elif 'length:' in line and 'calculated_length:' not in line:
                value = re.search(r'length: ([\d.]+)', line)
                if value:
                    length.append(float(value.group(1)))
            elif 'calculated_length:' in line:
                value = re.search(r'calculated_length: ([\d.]+)', line)
                if value:
                    calculated_length.append(float(value.group(1)))
            elif 'volume:' in line:
                value = re.search(r'volume: ([\d.]+)', line)
                if value:
                    volume.append(float(value.group(1)))
            elif 'difficulty:' in line:
                value = re.search(r'difficulty: ([\d.]+)', line)
                if value:
                    difficulty.append(float(value.group(1)))
            elif 'effort:' in line:
                value = re.search(r'effort: ([\d.]+)', line)
                if value:
                    effort.append(float(value.group(1)))
            elif 'time:' in line:
                value = re.search(r'time: ([\d.]+)', line)
                if value:
                    time.append(float(value.group(1)))
            elif 'bugs:' in line:
                value = re.search(r'bugs: ([\d.]+)', line)
                if value:
                    bugs.append(float(value.group(1)))

        # Skip files with all zeros
        non_zero_h1 = [val for val in h1 if val > 0]
        non_zero_h2 = [val for val in h2 if val > 0]
        non_zero_N1 = [val for val in N1 if val > 0]
        non_zero_N2 = [val for val in N2 if val > 0]
        non_zero_vocabulary = [val for val in vocabulary if val > 0]
        non_zero_length = [val for val in length if val > 0]
        non_zero_calculated_length = [val for val in calculated_length if val > 0]
        non_zero_volume = [val for val in volume if val > 0]
        non_zero_difficulty = [val for val in difficulty if val > 0]
        non_zero_effort = [val for val in effort if val > 0]
        non_zero_time = [val for val in time if val > 0]
        non_zero_bugs = [val for val in bugs if val > 0]

        # Calculate averages (excluding zero values)
        print(f"Average h1: {statistics.mean(non_zero_h1) if non_zero_h1 else 'N/A'}")
        print(f"Average h2: {statistics.mean(non_zero_h2) if non_zero_h2 else 'N/A'}")
        print(f"Average N1: {statistics.mean(non_zero_N1) if non_zero_N1 else 'N/A'}")
        print(f"Average N2: {statistics.mean(non_zero_N2) if non_zero_N2 else 'N/A'}")
        print(f"Average vocabulary: {statistics.mean(non_zero_vocabulary) if non_zero_vocabulary else 'N/A'}")
        print(f"Average length: {statistics.mean(non_zero_length) if non_zero_length else 'N/A'}")
        print(f"Average calculated_length: {statistics.mean(non_zero_calculated_length) if non_zero_calculated_length else 'N/A'}")
        print(f"Average volume: {statistics.mean(non_zero_volume) if non_zero_volume else 'N/A'}")
        print(f"Average difficulty: {statistics.mean(non_zero_difficulty) if non_zero_difficulty else 'N/A'}")
        print(f"Average effort: {statistics.mean(non_zero_effort) if non_zero_effort else 'N/A'}")
        print(f"Average time: {statistics.mean(non_zero_time) if non_zero_time else 'N/A'}")
        print(f"Average bugs: {statistics.mean(non_zero_bugs) if non_zero_bugs else 'N/A'}")

        # Print file count
        print(f"Total files analyzed: {len(h1)}")
        print(f"Files with code: {len(non_zero_h1)}")
        
        # Write results to output file
        output_file = os.path.join(metrics_dir, 'halstead_averages_after_with_tests.txt')
        with open(output_file, 'w') as f:
            f.write(f"Average h1: {statistics.mean(non_zero_h1) if non_zero_h1 else 'N/A'}\n")
            f.write(f"Average h2: {statistics.mean(non_zero_h2) if non_zero_h2 else 'N/A'}\n")
            f.write(f"Average N1: {statistics.mean(non_zero_N1) if non_zero_N1 else 'N/A'}\n")
            f.write(f"Average N2: {statistics.mean(non_zero_N2) if non_zero_N2 else 'N/A'}\n")
            f.write(f"Average vocabulary: {statistics.mean(non_zero_vocabulary) if non_zero_vocabulary else 'N/A'}\n")
            f.write(f"Average length: {statistics.mean(non_zero_length) if non_zero_length else 'N/A'}\n")
            f.write(f"Average calculated_length: {statistics.mean(non_zero_calculated_length) if non_zero_calculated_length else 'N/A'}\n")
            f.write(f"Average volume: {statistics.mean(non_zero_volume) if non_zero_volume else 'N/A'}\n")
            f.write(f"Average difficulty: {statistics.mean(non_zero_difficulty) if non_zero_difficulty else 'N/A'}\n")
            f.write(f"Average effort: {statistics.mean(non_zero_effort) if non_zero_effort else 'N/A'}\n")
            f.write(f"Average time: {statistics.mean(non_zero_time) if non_zero_time else 'N/A'}\n")
            f.write(f"Average bugs: {statistics.mean(non_zero_bugs) if non_zero_bugs else 'N/A'}\n")
            f.write(f"Total files analyzed: {len(h1)}\n")
            f.write(f"Files with code: {len(non_zero_h1)}\n")
            
        print(f"Results written to: {output_file}")
        
    else:
        print("No halstead metrics file found in the directory")
        
except subprocess.CalledProcessError as e:
    print(f"Error running ls command: {e}")
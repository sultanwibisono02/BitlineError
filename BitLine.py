import re
from collections import Counter
import matplotlib.pyplot as plt
import numpy as np

# Function to convert hex to 64-bit binary string
def hex_to_64bit_binary(hex_val):
    return bin(int(hex_val, 16))[2:].zfill(64)

# Function to compare two hex values and find mismatched bit positions
def compare_hex_pairs(hex1,hex2):
    bin1 = hex_to_64bit_binary(hex1)
    bin2 = hex_to_64bit_binary(hex2)

    length = len(bin1)

    mismatches = [(length - 1 -i) for i, (b1,b2) in enumerate(zip(bin1,bin2)) if b1!=b2]

    return mismatches

# Function to read hex pairs from a file and compare them
def process_hex_file(file_path):
    mismatch_counter = Counter()
    error_counter = Counter()

    # Relaxed regular expression to find any length hex numbers
    hex_pattern = re.compile(r'0x[0-9A-Fa-f]+')
    
    ## Use this if multiple txt files are necessary 

    # for file_path in file_path:
    #     try:
    #         with open(file_path, 'r') as file:
    #             for line in file:
    #                 print(f"Line from file: {line.strip()}")  # Debugging: print each line
    #                 hex_pair = hex_pattern.findall(line)
    #                 print(f"Hex pairs found: {hex_pair}")  # Debugging: print the hex pairs
    #                 if len(hex_pair) == 2:  # Found a valid pair
    #                     mismatches = compare_hex_pairs(hex_pair[0], hex_pair[1])
    #                     mismatch_counter.update(mismatches)
    #                     print(f"Mismatches for pair {hex_pair}: {mismatches}")  # Debugging print
    #     except FileNotFoundError:
    #         print(f"File not found :{file_path}")
    
    # Open the file

    with open(file_path, 'r') as file:
                for line in file:
                    print(f"Line from file: {line.strip()}")  # Debugging: print each line
                    hex_pair = hex_pattern.findall(line)

                    if len(hex_pair) >= 2:  # Found a valid pair
                        print(f"Hex pairs found: {hex_pair}")  # Debugging: print the hex pairs

                        mismatches = compare_hex_pairs(hex_pair[0], hex_pair[1])
                        mismatch_counter.update(mismatches)
                        print(f"Mismatches for pair {hex_pair[0],hex_pair[1]}: {mismatches}")  # Debugging print
                        print(" mismatch counter :: ",len(mismatches),"\n")

                        #Error Counter
                        error_count = len(mismatches)
                        error_counter.update([error_count])

    sorted_mismatch_counter = dict(sorted(mismatch_counter.items()))
    sorted_error_counter = dict(sorted(error_counter.items()))

    print("Error Count = ",sorted_error_counter)

    return (sorted_mismatch_counter,sorted_error_counter)

# def convert_path(file_path):
#     return file_path.replace("\\","/")

# Clean the ".." from the path
def clean_file_path(file_path):
     return file_path.strip('"').strip("'")

# Function to generate and display the graph
def generate_graph(mismatch_counter,error_counter):
    if not mismatch_counter:
        print("No mismatches found to display.")
        return
    
# Extract bit positions and their corresponding error frequencies
    bit_positions = list(mismatch_counter.keys())
    mismatch_frequencies = list(mismatch_counter.values())

    # bit_positions = list(reversed(bit_positions))
    # error_frequencies = list(reversed(error_frequencies))

    # Create the bar graph
    plt.figure(figsize=(10, 6))
    plt.bar(bit_positions, mismatch_frequencies, color='skyblue')

    # Add labels and title
    plt.xlabel('Bit Position (Dq63 - Dq0)', fontsize=12)
    plt.ylabel('Frequency of Mismatches', fontsize=12)
    plt.title('Error Frequency by Bit Position (Dq63 on Left, Dq0 on Right)', fontsize=14)

    # Set x-axis labels for bit positions (Dq63 to Dq0)
    plt.xticks(np.arange(0, 64, 1), [f'Dq{63- i}' for i in range(63, -1, -1)], rotation=90, ha='center')
    plt.xlim(-0.5, 63.5)

    # Ensure y-axis shows integer values
    plt.gca().yaxis.get_major_locator().set_params(integer=True)

    # Reverse x-axis to match the flipped labels
    plt.gca().invert_xaxis()
    plt.tight_layout()
    plt.grid()
    plt.show()

#test github

# Generate graph for Error Counter
    # error_numbers = list(error_counter.keys())
    # error_frequencies = list(error_counter.values())

    error_numbers = np.arange(0, 65, 1)
    error_frequencies = [error_counter.get(i,0) for i in error_numbers]

    # Create the bar graph
    plt.figure(figsize=(10, 6))
    plt.bar(error_numbers, error_frequencies, color='skyblue')

    # Add labels and title
    plt.xlabel('Number of Error in one iteration', fontsize=12)
    plt.ylabel('Frequency of Error each iteration', fontsize=12)
    plt.title('Error Frequency by Error Numbers ', fontsize=14)

    # Set x-axis labels for bit positions (Dq63 to Dq0)
    # plt.xticks(np.arange(0, 65, 1), [i for i in range(0,65)], rotation=90, ha='center')
    plt.xticks(np.arange(0, 65, 1), rotation=90, ha='center')

    plt.xlim(-0.5, 64.5)

    # Ensure y-axis shows integer values
    plt.gca().yaxis.get_major_locator().set_params(integer=True)

    # Reverse x-axis to match the flipped labels
    plt.tight_layout()
    plt.grid()
    plt.show()



# Main function to run the comparison and graph generation
def main():
    # Path to the .txt file (you can change this path)

    file_path = input("Enter input file path: ")
    file_path = clean_file_path(file_path)
    print(file_path)

    # # file_path = r"c:\Users\nauva\Desktop\hex_data.txt"
    # file_path = "C:/Users/nauva/Desktop/hex_data.txt"

    # Process the file and get mismatch frequencies
    mismatch_counter, error_counter = process_hex_file(file_path)

    # Debugging: print the mismatch counter
    print(f"Mismatch Counter: \n{mismatch_counter}")

    # Generate the graph
    generate_graph(mismatch_counter, error_counter)

# Run the program
if __name__ == '__main__':
    main()

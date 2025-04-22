import re
from collections import Counter
import matplotlib.pyplot as plt
import numpy as np

# Function to convert hex to 64-bit binary string
def hex_to_64bit_binary(hex_val):
    return bin(int(hex_val, 16))[2:].zfill(len(hex_val) * 4)

# Function to compare two hex values and find mismatched bit positions
def compare_hex_pairs(hex1,hex2):
    bin1 = hex_to_64bit_binary(hex1)
    bin2 = hex_to_64bit_binary(hex2)

    length = len(bin1)

    mismatches = [(length - 1 -i) for i, (b1,b2) in enumerate(zip(bin1,bin2)) if b1!=b2]

    return mismatches

# Function to read hex pairs from a file and compare them
def process_hex(hex_pairs):
    mismatch_counter = Counter()
    error_counter = Counter()

    for idx, (hex1, hex2) in enumerate(hex_pairs):
        try:
            if not hex1 or not hex2:
                print(f"Empty hex string found in pair {idx + 1}: ({hex1}, {hex2})")
                continue

            print(f"\nHex pair ({idx+1}) = ['{hex1}', '{hex2}'] will be checked")
            mismatches = compare_hex_pairs(hex1, hex2)
            mismatch_counter.update(mismatches)
            print(f"Mismatches for pair ({hex1}, {hex2}): {mismatches}")
            print(" mismatch counter :: ",len(mismatches),"\n")

            error_count = len(mismatches)
            error_counter.update([error_count])

        except ValueError as ve:
            print(f"❌ Error processing pair {idx}: ({hex1}, {hex2})")
            print("   Reason:", ve)

    sorted_mismatch_counter = dict(sorted(mismatch_counter.items()))
    sorted_error_counter = dict(sorted(error_counter.items()))

    print("Error Count = ",sorted_error_counter)
    print("Total Bit Mismatches =", sorted_mismatch_counter)

    return(mismatch_counter, error_counter,)

def get_selected_hex_pair(hex_pairs, level, group):
    prefix_map = {
        "1": (0, 8),
        "2": (0, 4),
        "3": (0, 2)
    }
    start_map = {
        "1": {"a": 0, "b": 8},
        "2": {"a": 0, "b": 4, "c": 8, "d": 12},
        "3": {"a": 0, "b": 2, "c": 4, "d": 6, "e": 8, "f": 10, "g": 12, "h": 14}
    }

    updated_pairs = []
    size = prefix_map[level][1]
    start = start_map[level][group]


    for hex1, hex2 in hex_pairs:
        part1 = hex1[start:start+size]
        part2 = hex2[start:start+size]
        updated_pairs.append((part1, part2))
        if len(part1) == len(part2) :
            hex_length = len(part2)

    return updated_pairs,hex_length

def acquire_hex(file_path):
    file_path = file_path.strip('"').strip("'")
    print(file_path)
    hex_pattern = re.compile(r'0x[0-9A-Fa-f]+')

    hex_pairs = []

    with open(file_path, 'r') as file:
        for line in file:
            print(f"Line from file: {line.strip()}")  # Debugging: print each line
            hex_pair = hex_pattern.findall(line)

            if len(hex_pair) >= 2:
                print(f"Hex pairs found: {hex_pair}") 
                if len(hex_pair[0][2:]) < 16 or len(hex_pair[1][2:]) < 16:
                    print(f"Skipping short hex pair: {hex_pair[0]}, {hex_pair[1]}")
                    continue
                hex1, hex2 = hex_pair[0][2:], hex_pair[1][2:]
                hex_pairs.append((hex1,hex2))

    return hex_pairs

# Function to generate and display the graph
def generate_graph_spec(mismatch_counter,error_counter,hex_length, group_label='a'):
    if not mismatch_counter:
        print("No mismatches found to display.")
        return
    
# Extract bit positions and their corresponding error frequencies
    bit_positions = list(mismatch_counter.keys())
    mismatch_frequencies = list(mismatch_counter.values())
    
    bit_count = hex_length * 4
    group_index = ord(group_label.lower()) - ord('a')

    start_bit = 64 - ((group_index + 1) * bit_count)
    end_bit = start_bit + bit_count - 1
    print("end_bit", end_bit, "bit_count", bit_count, "end_bit", end_bit)

    # bit_positions = list(reversed(bit_positions))
    # error_frequencies = list(reversed(error_frequencies))

    # Create the bar graph
    plt.figure(figsize=(12,7))
    plt.bar(bit_positions, mismatch_frequencies, color='skyblue')

    # Add labels and title
    plt.xlabel(f'Bit Position (Dq{end_bit} - Dq{start_bit})', fontsize=12)
    plt.ylabel('Frequency of Mismatches', fontsize=12)
    plt.title(f'Error Frequency for Group {group_label.upper()} ({bit_count} bits)', fontsize=14)

    # Set x-axis labels for bit positions (Dq63 to Dq0)
    plt.xticks(
        np.arange(0, bit_count, 1), 
        [f'Dq{end_bit- i + 1}' for i in range(bit_count,0, -1)], 
        rotation=90, 
        ha='center'
    )

    plt.xlim(-0.5, bit_count - 0.5)

    # Ensure y-axis shows integer values
    plt.gca().yaxis.get_major_locator().set_params(integer=True)

    # Reverse x-axis to match the flipped labels
    plt.gca().invert_xaxis()
    plt.tight_layout()
    plt.grid()
    plt.show()

# Generate graph for Error Counter
    # error_numbers = list(error_counter.keys())
    # error_frequencies = list(error_counter.values())

    error_numbers = np.arange(0, bit_count + 1, 1)
    error_frequencies = [error_counter.get(i,0) for i in error_numbers]

    # Create the bar graph
    plt.figure(figsize=(12,7))
    plt.bar(error_numbers, error_frequencies, color='skyblue')

    # Add labels and title
    plt.xlabel('Number of Error in one iteration', fontsize=12)
    plt.ylabel('Frequency of Error each iteration', fontsize=12)
    plt.title('Error Frequency by Error Numbers ', fontsize=14)

    # Set x-axis labels for bit positions (Dq63 to Dq0)
    # plt.xticks(np.arange(0, 65, 1), [i for i in range(0,65)], rotation=90, ha='center')
    plt.xticks(np.arange(0, bit_count + 1, 1), rotation=90, ha='center')

    plt.xlim(-0.5, bit_count + 0.5)

    # Ensure y-axis shows integer values
    plt.gca().yaxis.get_major_locator().set_params(integer=True)

    # Reverse x-axis to match the flipped labels
    plt.tight_layout()
    plt.grid()
    plt.show()

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
    file_path = input("Enter input file path: ")
    hex_pairs = acquire_hex(file_path)

    print("\nWhich level to check for mismatch:")
    print("  0 - Full 16-char")
    print("  1 - 8-char blocks")
    print("  2 - 4-char blocks")
    print("  3 - 2-char blocks")

    selected_level = input("Please input your selection (0/1/2/3): ").strip()

    if selected_level == "0":
        mismatch_counter,error_counter = process_hex(hex_pairs)
        generate_graph(mismatch_counter,error_counter)

    elif selected_level in {"1", "2", "3"}:
        group_map = {"1": 2, "2": 4, "3": 8}
        group_count = group_map.get(selected_level, 0)
        print(f"Selected char blocks: {group_count}")
        labels = [chr(97 + i) for i in range(group_count)]
        print(f"Available groups: {', '.join(labels)}")
        selected_group = input("Please input your group selection: ").strip().lower()

        if selected_group in labels:
            updated_hex_pairs, hex_length = get_selected_hex_pair(hex_pairs, selected_level, selected_group)
            print("Updated hex pairs:", updated_hex_pairs)
            print("hex_length",hex_length)
            mismatch_counter,error_counter = process_hex(updated_hex_pairs)
            generate_graph_spec(mismatch_counter,error_counter,hex_length, selected_group)

        else:
            print("Invalid group selection.")

# Run the program
if __name__ == '__main__':
    main()

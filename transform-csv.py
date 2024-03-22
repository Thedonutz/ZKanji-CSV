import csv
import argparse

def process_line(line):
    parts = line.split(" ")
    japanese_word = parts[0]
    kana_word = parts[1]
    rest_of_line = " ".join(parts[2:])
    meaning_start = rest_of_line.find("M{") + 2  # Start after "M{"
    meaning_end = rest_of_line.find("#0", meaning_start)  # End before "#0"
    meaning = rest_of_line[meaning_start:meaning_end].strip()
    return [japanese_word, kana_word, meaning]

def process_file(input_file_path):
    processed_data = []
    with open(input_file_path, 'r', encoding='utf-8') as file:
        process_flag = False
        for line in file:
            if line.startswith('[Words]'):
                process_flag = True
                continue
            if process_flag:
                # Skip empty lines or lines that don't contain data entries
                if line.strip() and "M{" in line:
                    processed_data.append(process_line(line))
    return processed_data

def main():
    parser = argparse.ArgumentParser(description='Process a file to extract and transform data, starting from a specific marker.')
    parser.add_argument('-f', '--file', help='Input file path', required=True)
    args = parser.parse_args()

    # Process the file and get the processed data
    processed_data = process_file(args.file)

    # Output filename is derived from the input filename
    output_file = args.file.rsplit('.', 1)[0] + '_processed.csv'

    # Write the processed data to a CSV file, omitting the header
    with open(output_file, mode='w', encoding='utf-8', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(processed_data)

    print(f"Processed data has been saved to {output_file}")

if __name__ == "__main__":
    main()
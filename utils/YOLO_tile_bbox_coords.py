#Sa'doun's modified script for translating bbox coordinates on full images to tiles
#Useful for Labelbox labels-- all others were labeled on tiles

import pandas as pd
import os

# Directory containing the text files
directory = r''   # Replace with the path to your directory

# Create an empty list to store data
data = []

imw = 5472 
imh = 3648 
tlw = 684
tlh = 521
# Iterate through each file in the directory
for filename in os.listdir(directory):
    if filename.endswith('.txt'):  # Process only text files
        file_path = os.path.join(directory, filename)
        with open(file_path, 'r') as file:
            # Read each line from the file
            for line in file:
                line = line.strip()
                if line:  # Skip blank lines
                    # Split the line into individual values
                    values = line.split()
                    
                    # Insert the filename as the first value
                    values.insert(0, filename)
                    
                    # Convert data types
                    values = [values[0]] + [int(values[i]) if i == 1 else float(values[i]) for i in range(1, len(values))]
                    
                    # Append the values to the data list
                    data.append(values)

# Create the DataFrame with specified column names
df = pd.DataFrame(data, columns=['File', 'Class', 'X', 'Y', 'W', 'H'])

df['X'] = df['X'] * imw
df['W'] = df['W'] * imw

# Multiply columns Y and H with imh
df['Y'] = df['Y'] * imh
df['H'] = df['H'] * imh

# Calculate the tile position for X
df['X_tile'] = ((df['X'] // tlw) + 1).astype(int)

# Calculate the tile position for Y
df['Y_tile'] = ((df['Y'] // tlh) + 1).astype(int)

# Calculate the starting coordinates of each tile within the original image
start_x = (df['X_tile'] - 1) * tlw
start_y = (df['Y_tile'] - 1) * tlh

# Update the 'X' and 'Y' columns to represent the location within the tile image
df['X'] = df['X'] - start_x
df['Y'] = df['Y'] - start_y

# # Apply checks for maximum summation of X+W and Y+H
# df['XW_sum'] = df['X'] + df['W']
# df['YH_sum'] = df['Y'] + df['H']

# Apply checks for maximum summation of X+W and Y+H
df['W'] = df.apply(lambda row: min(row['W'], tlw - 1 - row['X']), axis=1)
df['H'] = df.apply(lambda row: min(row['H'], tlh - 1 - row['Y']), axis=1)

# Divide 'X' and 'W' columns by tlw
df['X'] = df['X'] / tlw
df['W'] = df['W'] / tlw

# Divide 'Y' and 'H' columns by tlh
df['Y'] = df['Y'] / tlh
df['H'] = df['H'] / tlh

# Modify the "File" column
df['File'] = df.apply(lambda row: row['File'].split('.')[0] + '_0' + str(row['Y_tile']) + '_0' + str(row['X_tile']) + '.txt', axis=1)

df.drop(df[(df['X'] > 0.99) | (df['Y'] > 0.99)].index, inplace=True)

# Display the modified DataFrame
print(df)

# Create a directory to store the output files
output_directory = r''  # Replace with the path to your desired output directory
os.makedirs(output_directory, exist_ok=True)

# Group the DataFrame by 'File' column
grouped = df.groupby('File')

# Iterate over each unique 'File' value and write the associated values to a file
for filename, group in grouped:
    output_file = os.path.join(output_directory, filename)
    with open(output_file, 'w') as file:
        for _, row in group.iterrows():
            line = f"{int(row['Class'])} {row['X']} {row['Y']} {row['W']} {row['H']}"
            file.write(line + '\n')

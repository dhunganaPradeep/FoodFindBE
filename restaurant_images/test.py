import os

# Directory where your images are located
directory = './'

# Iterate over each file in the directory
for filename in os.listdir(directory):
    # Check if it's a file (not a directory)
    if os.path.isfile(os.path.join(directory, filename)):
        # Split the filename by underscore
        parts = filename.split('_')
        
        # If there are more than two parts (at least two underscores)
        if len(parts) > 2:
            # Join the parts before the second underscore
            new_filename = '_'.join(parts[:2]) + '.' + parts[-1].split('.')[-1]
            
            # Rename the file
            os.rename(os.path.join(directory, filename), os.path.join(directory, new_filename))
            print(f"Renamed {filename} to {new_filename}")

import os

# Print current working directory
print("Current working directory:", os.getcwd())

# List files in the assets directory
print("Files in the assets directory:")
for filename in os.listdir("assets"):
    print(filename)

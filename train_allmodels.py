#Automate executing multiple planned models
import subprocess
import os

# List of training commands
training_commands = [
    'python train.py --img 640 --batch-size -1 --epochs 2 --data zooniverse_4class.yaml --weights yolov5s.pt',
    "python train.py --img 640 --batch-size -1 --epochs 2 --data birddetector.yaml --weights yolov5s.pt",
    # Add more training commands here-- the ones above are short epochs just to test that it turns over correctly
]

# Function to execute a command and capture the output
def run_command(command):
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    while True:
        output = process.stdout.readline().decode().strip()
        if output == '' and process.poll() is not None:
            break
        if output:
            print(output)
    return process.poll()

# Iterate over the training commands
for i, command in enumerate(training_commands, start=1):
    print(f"Training model {i}/{len(training_commands)}")
    print(f"Command: {command}")

    # Execute the command
    return_code = run_command(command)

    if return_code == 0:
        print(f"Model {i}/{len(training_commands)} finished training successfully.")
    else:
        print(f"Model {i}/{len(training_commands)} failed during training.")

    # Clear the terminal
    os.system('cls')

print("All models finished training.")

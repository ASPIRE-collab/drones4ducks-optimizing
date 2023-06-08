import subprocess
import os

# List of training commands
training_commands = [
    "python train.py --img 640 --batch-size -1 --epochs 150 --data data.yaml --weights yolov5s.pt",
    "etc"
    # Add more training commands here
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

# Variables to store the results
results = []

# Iterate over the training commands
for i, command in enumerate(training_commands, start=1):
    print(f"Training model {i}/{len(training_commands)}")
    print(f"Command: {command}")

    # Execute the command
    return_code = run_command(command)

    if return_code == 0:
        print(f"Model {i}/{len(training_commands)} finished training successfully.")
        results.append((command, "Success"))
    else:
        print(f"Model {i}/{len(training_commands)} failed during training.")
        results.append((command, "Failure"))

    # Clear the terminal
    #os.system('cls')

print("All training commands executed.")

# Save the summary to a text file
summary_file = "training_summary.txt"
with open(summary_file, "w") as f:
    for command, result in results:
        f.write(f"Command: {command}\n")
        f.write(f"Result: {result}\n")
        f.write("-" * 20 + "\n")

print(f"Summary saved to {summary_file}.")
#!/bin/python3

import subprocess as sp
import re
import os
import sys

def get_user_input():
    path = str(input("Where to mount?: "))
    while True: 
        if not os.path.isdir(path):
            print("Invalid dir!")
            path = str(input())
            continue
        break
    return path

cmd = ['lsblk', '-l']
output = sp.run(cmd, capture_output=True).stdout.decode().split("\n")

is_partition = re.compile(".*part.*")
partitions = [line.split() for line in output if is_partition.match(line)]

non_mounted = [partition for partition in partitions if len(partition) == 6]

if len(non_mounted) == 0:
    print("There is no non mounted partitions!")
    exit(0)

print(f"There are currently {len(non_mounted)} non mounted partitions")
for i, p in enumerate(non_mounted):
    print(f"{i + 1}) /dev/{p[0]} for {p[3]}")

selection = int(input("Which one do you want to mount?: "))
while True:
    if not (0 < selection <= len(non_mounted)):
        print("Pick good number pls")
        selection = int(input())
        continue
    break

selected_part = non_mounted[selection - 1]

print(f"Your selection is {selected_part[0]}")

if len(sys.argv) > 1 and os.path.isdir(sys.argv[1]):
    path = sys.argv[1]
    print(f"Using cmd arg as path: {path}")
else:
    path = get_user_input()

print(f"Now good path {path}")
print(f"Mounting {selected_part[0]} to {path}...")

sp.run(["sudo", "mount", f"/dev/{selected_part[0]}", path])



import sys

failure = sys.argv[1]

# actions already tried
tried = sys.argv[2].split(",") if len(sys.argv) > 2 and sys.argv[2] else []

# Possible actions
actions = ["retry", "reinstall", "clean"]

# Avoid repeating same action
for action in actions:
    if action not in tried:
        print(action)
        exit()

# If all tried, fallback
print("retry")
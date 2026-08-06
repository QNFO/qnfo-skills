import subprocess
r = subprocess.run(["git", "-C", r"C:\Users\LENOVO\Documents\GitHub\qnfo-skills", "log", "--oneline", "-3"], capture_output=True, text=True)
print(r.stdout)
print(r.stderr)

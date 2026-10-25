import os
from datetime import datetime
from pathlib import Path

load_recursive = ["system", "owner_00"]
output_dir = os.path.join(os.getenv("USERPROFILE"), r"Desktop\LILY-THE-GARDENER")

os.makedirs(output_dir, exist_ok=True)

prompt = ""

for rd in load_recursive:
    for root, dirs, files in os.walk(rd):
        prompt += ("== START root node \"%s\" ==\n" % root)
        for i in os.listdir(root):
            if os.path.isfile(os.path.join(root, i)):
                prompt += ("= START entry node \"%s\" =\n" % i)
                with open(os.path.join(root, i)) as f:
                    for line in f:
                        if line.strip() != "":
                            prompt += (line)
                if not prompt.endswith("\n"):
                    prompt += "\n"
                prompt += ("= END entry node \"%s\" =\n" % i)
        prompt += ("== END root node \"%s\" ==\n" % root)

output_file = os.path.join(output_dir, "MASTER-PROMPT-%s.txt" % str(datetime.now().strftime("%Y-%m-%d-%H-%M-%S")))

with open(output_file, "w") as f:
    f.write(prompt)
    
print(prompt)
print("written to %s" % output_file)
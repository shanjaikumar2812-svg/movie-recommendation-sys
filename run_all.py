import subprocess
import sys

files = [
    "load_movies.py",
    "curd_operation.py",
    "aggregation.py",
    "recommandation.py",
    "visualize.py",
]

for file in files:
    print(f"\n{'='*40}")
    print(f" Running {file}...")
    print(f"{'='*40}")
    
    result = subprocess.run(
        [sys.executable, file],
        capture_output=False
    )
    
    if result.returncode == 0:
        print(f"{file} completed!")
    else:
        print(f" Error in {file} — fix before continuing!")
        break

print("\n All files completed!")
print(" Now run: python app.py")
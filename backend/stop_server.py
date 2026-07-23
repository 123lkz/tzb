import urllib.request
import os, signal, subprocess, sys

port = sys.argv[1] if len(sys.argv) > 1 else "8720"

try:
    urllib.request.urlopen("http://localhost:" + port + "/api/shutdown", data=b"", timeout=5)
    print("API shutdown request sent (port " + port + ")")
    exit(0)
except Exception:
    pass

result = subprocess.run(
    "netstat -ano | findstr :" + port,
    capture_output=True, text=True, shell=True
)
for line in result.stdout.splitlines():
    if "LISTENING" in line:
        pid = line.strip().split()[-1]
        try:
            os.kill(int(pid), signal.SIGTERM)
            print("Killed process " + pid)
        except:
            print("Permission denied, run as admin: taskkill /PID " + pid + " /F")
print("Done")

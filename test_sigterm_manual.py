import signal
import subprocess
import sys


script = """
import signal
import time

def handle_sigterm(signum, frame):
    print("SIGTERM_RECEIVED", flush=True)
    raise SystemExit(0)

signal.signal(signal.SIGTERM, handle_sigterm)

print("PROCESS_READY", flush=True)

while True:
    time.sleep(0.2)
"""

process = subprocess.Popen(
    [sys.executable, "-u", "-c", script],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True,
)

try:
    ready = process.stdout.readline().strip()
    print("Child process:", ready)

    if ready != "PROCESS_READY":
        raise RuntimeError("Child process did not start correctly")

    process.send_signal(signal.SIGTERM)

    try:
        process.wait(timeout=5)
    except subprocess.TimeoutExpired:
        process.kill()
        process.wait()
        raise RuntimeError("Process did not stop after SIGTERM")

    stdout_output = process.stdout.read()
    stderr_output = process.stderr.read()

    print("Child stdout:", stdout_output)
    print("Child stderr:", stderr_output)
    print("Exit code:", process.returncode)
    if process.returncode == 0:
        print("RESULT: SIGTERM HANDLING VERIFIED")
    else:
        print("RESULT: UNEXPECTED EXIT CODE")

finally:
    if process.poll() is None:
        process.kill()
        process.wait()

    process.stdout.close()
    process.stderr.close()

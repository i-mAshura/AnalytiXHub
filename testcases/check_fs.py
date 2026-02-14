print("Hello check")
try:
    with open("testcases/check.txt", "w") as f:
        f.write("Works")
    print("Write success")
except Exception as e:
    print(f"Write failed: {e}")

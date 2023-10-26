import paramiko



# Define the SSH connection parameters
ip_address = '192.168.56.101'
username = 'prne'
password = 'cisco123!'
new_hostname = 'R1'


def connect_to_ssh(ip_address, username, password):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip_address, username=username, password=password,allow_agent=False,look_for_keys=False)
        print(f"SSH connection successful to {ip_address}")
        return ssh
    except paramiko.AuthenticationException:
        print('---FAILURE! Authentication failed, please verify your credentials')
        exit()
    except paramiko.SSHException as sshException:
        print('---FAILURE! Unable to establish SSH connection: ', sshException)
        exit()
    except paramiko.BadHostKeyException as badHostKeyException:
        print('---FAILURE! Unable to verify server\'s host key: ', badHostKeyException)
        exit()

ssh_client = connect_to_ssh(ip_address, username, password)


# If the connection was successful, create a new channel for remote commands
channel = ssh_client.invoke_shell()

# Send the command to modify the device hostname
channel.send('configure terminal\n')
channel.send('hostname ' + new_hostname + '\n')
channel.send('end\n')


# Wait for the command to complete
while not channel.recv_ready():
    pass


# Print the output of the command
print(channel.recv(1024).decode('utf-8'))


# Send a command to the remote device to output the running configuration and save this to a file locally
channel.send('show running-config\n')

# Wait for the command to complete
while not channel.recv_ready():
    pass

# Print the output of the command
print(channel.recv(1024).decode('utf-8'))

# Save the output to a file
with open('running_config.txt', 'w') as f:
    f.write(channel.recv(1024).decode('utf-8'))

# Close the SSH connection
ssh_client.close()




import paramiko
from io import StringIO

command = "uname"

# Update the next three lines with your
# server's information

host = "192.168.10.25"
username = "ubuntu"
password = "coinsdo@123!"
ssh_key = "-----BEGIN OPENSSH PRIVATE KEY-----\nb3BlbnNzaC1rZXktdjEAAAAABG5vbmUAAAAEbm9uZQAAAAAAAAABAAAAMwAAAAtzc2gtZW\nQyNTUxOQAAACDJVtAhOdcL1WCopFrbkD4RVAOzTkzN30yE0iVCIeTOOwAAALBfh2I2X4di\nNgAAAAtzc2gtZWQyNTUxOQAAACDJVtAhOdcL1WCopFrbkD4RVAOzTkzN30yE0iVCIeTOOw\nAAAEB6BNyDlub6t2/OJgdpq0KJDvtG310rcyaSBAp86HUhOclW0CE51wvVYKikWtuQPhFU\nA7NOTM3fTITSJUIh5M47AAAAKHRlY3N0YXRpb25AdGVjc3RhdGlvbnMtTWFjQm9vay1Qcm\n8ubG9jYWwBAgMEBQ==\n-----END OPENSSH PRIVATE KEY-----"

# client = paramiko.client.SSHClient()
# client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
# key_file = StringIO(password)
# client.connect(host, username=username,
#                password=password)
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
key_file = StringIO(ssh_key)
try:
    private_key = paramiko.Ed25519Key.from_private_key(key_file)
except paramiko.SSHException:
    key_file.seek(0)
    private_key = paramiko.RSAKey.from_private_key(key_file)

client.connect(hostname=host, port=22,
               username=username, pkey=private_key)
_stdin, _stdout, _stderr = client.exec_command(command)
print(_stdout.read().decode())
client.close()

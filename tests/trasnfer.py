from drowsypy.transfer import FTPClient

address = "192.168.111.202"
port = 21
username = "testuser"
password = "testpassword"

up_source = "/Users/eunsu/miniconda.sh"
up_destination = "/home/testuser/test/miniconda.sh"

down_source = "/home/testuser/test/ftp_check.txt"
down_destination = "/Users/eunsu/ftp_check.txt"

client = FTPClient(address=address, port=port, username=username, password=password)
client.check_connection()
client.connect()
client.check_connection()

client.check_directory("/home/testuser/test")
client.check_file_path("/home/testuser/test/tmp.txt")
client.download(down_source, down_destination, overwrite=True)
client.upload(up_source, up_destination, overwrite=True)

client.disconnect()

# client = FTP(address=address, port=port, username=username, password=password)
# client.connect()
# #status = client.check_connection()

# client.check_directory("/home/testuser/test")
# client.check_file_path("/home/testuser/test/tmp.txt")

# client.disconnect()
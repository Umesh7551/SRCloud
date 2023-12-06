import bluetooth

# Set the Bluetooth name and port of the RFID reader
rfid_name = 'EMPOSAIR17901'  # Replace with the RFID reader's Bluetooth name
rfid_port = 4  # Replace with the appropriate port number

# Discover nearby Bluetooth devices
devices = bluetooth.discover_devices()
# print(devices)
# Find the RFID reader in the discovered devices
rfid_address = None
for addr in devices:
    if bluetooth.lookup_name(addr) == rfid_name:
        rfid_address = addr
        break

# Check if the RFID reader was found
if rfid_address is None:
    print("RFID reader not found.")
    exit()

# Establish a Bluetooth socket connection
sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
sock.connect((rfid_address, rfid_port))

# Send a command to the RFID reader and receive data
command = b'\x04\x02\x00\x00\x00'
sock.send(command)

# Receive data from the RFID reader
data = sock.recv(1024)
convertedhex = data.hex()
print(convertedhex)

adjustedhex = convertedhex[7:32]
print("RFID Code is: ", adjustedhex)
#print("Received data:", data)

# Close the Bluetooth socket connection
sock.close()
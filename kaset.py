import asyncio
import aioconsole
from bleak import BleakScanner, BleakClient
import random

TARGET_NAME = "Trainning_PAD"
mode = "connect"  # Initial mode
LED_CHAR_UUID = "B2E9FDA1-822C-4729-B8E2-9C35E7630009"
RED_LIGHT = bytes.fromhex("FF0000")
BLUE_LIGHT = bytes.fromhex("0000FF")
OFF_LIGHT = bytes.fromhex("000000")
def randomColor() :
	red = random.randint(0, 255)
	green = random.randint(0, 255)
	blue = random.randint(0, 255)
	hexString = f"{red:02X}{green:02X}{blue:02X}"
	return bytes.fromhex(hexString)
device = []

async def scan_and_connect():
	"""Scans for BLE devices and connects to the target device."""
	global mode
	global device
	while True:
		if mode == "connect":
			print("Scanning for devices... (Press 'r' to switch to running mode)")
			devices = await BleakScanner.discover()
			target_device = next((d for d in devices if d.name == TARGET_NAME), None)
			if target_device:
				print(f"Found target device: {target_device.address}, connecting...")
				client = BleakClient(target_device.address)
				await client.connect()
				device.append(client)
				print("Connected!")
			else:
				print("Device not found.")
		elif mode == "run":
			print("Running... (Press 'r' to switch to connecting mode)")
			for c in device :
				await c.write_gatt_char(LED_CHAR_UUID, randomColor())
				await asyncio.sleep(0.5)
				await c.write_gatt_char(LED_CHAR_UUID, randomColor())
				await asyncio.sleep(0.5)
				await c.write_gatt_char(LED_CHAR_UUID, OFF_LIGHT)
		await asyncio.sleep(0.5)  # Prevent CPU overuse

async def wait_for_key():
	"""Waits for a key press to switch mode."""
	global mode
	while True:
		key = await aioconsole.ainput()  # Wait for user input
		if key.lower() == "r":
			mode = "run" if mode == "connect" else "connect"
			print(f"Switched to {mode} mode!")

async def main():
	await asyncio.gather(scan_and_connect(), wait_for_key())

asyncio.run(main())

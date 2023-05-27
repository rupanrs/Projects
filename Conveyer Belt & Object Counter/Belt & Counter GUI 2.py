import matplotlib.pyplot as plt
import serial

arduino_port = 'COM9'  # Replace 'COM1' with the appropriate port for your Arduino
baud_rate = 9600  # Make sure it matches the baud rate set in the Arduino code

ser = serial.Serial(arduino_port, baud_rate)

x_data = []
y_data = []

while True:
    try:
        line = ser.readline().decode('utf-8').rstrip()
        ir_value = int(line)
        x_data.append(len(x_data) + 1)
        y_data.append(ir_value)
        print(f"IR Value: {ir_value}")
    except KeyboardInterrupt:
        break
    except ValueError:
        continue

plt.plot(x_data, y_data, 'ro-')
plt.xlabel('Time')
plt.ylabel('IR Sensor Value')
plt.title('IR Sensor Data')
plt.grid(True)
plt.draw()  # Draw the plot
plt.pause(0.001)  # Pause briefly to allow the plot to be displayed

plt.show(block=True)  # Keep the plot displayed until the window is closed

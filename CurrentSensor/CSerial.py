import serial
import time
import sqlite3
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Initialize serial connection
arduino = serial.Serial(port='COM3', baudrate=115200, timeout=0.1)
time.sleep(2)  # Wait for connection to establish

# Function to insert data into the database
def insert_data(value):
    conn = sqlite3.connect('Project192.db')
    c = conn.cursor()
    c.execute("INSERT INTO current_points (value) VALUES (?)", (value,))
    conn.commit()
    conn.close()

# Function to fetch data from the database for plotting
def fetch_data():
    conn = sqlite3.connect('Project192.db')
    c = conn.cursor()
    c.execute("SELECT value FROM current_points")
    data = c.fetchall()
    conn.close()
    return data

# Update function for the plot
def update(frame):
    data = fetch_data()
    plt.cla()  # Clear the current axes
    if data:
        plt.plot([x for x in range(len(data))], [y[0] for y in data], marker='o')
    plt.xlabel('Entry Number')
    plt.ylabel('Current (A)')
    plt.title('Real-Time Current Measurement')

# Read data from Arduino and insert into database
def read_from_arduino():
    while True:
        data = arduino.readline()
        if data:
            try:
                current_value = float(data.decode().strip())  # Decode and convert to float
                insert_data(current_value)
                print(current_value)
            except ValueError:
                print("Invalid data received:", data)

# Main function to manage database and plotting
def main():
    # Setup database
    conn = sqlite3.connect('Project192.db')
    c = conn.cursor()
    c.execute('''
              CREATE TABLE IF NOT EXISTS current_points
              (id INTEGER PRIMARY KEY, value FLOAT)
              ''')
    conn.commit()
    conn.close()

    # Initialize plot
    fig = plt.figure()
    ani = FuncAnimation(fig, update, interval=1000)
    plt.tight_layout()

    # Start reading from Arduino in a background thread
    import threading
    thread = threading.Thread(target=read_from_arduino)
    thread.daemon = True  # Allows program to exit if this is the only active thread
    thread.start()

    # Display plot
    plt.show()

if __name__ == "__main__":
    main()

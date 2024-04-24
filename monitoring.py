import Adafruit_DHT
import time
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import matplotlib.pyplot as plt
import matplotlib.animation as animation

i2c = busio.I2C(board.SCL, board.SDA)
ads = ADS.ADS1115(i2c)
channel = AnalogIn(ads, ADS.P0)
channel1 = AnalogIn(ads, ADS.P1)

temp_sensor = Adafruit_DHT.DHT11
gpio_temp = 17

ORIGINAL_CAPACITY_AH = 2.0

def measure_current():
    return 0.5 

total_discharged_ah = 0.0  
discharge_start_time = time.time()
print("discharge_start_time = ",discharge_start_time)

fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 7))

def animate(i, xs, ys, zs, ws):
    # Measure voltage, current, temperature, and humidity
    voltage = channel.voltage/0.2
    print("VOLTAGE:",voltage)
    
    current_a = channel1.voltage
    print("Current:",current_a)
    
    humidity, temperature = Adafruit_DHT.read_retry(temp_sensor, gpio_temp)
    print("Temperature: ",temperature)
    # Update the discharge calculation
    current_time = time.time()
    discharge_start_time = time.time()
    print("current_time= ",current_time)
    print("discharge_start_time1 = ",discharge_start_time)
    
    elapsed_time_h = ( discharge_start_time-current_time )/3600
    print("elapsed_time_h:",elapsed_time_h)
    
    discharged_ah = current_a * elapsed_time_h
    print("discharged_ah:", discharged_ah)
    
    total_discharged_ah = 0.0
    total_discharged_ah += discharged_ah  # Accumulate the discharged capacity
    print("total_discharged_ah:",total_discharged_ah)
    
    discharge_start_time = current_time  # Reset the timer for the next measurement
    
    
    # Estimate battery health based on discharged capacity
    current_capacity_ah = ORIGINAL_CAPACITY_AH - total_discharged_ah
    
    battery_health_percentage = (current_capacity_ah / ORIGINAL_CAPACITY_AH) * 100
    print("battery_health_percentage",battery_health_percentage)
    
    xs.append(i * 2)  # Append the time interval (2 seconds)
    ys.append(voltage)
    zs.append(temperature if temperature is not None else float('nan'))  # Use nan for missing values
    ws.append(battery_health_percentage)
    
    xs = xs[-20:]
    ys = ys[-20:]
    zs = zs[-20:]
    ws = ws[-20:]

    # Clear and plot the data
    ax1.clear()
    ax2.clear()
    ax3.clear()

    ax1.plot(xs, ys, 'r', label='Voltage (V)')
    ax2.plot(xs, zs, 'b', label='Temperature (°C)')
    ax3.plot(xs, ws, 'g', label='Battery Health (%)')

    # Format the plots
    ax1.set_ylabel('Voltage (V)')
    ax2.set_ylabel('Temperature (°C)')
    ax3.set_ylabel('Battery Health (%)')
    ax3.set_xlabel('Time (seconds)')

    # Add legends
    ax1.legend(loc='upper left')
    ax2.legend(loc='upper left')
    ax3.legend(loc='upper left')

    # Add a grid
    ax1.grid(True)
    ax2.grid(True)
    ax3.grid(True)
    
    
xs = []
ys = []
zs = []
ws = []

# Set up plot to call animate() function periodically
ani = animation.FuncAnimation(fig, animate, fargs=(xs, ys, zs, ws), interval=2000)
plt.tight_layout()
plt.show()

def animate(i, xs, ys):
    # Measure voltage
    voltage = channel.voltage / 0.2
    #print("VOLTAGE:", voltage)
    
    # Send voltage data to ThingSpeak
    ts_url = 'https://api.thingspeak.com/update?api_key=T68GQEGZIZHTH86H&field1=0' + str(voltage)
    response = requests.get(ts_url)
    print("ThingSpeak Response:", response.text)
    
    #xs.append(i * 2)  # Append the time interval (2 seconds)
    ys.append(voltage)
    
    #xs = xs[-20:]
    #ys = ys[-20:]

    # Clear and plot the data
    ax1.clear()
    ax1.plot(xs, ys, 'r', label='Voltage (V)')
    
    # Format the plot
    ax1.set_ylabel('Voltage (V)')
    ax1.set_xlabel('Time (seconds)')
    ax1.legend(loc='upper left')
    ax1.grid(True)


time.sleep(2);

# Weather & clock station with simple Web interface

## Project description

The project aims to create a smart alarm clock based on Raspberry Pi Zero. The device displays the current time, date, and weather data from a BME280 sensor (temperature, humidity, pressure). The alarm can be set using physical buttons as well as through a web interface.

## Functionality

### Display information
- **Time and date:** Switch between displaying the current time and date and weather measurements.
- **Temperature, humidity, and pressure:** Data from the BME280 sensor.

### Alarm clock
- **Setting the alarm:** Enter alarm setting mode using buttons.
- **Increment and decrement:** Adjust the alarm hour value.
- **Confirmation:** Confirm alarm settings.

### Buzzer
- **Buzzer activation:** Enable the buzzer when the alarm goes off.
- **Buzzer deactivation:** Turn off the buzzer using any button press or automatically after 20 seconds.

### Web interface
- **Setting the alarm:** Ability to set the alarm through the web interface.
- **Turning off the alarm:** Disable the alarm via the web interface button.
- **Temperature refresh:** Manually refresh temperature data.
- **Data update:** Automatic data update every 5 seconds.

### LED indicators
- **Temperature condition indication:** LED indicators showing temperature conditions:
  - Red - above 22°C
  - Yellow - below 18°C
  - Green - between 18°C and 22°C

## Project execution

### Physical Components
- **Raspberry Pi Zero:** Main computing unit.
- **16 x 2 LCD Screen:** Information display.
- **Buttons:** Five buttons for interaction.
- **Buzzer:** Sound alarm output.
- **Potentiometer:** LCD screen contrast control.
- **BME280 Sensor:** Measures temperature, humidity, and pressure.
- **LEDs x 3 + 330Ω resistors x 3:** Temperature condition indicators.

### Software
- **Python with datetime library:** Retrieves current time.
- **Website:** Interface for setting the alarm and interacting with the device.
- **HTML, CSS, JavaScript:** Technologies used for the web interface.
- **LCD library:** Handles LCD screen output.
- **BME280 library:** Reads data from the sensor.
- **Web interface script:** Communicates between the device and the web page.

## Program Code

### Python
- **Functions:**
  - `play` and `buzz`: Generates buzzer signals.
  - `set_alarm_p`: Sets the alarm using buttons.
  - `display_date_time`: Displays date and time on the LCD.
  - `display_temperature`: Displays temperature, humid

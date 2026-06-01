from machine import Pin
import time

# LED Configuration (using pins 2,4,5,13,14,21,27,18)
led_pins = [2, 4, 5, 13, 14, 21, 27, 18]
leds = [Pin(pin, Pin.OUT) for pin in led_pins]

# Turn off all lamps before beginning
for led in leds:
    led.value(0)

# Button Configuration (using recommended input pins 34,35)
entrance_btn = Pin(34, Pin.IN, Pin.PULL_UP)
exit_btn = Pin(35, Pin.IN, Pin.PULL_UP)

# System Variables
car_count = 0
MAX_CARS = 8
last_entrance_state = entrance_btn.value()
last_exit_state = exit_btn.value()
DEBOUNCE_DELAY = 50  # ms

def update_display():
    """Update LEDs to reflect current car count"""
    for i, led in enumerate(leds):
        led.value(1 if i < car_count else 0)
    print(f"Total cars: {car_count}")  # Debug output

def handle_button(btn, last_state, action):
    """Handle button press with debounce"""
    current_state = btn.value()
    if current_state != last_state:
        time.sleep_ms(DEBOUNCE_DELAY)
        current_state = btn.value()
        if current_state == 0:  # Active-low pressed
            action()
    return current_state

def increment_count():
    """Process entrance button press"""
    global car_count
    if car_count < MAX_CARS:
        car_count += 1
        update_display()

def decrement_count():
    """Process exit button press"""
    global car_count
    if car_count > 0:
        car_count -= 1
        update_display()

# Initialize display
update_display()

# Main loop
while True:
    last_entrance_state = handle_button(
        entrance_btn, 
        last_entrance_state, 
        increment_count
    )
    
    last_exit_state = handle_button(
        exit_btn,
        last_exit_state,
        decrement_count
    )
    
    time.sleep_ms(1)
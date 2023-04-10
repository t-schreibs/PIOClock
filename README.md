# PIOClock
A simple square wave clock for the Raspberry Pi Pico.

## Usage
To instantiate and use a PIO Clock:
1. Import `PIOClock` at the top of your script.
2. Use `clock = PIOClock.Clock(<state_machine_id>, <pin_number>)` to instantiate a new clock with the provided state machine and pin.
    - State machine IDs range from 0-7, and each clock will need a unique state machine ID.
    - Each clock will also require a unique pin number.
3. Set the hertz value of a clock with `clock.set(<hertz>)`.
## Testing
This repository includes a [testing class](ClockTest.py). Copy over the `PIOClock.py` file to a Pi Pico, save `ClockTest.py` as `main.py` in the root directory of the Pico, and then you can run it to evaluate the PIO Clock class.
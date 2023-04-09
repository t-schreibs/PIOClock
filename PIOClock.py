import machine, random, time
from rp2 import PIO, StateMachine, asm_pio


# Assembly code program for the PIO square oscillator
# Thanks to Ben Everard at HackSpace for the basis of this program:
# https://hackspace.raspberrypi.com/articles/raspberry-pi-picos-pio-for-mere-mortals-part-3-sound
@asm_pio(sideset_init=PIO.OUT_LOW)
def square_prog():
    # Initialize x & y variables - these are used to count down the
    # loops which set the length of the square wave's cycle
    label("restart")
    pull(noblock).side(0)
    mov(x, osr)
    mov(y, isr)
    # Start loop
    # Here, the pin is low, and it will count down y
    # until y=x, then set the pin high and jump to the next section
    label("up_loop")
    jmp(x_not_y, "skip_up")
    nop().side(1)
    jmp("down")
    label("skip_up")
    jmp(y_dec, "up_loop")
    # Mirror the above loop, but with the pin high to form the second
    # half of the square wave
    label("down")
    mov(y, isr)
    label("down_loop")
    jmp(x_not_y, "skip_down")
    nop().side(0)
    jmp("restart")
    label("skip_down")
    jmp(y_dec, "down_loop")


# Class for managing a state machine running the PIO oscillator program
class PIOClock:
    def __init__(self, state_machine_id, pin_number):
        # PIO settings
        max_count = 50_000_000
        count_freq = 50_000_000
        self._sm = StateMachine(
            state_machine_id,
            square_prog,
            freq=2 * count_freq,
            sideset_base=machine.Pin(pin_number),
        )
        # Use exec() to load max count into ISR
        self._sm.put(max_count)
        self._sm.exec("pull()")
        self._sm.exec("mov(isr, osr)")
        self._sm.active(1)
        self._max_count = max_count
        self._count_freq = count_freq

    def set(self, hertz):
        value = self.get_pitch(hertz)
        # Minimum value is -1 (completely turn off), 0 actually still
        # produces a narrow pulse
        value = self.clamp(value, -1, self._max_count)
        self._sm.put(value)

    def clamp(self, num, min_value, max_value):
        return max(min(num, max_value), min_value)

    # Converts Hertz to the value the state machine running the PIO
    # program needs
    def get_pitch(self, hertz):
        return int(-1 * (((self._count_freq / hertz) - (self._max_count * 4)) / 4))


class ClockTest:
    def __init__(self):
        self.clocks = [
            PIOClock(0, 21),
            PIOClock(1, 20),
            PIOClock(2, 16),
            PIOClock(3, 17),
            PIOClock(4, 18),
            PIOClock(5, 19),
        ]

    def main(self):
        while True:
            for clock in self.clocks:
                clock.set(random.randint(1, 10000))
            time.sleep(5)


# Test script execution
if __name__ == "__main__":
    ClockTest().main()
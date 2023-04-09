import PIOClock, random, time


class ClockTest:
    def __init__(self):
        self.clocks = [
            # Defaults for EuroPi - change these for your configuration
            PIOClock.Clock(0, 21),
            PIOClock.Clock(1, 20),
            PIOClock.Clock(2, 16),
            PIOClock.Clock(3, 17),
            PIOClock.Clock(4, 18),
            PIOClock.Clock(5, 19),
        ]

    # Tests a slide from the minHertz to the maxHertz and back again on the first clock
    def TestSlide(self, interval, minHertz, maxHertz):
        while True:
            hertz = minHertz
            while hertz < maxHertz:
                self.clocks[0].set(hertz)
                hertz += interval
            while hertz > minHertz:
                self.clocks[0].set(hertz)
                hertz -= interval

    # Sets a constant value output for all clocks
    def TestPitch(self, hertz):
        for clock in self.clocks:
            clock.set(hertz)
        while True:
            time.sleep(5)

    # Sets a random value for each clock every 5 seconds
    def TestRandomPitches(self, minHertz, maxHertz):
        while True:
            for clock in self.clocks:
                clock.set(random.uniform(minHertz, maxHertz))
            time.sleep(5)

    def main(self):
        # Select the test loop you'd like to run here:
        self.TestRandomPitches(1, 5000)
        # self.TestPitch(50)
        # self.TestSlide(0.25, 1, 5000)


# Test script execution
if __name__ == "__main__":
    ClockTest().main()

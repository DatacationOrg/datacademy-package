"""Module containing an animation thread."""
from collections.abc import Callable
from threading import Thread
from time import sleep, time


class TextAnimation(Thread):
    """Class to animate console text using a Thread."""

    def __init__(self, func: Callable[[int], str], frequency: int = 10) -> None:
        """Create a new animation thread.

        Args:
            func (Callable[[int], str]): Animation function from step to string.
            frequency (int, optional): Amount of string updates per second. Defaults to 10.
        """
        super().__init__(daemon=True)
        self.func = func
        self.step = 0
        self.speed = 1.0 / frequency
        self.wait = min(0.1, self.speed)
        self.should_stop = False
        self.longest_line = 0

    def run(self) -> None:
        """Run the animation."""
        last_run = time() - self.speed
        while not self.should_stop:
            if time() - self.speed >= last_run:
                last_run = time()
                text = self.func(self.step)
                print(' ' * self.longest_line, end='\r')
                print(text, end='\r', flush=True)
                self.longest_line = max(self.longest_line, len(bytes(text, encoding='utf-8')))
                self.step += 1

            sleep(max(0, self.wait - (time() - last_run)))
        print(' ' * self.longest_line, end='\r', flush=True)

    def stop(self, text: str | None = None) -> None:
        """Stop the animation. Blocks until animation is stopped.

        Args:
            text (str | None, optional): A text to print when the animation is complete. Defaults to None.
        """
        self.should_stop = True
        if text is not None:
            print(text, flush=True)
        self.join()

    @staticmethod
    def start_new(func: Callable[[int], str], frequency: int = 10) -> 'TextAnimation':
        """Create a new AnimationThread and immediately start it.

        Args:
            func (Callable[[int], str]): Animation function from step to string.
            frequency (int, optional): Amount of string updates per second. Defaults to 10.

        Returns:
            AnimationThread: Started AnimationThread.
        """
        animation = TextAnimation(func, frequency=frequency)
        animation.start()
        return animation

    @staticmethod
    def loop_list(loop_list: str | list[str], frequency: int = 10) -> 'TextAnimation':
        """Create an animation by looping a list.

        Args:
            loop_list (str | list[str]): List to loop.
            frequency (int, optional): Amount of string updates per second. Defaults to 10.

        Returns:
            AnimationThread: _description_
        """
        def _loop(step: int) -> str:
            return loop_list[step % len(loop_list)]

        return TextAnimation.start_new(_loop, frequency=frequency)

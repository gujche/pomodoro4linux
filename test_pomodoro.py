from unittest import TestCase, main
from optparse import OptionValueError

from pomodoro import Timer, UserInterface
from pomodoro_parser import check_positive_integer

class TestParse(TestCase):
    def test_raise_with_negative(self):
        number = -5
        self.assertRaises(
            OptionValueError,
            check_positive_integer,
            '-w',
            '-r',
            number
        )


    def test_raise_with_0(self):
        number = 0
        self.assertRaises(
            OptionValueError,
            check_positive_integer,
            '-w',
            '-r',
            number
        )


    def test_returns_the_value_5(self):
        number = 5
        expected = 5
        returned = check_positive_integer('-w', '-r', number)
        self.assertEqual(expected,  returned)


    def test_returns_the_value_500(self):
        number = 500
        expected = 500
        returned = check_positive_integer('-w', '-r', number)
        self.assertEqual(expected, returned)



class TestUI(TestCase):
    def setUp(self):
        timer = Timer(300, 200)
        self.ui = UserInterface(timer)


    def test_seconds_to_minutes_300(self):
        time_left = 300
        returned = self.ui.seconds_to_minutes(time_left)
        self.assertEqual((5, 0), returned)


    def test_seconds_to_minutes_1500(self):
        time_left = 1500
        returned = self.ui.seconds_to_minutes(time_left)
        self.assertEqual((25, 0), returned)


    def test_seconds_to_minutes_1000(self):
        time_left = 1000
        returned = self.ui.seconds_to_minutes(time_left)
        self.assertEqual((16, 40), returned)


    def test_seconds_to_minutes_900(self):
        time_left = 900
        returned = self.ui.seconds_to_minutes(time_left)
        self.assertEqual((15, 0), returned)


    def test_seconds_to_minutes_005(self):
        time_left = 005
        returned = self.ui.seconds_to_minutes(time_left)
        self.assertEqual((0, 5), returned)


    def test_seconds_to_minutes_150(self):
        time_left = 150
        returned = self.ui.seconds_to_minutes(time_left)
        self.assertEqual((2, 30), returned)



if __name__ == '__main__':
    main()
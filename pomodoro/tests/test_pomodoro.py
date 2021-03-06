"""
    Test all the classes of pomodoro4linux.
"""

from unittest import TestCase
from optparse import OptionValueError

from pomodoro.pomodoro import Timer
from pomodoro.ui import UI
from pomodoro.utils.parser import check_positive_integer
from pomodoro.utils.utils import seconds_to_minutes


class TestParser(TestCase):
    """
        Checks exclusively cases of parsing command-line.
    """
    def test_raise_with_negative(self):
        """
            Test if check_positive_integer returns a raise with
            negative number.
        """
        number = -5
        self.assertRaises(
            OptionValueError,
            check_positive_integer,
            '-w',
            '-r',
            number
        )

    def test_raise_with_0(self):
        """
            Test if check_positive_integer returns a raise with
            a neutral number.
        """
        number = 0
        self.assertRaises(
            OptionValueError,
            check_positive_integer,
            '-w',
            '-r',
            number
        )

    def test_returns_the_correct_value(self):
        """
            Test if check_positive_integer returns the correct number.
        """
        number = 5
        expected = 5
        returned = check_positive_integer('-w', '-w', number)
        self.assertEqual(expected,  returned)


class TestUtils(TestCase):
    """
        Checks exclusively utils
    """
    def setUp(self):
        """
            Override the method setUp of TestCase.
            I cannot take this name better :(
        """
        timer = Timer(300, 200)
        self.user_interface = UI(timer)

    def test_seconds_to_minutes(self):
        """
            Test if returns 8 minutes and 20 seconds.
        """
        time_left = 500
        returned = seconds_to_minutes(time_left)
        self.assertEqual((8, 20), returned)


class TestTimer(TestCase):
    """
        Checks exclusively timer.
    """
    def setUp(self):
        """
            Override the method setUp of TestCase.
            I cannot take this name better :(
        """
        self.test_pomodoro = Timer()

    def test_start(self):
        """
            When call the function start the expected value is running = True
        """
        time_left = 1500
        returned = seconds_to_minutes(time_left)
        self.assertEqual((25, 0), returned)
        self.assertFalse(self.test_pomodoro.running)
        self.test_pomodoro.start()
        self.assertTrue(self.test_pomodoro.running)

    def test_pause(self):
        """
            When call the function pause the expected value is running = False
        """
        time_left = 1000
        returned = seconds_to_minutes(time_left)
        self.assertEqual((16, 40), returned)
        self.test_pomodoro.pause()
        self.assertFalse(self.test_pomodoro.running)

    def test_update_running(self):
        """
            When update is called with running = True the expected vale
            is time_left - 1
        """
        time_left = 900
        returned = seconds_to_minutes(time_left)
        self.assertEqual((15, 0), returned)
        self.test_pomodoro.time_left = 12
        self.test_pomodoro.running = True
        self.test_pomodoro.update()
        self.assertEqual(self.test_pomodoro.time_left, 11)

    def test_update_not_running(self):
        """
            When update is called with running = False the expected vale
            is work_time
        """
        time_left = 005
        returned = seconds_to_minutes(time_left)
        self.assertEqual((0, 5), returned)
        work_time = 1500
        self.test_pomodoro.running = False
        self.test_pomodoro.update()
        self.assertEqual(self.test_pomodoro.time_left, work_time)

    def test_update_running_and_not_time_left(self):
        '''
        When rest timer ends time left starts again with work time
        '''
        time_left = 900
        returned = seconds_to_minutes(time_left)
        self.test_pomodoro.time_left = 0
        self.test_pomodoro.running = True
        self.test_pomodoro.work_time = 500
        self.test_pomodoro.update()

        self.assertEqual((15, 0), returned)
        self.assertEqual(self.test_pomodoro.time_left, 500)


class TestUI(TestCase):
    """
        Checks exclusively user interface.
    """

    def setUp(self):
        self.timer = Timer()
        self.UI = UI(self.timer)

    def test_function_init(self):
        '''
        After init the menu and quit item exists and current status has to be 0
        '''
        self.assertEqual(self.UI.current_status, 0)
        self.assertTrue(self.UI.menu)
        self.assertTrue(self.UI.quit_item)

    def test_start_timer(self):
        '''
        Start timer sets current status = 0
        '''
        current_status = 0
        self.UI.start_timer()
        self.assertEqual(current_status, self.UI.current_status)

    def test_rest_icon_with_status_1(self):
        '''
        When status = 1 rest icon has to be displayed
        '''
        self.UI.current_status = 1
        self.UI._set_icon()
        self.assertEqual(self.UI.status_icon.get_title(), 'rest.png')

    def test_work_icon_with_status_0(self):
        '''
        When status = 0 work icon has to be displayed
        '''
        self.UI.current_status = 0
        self.UI._set_icon()
        self.assertEqual(self.UI.status_icon.get_title(), 'work.png')

    def test_pause_timer_changes_status(self):
        '''
        Assert status changes when call pause timer
        '''
        self.UI.current_status = 0
        self.UI.pause_timer()
        self.assertEqual(self.UI.current_status, 1)

    def test_update_timer_changes_status_icon(self):
        '''
        Update timer has to the change the icon work/rest
        '''
        self.UI.current_status = 0
        self.timer.time_left = 15
        self.UI.update_timer()

        tooltip_text = self.UI.status_icon.get_tooltip_text()
        self.assertTrue(tooltip_text.startswith('Pomodoro4linux'))

    def test_update_timer_sets_the_dialog_visible(self):
        '''
        Update timer sets the dialog visible when needed
        '''
        self.UI.current_status = 0
        self.timer.time_left = 0
        self.UI.update_timer()
        self.assertTrue(self.UI.dialog.get_visible)

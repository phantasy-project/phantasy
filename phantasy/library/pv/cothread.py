# encoding: UTF-8

"""
Utilities and extensions for the `cothread`_ library.

.. cothread: http://controls.diamond.ac.uk/downloads/python/cothread

.. moduleauthor:: Dylan Maxwell <maxwelld@frib.msu.edu>
"""

import subprocess
import threading

import cothread


class Popen(object):
    """
    Utility for integrating the standard Python Popen class with
    the cothread library's synchronization primitives. The API is
    designed to be the same of the standard Popen.
    """
    def __init__(self, *args, **kwargs):
        """
        Initialize the Popen class by creating a new subprocess.

        All arguments are passed unaltered to the underlying subprocess
        `Popen`_ constructor

        .. Popen: https://docs.python.org/2/library/subprocess.html#popen-constructor
        """
        self._process = subprocess.Popen(*args, **kwargs)
        self._output = None
        self._event = None


    def communicate(self, input=None):
        """Start a real OS thread to wait for process communication.
        """
        # To manintain compatibility with the standard library
        # the 'input' keyword argument is used which redefines
        # the builtin function.
        #   pylint: disable=redefined-builtin
        if self._event is None:
            self._event = cothread.Event()
            threading.Thread(target=self._communicate_thread,
                             args=(input,)).start()
        elif input is not None:
            raise RuntimeError("Popen: Communicate method already called")
        self._event.Wait()
        return (self._output[0], self._output[1], self._process.poll())


    def _communicate_thread(self, input_):
        """Executes in separate OS thread. Wait for communication
           then return the output to the cothread context.
        """
        output = self._process.communicate(input_)
        cothread.Callback(self._communicate_callback, output)


    def _communicate_callback(self, output):
        """Record the output and then signal other cothreads.
        """
        self._output = output
        self._event.Signal()


    def wait(self):
        """Wait for the process to complete and result the exit code.
        """
        self.communicate()
        return self._process.poll()


    def terminate(self):
        """Send the terminate signal. See subprocess.Popen.terminate()
        """
        self._process.terminate()


    def kill(self):
        """Send the kill signal.  See subprocess.Popen.kill()
        """
        self._process.kill()

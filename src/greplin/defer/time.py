# Copyright 2011 The greplin-twisted-utils Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Time utility functions."""

from greplin.defer import base

from twisted.internet import defer

import random


def sleep(seconds):
  """
  Returns a deferred that will call after the specified number of seconds
  have passed. It callsback with True to indicate cancellation.
  """
  return Sleep(seconds)



# pylint is just wrong about this being an old style class.  # pylint: disable=E1001
class Sleep(base.LowMemoryDeferred):
  """Sleep object."""

  __slots__ = ('_delayedCall',)


  def __init__(self, seconds):
    base.LowMemoryDeferred.__init__(self)

    from twisted.internet import reactor
    self._delayedCall = reactor.callLater(seconds, self.callback, None)


  def cancel(self):
    """Stops sleeping."""
    self._delayedCall.cancel()
    self.callback(True)


  def describeDeferred(self):
    """Describes this Deferred."""
    return 'sleep(%f)' % self._delayedCall.time



def timeoutDeferred(seconds, deferred):
  """Returns a new deferred that returns the results of the first deferred, or errs back if on timeout."""
  if deferred.called:
    return deferred

  from twisted.internet import reactor
  timeout = reactor.callLater(seconds, lambda: defer.timeout(deferred))

  result = defer.Deferred()
  result.addCallback(lambda result: timeout.cancel() or result)
  deferred.chainDeferred(result)
  return result



class SleepManager(object):
  """Manages the amount of time to sleep between iterations of a task."""

  def __init__(self, minSleep = 60, maxSleep = 60 * 10, increment = 60, jitter = 0):
    """Initializes the SleepManager.

    Args:
      minSleep: the starting amount of seconds to sleep
      maxSleep: the maximum amount of seconds to sleep
      increment: the number of seconds to increase the delay each time
      jitter: if non-zero, a random floating point number of seconds up to this number will be added to the delay.
              This is useful to help prevent many separate SleepManager objects from getting in sync.
    """
    self.__minSleep = minSleep
    self.__maxSleep = maxSleep
    self.__increment = increment
    self.__jitter = jitter
    self.delay = self.__minSleep


  def reset(self):
    """Reset the delay, usually after an iteration with updated data."""
    self.delay = self.__minSleep


  def sleep(self):
    """Returns a deferred that sleeps the current amount of delay."""
    delayTime = self.delay
    if self.__jitter:
      delayTime += random.random() * self.__jitter
    d = sleep(delayTime)
    self.delay = min(self.delay + self.__increment, self.__maxSleep)
    return d

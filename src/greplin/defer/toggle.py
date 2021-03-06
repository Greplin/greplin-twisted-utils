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

"""A single-fire event that can have many observers."""

from greplin.defer import event

from twisted.internet import defer



class DeferredToggle(object):
  """A single-fire event that can have many observers."""

  def __init__(self):
    self.__event = event.DeferredEvent()
    self.__done = False
    self.__result = None


  def addListener(self):
    """Adds a listener to the event, returning a deferred that will be fired the next time the event is fired."""
    if self.__done:
      return defer.succeed(self.__result)
    else:
      return self.__event.addListener()


  def fire(self, result = None):
    """Fires the event, calling back each listener."""
    assert not self.__done
    self.__done = True
    self.__event.fire(result)
    del self.__event


  def isFired(self):
    """Whether the event has already been fired."""
    return self.__done
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

"""Tests for the StepTask class."""

from twisted.internet import defer

import unittest

from greplin.defer import queue



class MaxSizeQueueTest(unittest.TestCase):
  """Tests for MaxSizeQueueTest."""

  def testBasics(self):
    """Tests the basics of a MaxSizeQueue."""
    q = queue.MaxSizeQueue(5)
    self.assertEquals(0, len(q))
    self.assertEquals(False, q.isFull())

    self.assertEquals(None, q.push(1, 2, 3))
    self.assertEquals(3, len(q))

    self.assertEquals(None, q.push(4))
    self.assertEquals(4, len(q))

    deferred = q.push(5)
    self.assertEquals(False, deferred.called)
    self.assertEquals(5, len(q))
    self.assertEquals(True, q.isFull())

    anotherDeferred = q.push(6)
    self.assertEquals(False, anotherDeferred.called)
    self.assertEquals(6, len(q))
    self.assertEquals(True, q.isFull())

    self.assertNotEquals(deferred, anotherDeferred)

    self.assertEquals([1, 2, 3], q.shiftMany(3))
    self.assertEquals(3, len(q))
    self.assertEquals(True, deferred.called)
    self.assertEquals(True, anotherDeferred.called)
    self.assertEquals(False, q.isFull())

    self.assertEquals(None, q.push(7))
    self.assertEquals(4, len(q))

    self.assertEquals(4, q.shift())
    self.assertEquals(3, len(q))



class MaxSizeDeferredQueueTest(unittest.TestCase):
  """Tests for MaxSizeDeferredQueueTest."""

  def setUp(self):
    """Sets up the test."""
    self.log = []
    self.queue = queue.MaxSizeDeferredQueue(backlog=2, maxSize=3)


  def call(self, fn, *args):
    """Calls the function with the given name and args and logs various related events."""
    desc = ' '.join([fn] + list(args))
    self.log.append(desc)
    result = getattr(self.queue, fn)(*args)
    if isinstance(result, defer.Deferred):
      self.log.append('result: Deferred')
      result.addCallback(lambda _: self.log.append('callback ' + desc))
    else:
      self.log.append('result: %s' % result)


  def testBasics(self):
    """Tests the basics of a MaxSizeDeferredQueue."""
    self.call('push', '1')
    self.call('push', '2')
    self.call('push', '3')
    self.call('push', '4')
    self.call('shift')
    self.call('shift')
    self.call('shift')
    self.call('shift')
    self.call('shift')
    self.call('shift')
    self.assertRaises(defer.QueueUnderflow, self.queue.shift)
    self.call('push', '5')
    self.call('push', '6')

    self.assertEquals([
      'push 1',
      'result: None',
      'push 2',
      'result: None',
      'push 3',
      'result: Deferred',
      'push 4',
      'result: Deferred',
      'shift',
      'result: 1',
      'shift',
      'callback push 3',
      'callback push 4',
      'result: 2',
      'shift',
      'result: 3',
      'shift',
      'result: 4',
      'shift',
      'result: Deferred',
      'shift',
      'result: Deferred',
      'push 5',
      'callback shift',
      'result: None',
      'push 6',
      'callback shift',
      'result: None'
    ], self.log)



class DeferredPriorityQueueTest(unittest.TestCase):
  """Tests for DeferredPriorityQueue."""


  def setUp(self):
    """Sets up the test."""
    self.log = []
    self.queue = queue.DeferredPriorityQueue(sortKey=lambda e: e)


  def call(self, fn, *args):
    """Calls the function with the given name and args and logs various related events."""
    desc = ' '.join([fn] + list(args))
    self.log.append(desc)
    result = getattr(self.queue, fn)(*args)
    if isinstance(result, defer.Deferred):
      self.log.append('result: Deferred')
      result.addCallback(lambda res: self.log.append('callback ' + desc + " returned " + res))
    else:
      self.log.append('result: %s' % result)


  def testBasics(self):
    """Test the basics of a deferred priority queue."""
    self.call('get')
    self.call('put', '1')
    self.call('put', '2')
    self.call('get')
    self.call('put', '3')
    self.call('put', '6')
    self.call('put', '4')
    self.call('put', '5')
    self.call('get')
    self.call('get')
    self.call('put', '7')
    self.call('put', '1')
    self.call('get')
    self.call('get')
    self.call('get')
    self.call('get')
    self.assertEquals([
       "get",
       "result: Deferred",
       "put 1",
       "callback get returned 1",
       "result: None",
       "put 2",
       "result: None",
       "get",
       "result: Deferred",
       "callback get returned 2",
       "put 3",
       "result: None",
       "put 6",
       "result: None",
       "put 4",
       "result: None",
       "put 5",
       "result: None",
       "get",
       "result: Deferred",
       "callback get returned 3",
       "get",
       "result: Deferred",
       "callback get returned 4",
       "put 7",
       "result: None",
       "put 1",
       "result: None",
       "get",
       "result: Deferred",
       "callback get returned 1",
       "get",
       "result: Deferred",
       "callback get returned 5",
       "get",
       "result: Deferred",
       "callback get returned 6",
       "get",
       "result: Deferred",
       "callback get returned 7"
      ], self.log)

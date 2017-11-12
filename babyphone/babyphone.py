import os
import tempfile
import time

import sound
import webbrowser

import numpy as np
import matplotlib.pyplot as plt


TEL = 'echo123'  # your number here


class Babyphone:

  SECONDS = 2
  THRESHOLD = -20
  DEBUG = False

  def __init__(self, phone):
    self.url = 'skype:{}?call'.format(phone)
    self.threshold = self.THRESHOLD
    self._t = []
    self._avg = []
    self._peak = []
  
  def start(self, play=False):
    while True:
      self.file = tempfile.mkstemp('.m4a')[1]
      print(self.file)
      self._recorder = sound.Recorder(self.file)
      self._recorder.record(self.SECONDS)
      
      # loop clips
      wait_until(self.finished, self.SECONDS + 1, 0.1)
      self._stats()
      
      if play and self.DEBUG:
        print('Replaying...',)
        player = sound.Player(self.file)
        player.play()
        print(player.duration)
      
      os.remove(self.file)
      
      #if threshold reached, call
      if self.louder_than():
        if self.DEBUG:
          print('🚼 CALLING MUMMY !!! 🔔🔔🔔')
        else:
          self._call()

  def finished(self):
    self._collect(self._recorder.meters)
    return not self._recorder.recording
  
  def louder_than(self):
    peak = np.array(self._peak)
    mean = np.mean(peak[-30:])
    return mean > self.threshold

  def _collect(self, meters):
    if meters['peak'][0] <= -120:
      return # skip initial values
    if not self._t:
      self._t.append(0)
    else:
      self._t.append(self._t[-1] + 1)
    self._avg.append(meters['average'][0])
    self._peak.append(meters['peak'][0])
  
  def _stats(self):
    y = list(zip(self._avg, self._peak))
    plt.plot(self._t, y)
    plt.xlabel('meter point')
    plt.ylabel('volume')
    plt.legend(['average', 'peak'], loc='lower center')
    plt.title('recording')
    plt.grid()
    plt.show()

  def _call(self):
    webbrowser.open(self.url)


def wait_until(somepredicate, timeout, period=0.25, *args, **kwargs):
  mustend = time.time() + timeout
  while time.time() < mustend:
    if somepredicate(*args, **kwargs): return True
    time.sleep(period)
  return False


def main():
  babyphone = Babyphone(TEL)
  babyphone.threshold = -10
  babyphone.DEBUG = True
  babyphone.start()#play=True)


if __name__ == '__main__':
  main()


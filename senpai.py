import sys
import json

import win32pipe, win32file, win32api

from threading import Thread, Lock
from event import buildEvent

class SENPAI:
   def __init__ (self):
      self.pipe = None

   def __enter__ (self):
      self.open()
      return self

   def __exit__ (self, type, value, traceback):
      self.close()

   def open (self):
      self.pipe = win32file.CreateFile(r"\\.\pipe\SEN_P-AI", win32file.GENERIC_READ | win32file.GENERIC_WRITE, 0, None, win32file.OPEN_EXISTING, 0, None)

   def close (self):
      win32api.CloseHandle(self.pipe)

   def readEvent (self):
      data = win32file.ReadFile(self.pipe, 4)
      size = int.from_bytes(data[1],byteorder="little",signed=True)
      data = win32file.ReadFile(self.pipe, size)
      raw = data[1].decode('utf-8')
      return buildEvent(json.loads(raw))

class ThreadSENPAI:
   """
      A SENPAI wrapper intended for multithreaded access.

      Any object which implements methods from SENPAIListener can be registered as a listener through addListener.
      The object will wait in its own thread, 
   """
   def __init__ (self):
      self.senpai = SENPAI()
      self.listeners = []
      self.locks = {
         "listen": Lock()
      }
      self.thread = None

   def addListener (self, listener):
      with self.locks["listen"]:
         self.listeners.append(listener)

   def start (self):
      print("SENPAI client running in multithreaded mode.")
      self.senpai.open()
      self.thread = Thread(target=self.loop).run()

   def loop (self):
      while True:
         try:
            event = self.senpai.readEvent()
         except Exception as e:
            print("Error reading next SENPAI event: {}".format(e))
            print("Shutting down ThreadSENPAI main thread.")
            return
         with self.locks["listen"]:
            for listener in self.listeners:
               # spawn thread to handle things for the listener
               Thread(target=listener.handleEvent,args=(event,)).run()


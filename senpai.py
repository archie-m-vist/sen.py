import sys
import json

import win32pipe, win32file, win32api

from event import handleEvent

class SENPAI:
   def __init__ (self):
      self.pipe = win32file.CreateFile(r"\\.\pipe\SEN_P-AI",
         win32file.GENERIC_READ | win32file.GENERIC_WRITE,
         0, None,
         win32file.OPEN_EXISTING,
         0, None)

   def close (self):
      win32api.CloseHandle(self.pipe)

   def readEvent (self):
      data = win32file.ReadFile(self.pipe, 65536)
      raw = data[1].decode('utf-8')
      return handleEvent(json.loads(raw))

def main ():
   testclient = SENPAI()
   try:
      while True:
         print(testclient.readEvent())
   except SystemExit:
      SENPAI.close()

if __name__ == '__main__':
   main()
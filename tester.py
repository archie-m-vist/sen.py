import sys
import json

import win32pipe, win32file

def main ():
   p = win32pipe.CreateNamedPipe(r"\\.\pipe\SEN_P-AI",
      win32pipe.PIPE_ACCESS_DUPLEX | win32file.FILE_FLAG_OVERLAPPED,
      win32pipe.PIPE_TYPE_MESSAGE | win32pipe.PIPE_READMODE_MESSAGE | win32pipe.PIPE_WAIT,
      1, 65536, 65536,3000,None)
   print("created pipe")
   win32pipe.ConnectNamedPipe(p, None)
   print("connected to pipe")
      
   fname = "sample.log" if len(sys.argv) < 2 else sys.argv[1]
   print("loaded logfile",fname)
   with open(fname) as logfile:
      data = json.load(logfile)
      for obj in data:
         out = memoryview(json.dumps(obj).encode('utf-8'))
         win32file.WriteFile(p,out)
         temp = input("Press Enter for next event.")

if __name__ == '__main__':
   main()
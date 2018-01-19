from listener import SENPAIListener
from senpai import SENPAI, ThreadSENPAI

class TestListener (SENPAIListener):
   def handleEvent (self, event):
      print(event)

class TestGoalListener (SENPAIListener):
   def handlesEvent (self, eventType):
      return eventType in set(["Goal", "Own Goal"])

   def handleGoalEvent (self, event):
      print("GOOOOAL! {} puts it in for {}!".format(event.scorer, event.team))

   def handleOwnGoalEvent (self, event):
      print("What a fuckup. {} is going to be ashamed of {} tonight, folks.".format(event.team, event.player))

def main ():
   main = ThreadSENPAI()
   main.addListener(TestListener())
   main.addListener(TestGoalListener())
   main.start()

if __name__ == '__main__':
   main()
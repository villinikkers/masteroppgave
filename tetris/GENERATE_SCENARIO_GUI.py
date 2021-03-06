import tkinter as tk
from tkinter import messagebox
import subprocess
import colorPalettes as cp
import os
from time import localtime, sleep
#FIXME:

#color scheme:


class App:
  def __init__(self, master):
    frame = tk.Frame(master,bg=cp.background)
    frame.pack()

    # List with scenario parameters: [[<name>, <level>, <duration>, <ramp?>], ...]
    self.scenarios = []

    # Header first column:
    self.column0Label = tk.Label(frame, text="Parameters:", fg=cp.text, bg=cp.background)
    self.column0Label.grid(row=0, column=0, columnspan=2)

    # Name specification:
    self.nameLabel = tk.Label(frame, text= "Name:", bg=cp.background, fg=cp.text)
    self.nameLabel.grid(row=1, column=0, sticky="W")

    self.nameEntry = tk.Entry(frame, bg=cp.background2)
    self.nameEntry.grid(row = 1, column=1)

    # Difficulty level specification:
    self.levelLabel = tk.Label(frame, text="Level:", bg=cp.background, fg=cp.text)
    self.levelLabel.grid(row = 2, column=0, sticky="W")
    self.levelEntry = tk.Entry(frame, bg=cp.background2)
    self.levelEntry.grid(row =2, column = 1)

    # Duration specification
    self.durationLabel = tk.Label(frame, text="Duration (s):", bg=cp.background, fg=cp.text)
    self.durationLabel.grid(row=3, column=0, sticky="W")
    self.durationEntry = tk.Entry(frame, bg=cp.background2)
    self.durationEntry.grid(row=3, column=1)

    # Constant speed? ramp = False --> constant speed
    self.rampVar = tk.IntVar()
    self.ramp = tk.Checkbutton(frame, text="Increasing speed?",
      variable=self.rampVar)
    self.ramp.config(bg=cp.background, fg=cp.text, indicatoron=True,
      activebackground="green", onvalue=1, offvalue=0, selectcolor=cp.background)
    self.ramp.grid(row=4, column=0)

    # Number of steps in the ramp up scenario
    # TODO: make unavailabe until ramp i checked
    self.nStepsLabel = tk.Label(frame, text="Number ramp-up steps:",
      bg=cp.background, fg=cp.text)
    self.nStepsLabel.grid(row=5, column=0)
    self.nStepEntryState = "normal"
    self.nStepVar = tk.StringVar()
    self.nStepEntry = tk.Entry(frame, textvariable=self.nStepVar,
      state=self.nStepEntryState, bg=cp.background2)
    #self.nStepVar.set("4")
    self.nStepEntry.grid(row=5, column=1)

    #self.stepVar = tk.IntVar()
    #self.stepVar.set(4) # default
    #self.nStepsOption = tk.OptionMenu(frame,self.stepVar, 4, 6, 8)
    #self.nStepsOption.config(bg=cp.background2)
    #self.nStepsOption.grid(row=5, column=1, sticky="E")

    # Add scenario button
    self.addScenarioButton = tk.Button(frame, text="Add scenario",
      command=self.addScenario, bg=cp.background2)
    self.addScenarioButton.grid(row=6, column=1, columnspan=2, sticky="E")


    # header for list of created scenarios:
    self.listHeader = tk.Label(frame, text="Scenario's", bg=cp.background,
      fg=cp.text)
    self.listHeader.grid(row=0, column = 3)
    # List created scenarios:
    self.scenarioList = tk.Listbox(frame,bg=cp.background2)
    self.scenarioList.grid(row=1, column = 3, rowspan=3)


    # Add elements to listbox: listbox.insert(END, "a list entry")
    self.spaceLabel = tk.Label(frame, text="", bg=cp.background)
    self.spaceLabel.grid(row=9, column=0, columnspan=3)
    self.quitButton = tk.Button(frame, text="QUIT", fg="red", command=frame.quit,
      width=50)
    self.quitButton.grid(row=10, column=0, columnspan=4)

    self.generateScenariosButton = tk.Button(frame, text="Generate scenario's",
      bg=cp.background2, fg="green", command = self.generateVersions)
    self.generateScenariosButton.grid(row=4, column=3, columnspan=2, sticky="W")

    self.clearButton = tk.Button(frame, text="Clear list",
      bg=cp.background2, command=self.clearList)
    self.clearButton.grid(row=5, column = 3)

  # ************** end __init__ *****************************
  def addScenario(self):
    """ Add scnario name to the list of added scenarios: """
    if self.nStepVar.get()=="":
      self.nStepVar.set('1')

    self.scenarioList.insert(0, self.nameEntry.get())
    self.scenarios.append([self.nameEntry.get(), self.levelEntry.get(),
      self.durationEntry.get(), self.rampVar.get(), self.nStepVar.get()])
    print(self.scenarios[-1])
    # delete content of the scenario name field:
    self.nameEntry.delete(first=0, last=len(self.nameEntry.get()))
    self.levelEntry.delete(first=0, last=len(self.levelEntry.get()))
    self.durationEntry.delete(first=0, last=len(self.durationEntry.get()))
    self.rampVar.set(0)
    self.nStepVar.set("")



  def clearList(self):
    """ Clears the list of generated scenarios """
    self.scenarioList.delete(0, self.scenarioList.size())
    self.scenarios = []
    self.rampVar.set(0)
    self.nStepVar.set("")
    self.nameEntry.delete(first=0, last=len(self.nameEntry.get()))
    self.levelEntry.delete(first=0, last=len(self.levelEntry.get()))
    self.durationEntry.delete(first=0, last=len(self.durationEntry.get()))

  # Compile
  def generateVersions(self):
    """
    Compile the defined scenarios to executables
    The individual python versions of each scenario is generated in the first
    subprocess by calling the script generate_scenario_v2.py and passing the
    scenario parameters defined in the GUI.

    The second subprocess runs the script that compiles the generated tetris-
    versions into executables.
    """
    if(len(self.scenarios)==0):
      print("No scenario's added..")
    else:
      # Generate new python versions for each scenario defined:
      for scenario in self.scenarios:

        subprocess.run(
          f"python generate_scenario_v2.py {scenario[0]} {scenario[1]} "\
            f"{scenario[2]} {scenario[3]} {scenario[4]}")
        # end for loop scenario


      # Generate string with the files to be built:
      self.filenames = [scenario[0] + '.py' for scenario in self.scenarios]
      self.filenamesStr = ""
      for filename in self.filenames:
        self.filenamesStr += filename + " "
      self.filenamesStr = self.filenamesStr[:-1]

      # Generate the setup file required for compilation to executable:
      subprocess.run(
        f"python generate_setup.py {self.filenamesStr}")

      # Build executables:
      subprocess.run("python setup.py build")


      # Clear input:
      self.scenarios = []
      self.scenarioList.delete(first=0, last = self.scenarioList.size())
      self.nameEntry.delete(first=0, last= len(self.nameEntry.get()))
      self.durationEntry.delete(first=0, last=len(self.durationEntry.get()))
      self.rampVar.set(0)
      self.nStepVar.set("")

      # Rename folder to avoid accidental overwriting old scenarios:
      timeNow = localtime()
      newFolderName = f"{timeNow.tm_year}-{timeNow.tm_mon}-{timeNow.tm_mday}_"\
        f"{timeNow.tm_hour}{timeNow.tm_min}_build"

      sleep(1) # Necessary to avoid "Permission denied"-error when renameing
      os.rename('build', newFolderName)


      # message box confirming completion:
      messagebox.showinfo("Compilation complete!", "Compilation complete!")



#************ Run program ********************
root=tk.Tk()
root.title("Generate Tetris-Scenario's")
app = App(root)

root.mainloop()
root.destroy()

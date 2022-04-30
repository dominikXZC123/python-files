class Trkl:
  def __init__(self):
    self.variables = {}
    self.functions = {}
    self.currentfunc = None
    self.window = None
    self.pkg = []
  def log(self,text):
    import tkinter as tk
    from tkinter.simpledialog import askstring
    try:
      self.window.destroy()
    except:
      pass
    self.functions = {}
    self.variables = {}
    ifs = 0
    fullog = ""
    file = text.split("\n")
    for i in enumerate(file):
      i = i[0]
      if ifs == 0:
        if file[i].startswith("log >> "):
          replaced = file[i][7:] +"\n"
          for i in self.variables:
            if "*"+i+"*" in replaced:
              replaced = replaced.replace("*{}*".format(i),self.variables[i])
          fullog = fullog + replaced
        elif file[i].startswith("alert >> "):
          from tkinter import messagebox
          replaced = file[i][9:] +"\n"
          for i in self.variables:
            if "*"+i+"*" in replaced:
              replaced = replaced.replace("*{}*".format(i),self.variables[i])
          messagebox.showinfo("alert",replaced)
        elif file[i].startswith("randint "):
          vars = file[i][8:].split(" ")
          import random
          self.variables.update({vars[0][:-1]:str(random.randint(int(vars[1]),int(vars[2])))})
        elif file[i] == ("log >clear> "):
          fullog = ""
        elif file[i].startswith("var "):
          vars = file[i][4:].split(" ")
          var = vars[0][0:len(vars[0])-1]
          try:
            if not vars[1] == "input" and vars[2] == ">>":
              if ":" in vars[0] and vars[0].endswith(":") and vars[0].count(":") == 1:
                for i in self.variables:
                  if "*"+i+"*" in vars[1]:
                    vars[1] = vars[1].replace("*{}*".format(i),self.variables[i])
                self.variables.update({vars[0][:-1]:vars[1]})
              else:
                fullog = fullog + "Error at line {}:\nvariable never assigned\n".format(i+1)
            else:
              import tkinter as tk
              from tkinter.simpledialog import askstring
              vardis = vars
              vardis.remove(vardis[0])
              vardis.remove("input")
              vardis.remove(">>")
              input = askstring('input', " ".join(vardis))
              self.variables.update({var:input})
          except:
            if not "input" in vars and not ">>" in vars:
              if ":" in vars[0] and vars[0].endswith(":") and vars[0].count(":") == 1:
                for i in self.variables:
                  if "*"+i+"*" in vars[1]:
                    vars[1] = vars[1].replace("*{}*".format(i),self.variables[i])
                self.variables.update({vars[0][:-1]:vars[1]})
              else:
                fullog = fullog + "Error at line {}:\nvariable never assigned\n".format(i+1)
          del vars
        elif file[i].startswith("sub "):
          vars = file[i][4:].split(" ")
          nvar = vars[0][:-1]
          try:
            if not vars[1] == "input" and vars[2] == ">>":
              if ":" in vars[0] and vars[0].endswith(":") and vars[0].count(":") == 1:
                for i in self.variables:
                  if "*"+i+"*" in vars[1]:
                    vars[1] = vars[1].replace("*{}*".format(i),self.variables[i])
                self.variables.update({vars[0][:-1]:vars[1]})
              else:
                fullog = fullog + "Error at line {}:\nvariable never assigned\n".format(i+1)
            else:
              import tkinter as tk
              from tkinter.simpledialog import askstring
              vardis = vars
              vardis.remove(vardis[0])
              vardis.remove("input")
              vardis.remove(">>")
              input = askstring('input', " ".join(vardis))
              vars.append(input)
              self.variables.update({vars[0]:str(input)})
          except:
            if not "input" in vars and not ">>" in vars:
              if ":" in vars[0] and vars[0].endswith(":") and vars[0].count(":") == 1:
                for i in self.variables:
                  if "*"+i+"*" in vars[1]:
                    vars[1] = vars[1].replace("*{}*".format(i),self.variables[i])
                self.variables.update({vars[0][:-1]:vars[1]})
              else:
                fullog = fullog + "Error at line {}:\nvariable never assigned\n".format(i+1)
          matches = ["+","-","*","/","%"]
          if any(x in vars[1] for x in matches):
            variable = eval(vars[1])
            if variable % 1 == 0:
              variable = int(variable)
          else:
            variable = "NULL"
          vars.remove(vars[0])
          self.variables.update({nvar:str(variable)})
        elif file[i].startswith("#"):
          pass
        elif file[i].startswith("check if "):
          vars = file[i][9:].split(" ")
          if vars[1] == "=" or vars[1] == ">" or vars[1] == "<" or vars[1] == ">=" or vars[1] == "<=":
            try:
              if vars[1] == "=":
                if self.variables[vars[0]] == vars[2]:
                  ifs = 0
                else:
                  ifs = 1
              if vars[1] == ">":
                if self.variables[vars[0]] > vars[2]:
                  ifs = 0
                else:
                  ifs = 1
              if vars[1] == "<":
                if self.variables[vars[0]] < vars[2]:
                  ifs = 0
                else:
                  ifs = 1
              if vars[1] == ">=":
                if self.variables[vars[0]] >= vars[2]:
                  ifs = 0
                else:
                  ifs = 1
              if vars[1] == "<=":
                if self.variables[vars[0]] <= vars[2]:
                  ifs = 0
                else:
                  ifs = 1
            except:
              fullog = fullog + "Error at line {}:\nvariable {} is undefined\n".format(i+1, vars[0])
              ifs = 1
        elif file[i].startswith("check not "):
          vars = file[i][10:].split(" ")
          if vars[1] == "=" or vars[1] == ">" or vars[1] == "<" or vars[1] == ">=" or vars[1] == "<=":
            try:
              if vars[1] == "=":
                if not self.variables[vars[0]] == vars[2]:
                  ifs = 0
                else:
                  ifs = 1
              if vars[1] == ">":
                if not self.variables[vars[0]] > vars[2]:
                  ifs = 0
                else:
                  ifs = 1
              if vars[1] == "<":
                if not self.variables[vars[0]] < vars[2]:
                  ifs = 0
                else:
                  ifs = 1
              if vars[1] == ">=":
                if not self.variables[vars[0]] >= vars[2]:
                  ifs = 0
                else:
                  ifs = 1
              if vars[1] == "<=":
                if not self.variables[vars[0]] <= vars[2]:
                  ifs = 0
                else:
                  ifs = 1
            except:
              fullog = fullog + "Error at line {}:\nvariable {} is undefined\n".format(i+1, vars[0])
              ifs = 1
        elif file[i].startswith(":deploy:"):
          self.window = tk.Toplevel()
        elif file[i].startswith(":size: "):
          vars = file[i][7:].split(" ")
          for i in self.variables:
            if "*"+i+"*" in vars[0]:
              vars[0] = vars[0].replace("*{}*".format(i),self.variables[i])
              for i in self.variables:
                if "*"+i+"*" in vars[1]:
                  vars[1] = vars[1].replace("*{}*".format(i),self.variables[i])
          try:
            self.window.geometry("{}x{}".format(vars[0],vars[1]))
          except AttributeError as e:
            print(e)
            fullog = fullog + "Error at line {}:\nwindow not deployed\n".format(i+1)
          except tk.TclError as e:
            print(e)
            fullog = fullog + "Error at line {}:\nargument error; one or more arguments werent correct\n".format(i+1)
          except IndexError as e:
            print(e)
            fullog = fullog + "Error at line {}:\nnot enough arguments given (should be :size: sizex sizey\n".format(i+1)
          except Exception as e:
            print(e)
        elif file[i].startswith(":main: "):
          vars = file[i][7:].split(" ")
          try:
            self.packed.destroy()
          except:
            pass
          if vars[0] == ":text:":
            try:
              color = vars[1]
              vars.remove(color)
              vars.remove(":text:")
              varst = " ".join(vars)
              for c in self.variables:
                if "*"+c+"*" in varst:
                  varst = varst.replace("*{}*".format(c),self.variables[c])
              self.packed = tk.Label(self.window,text=varst,bg=self.window["background"],fg=color,font=("Arial","10"))
              self.packed.place(relx = 0.5,
                   rely = 0.5,
                   anchor = 'center')
            except AttributeError as e:
              print(e)
              fullog = fullog + "Error at line {}:\nwindow not deployed\n".format(i+1)
            except tk.TclError as e:
              print(e)
              fullog = fullog + "Error at line {}:\nargument error; one or more arguments werent correct\n".format(i+1)
            except Exception as e:
              print(e)
        elif file[i].startswith(":color: "):
          vars = file[i][8:].split(" ")
          for i in self.variables:
            if "*"+i+"*" in vars[0]:
              vars[0] = vars[0].replace("*{}*".format(i),self.variables[i])
          try:
            self.window.config(bg=vars[0])
          except tk.TclError:
            try:
              fullog = fullog + "Error at line {}:\n{} isnt a color\n".format(i+1, vars[0])
            except IndexError as e:
              print(e)
              fullog = fullog + "Error at line {}:\nno color assigned".format(i+1)
          except AttributeError:
            fullog = fullog + "Error at line {}:\nwindow not deployed\n".format(i+1)
        elif file[i].startswith("@"):
          if file[i].endswith(":") and file[i].count(":") == 1 and ":" in file[i]:
            if not file[i][1:-1] in self.functions:
              self.functions.update({file[i][1:-1]:[]})
              ifs = 2
              self.currentfunc = file[i][1:-1]
            else:
              fullog = fullog + "Error at line {}:\nfunction already exists\n".format(i+1)
          else:
            fullog = fullog + "Error at line {}:\nfunction never defined\n".format(i+1)
        elif file[i].startswith("call_"):
          if file[i][5:-1] in self.functions.keys():
            classs = file[i][5:-1]
            for k, c in enumerate(self.functions[classs]):
              file.insert(i+k+1, c)
              i += 2
        elif file[i] == "get discord-bot":
          self.pkg.append("discord")
          from discord.ext import commands
        elif file[i].startswith("discord-bot.init "):
          init = file[i][17:]
          client = commands.Bot(command_prefix=init)
        elif file[i].startswith("discord-bot.connect "):
          token = file[i][19:]
          client.run(token)
        elif file[i] == "<endcheck>":
          pass
        elif file[i] == "<endfunc>":
          pass
        elif not file[i] == "":
          fullog = fullog + "Error at line {}:\nunexpected function: {}\n".format(i+1, file[i].split(" ")[0])
      elif file[i] == "<endfunc>" and ifs == 2:
        ifs = 0
      elif ifs == 2:
        self.functions[self.currentfunc].append(file[i])
      elif  file[i] == "<endcheck>" and ifs == 1:
        ifs = 0
    return fullog

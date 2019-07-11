# ============================= FORM ============================= #
#@markdown <h3>📝 Enter which localhost port</h3>
port = 8989 #@param {type:"integer"}

#@markdown <h3>📝 Subdomain (Random if empty) (NOTE: this has to be unique!!!)</h3>
subdomain = "sonarr1337" #@param {type:"string"}
# ================================================================ #


import os, psutil, IPython, uuid, time
import ipywidgets as widgets

from IPython.display import HTML, clear_output
from google.colab import output

SuccessRun = widgets.Button(
    description='✔ Successfully',
    disabled=True,
    button_style='success'
)

UnsuccessfullyRun = widgets.Button(
    description='✘ Unsuccessfully',
    disabled=True,
    button_style='danger'
)

class MakeButton(object):
  def __init__(self, title, callback):
    self._title = title
    self._callback = callback
  def _repr_html_(self):
    callback_id = 'button-' + str(uuid.uuid4())
    output.register_callback(callback_id, self._callback)
    template = """<button class="p-Widget jupyter-widgets jupyter-button widget-button mod-info" id="{callback_id}">{title}</button>
        <script>
          document.querySelector("#{callback_id}").onclick = (e) => {{
            google.colab.kernel.invokeFunction('{callback_id}', [], {{}})
            e.preventDefault();
          }};
        </script>"""
    html = template.format(title=self._title, callback_id=callback_id)
    return html

def RandomGenerator():
  return time.strftime("%S") + str(time.time()).split(".")[-1]

def CheckProcess(process, command):
  for pid in psutil.pids():
    try:
      p = psutil.Process(pid)
      if process in p.name():
        for arg in p.cmdline():
          if command in str(arg):  
            return True
          else:
            pass
      else:
        pass
    except:
      continue

def AutoSSH(name,port):
  get_ipython().system_raw("autossh -l " + name + " -M 0 -fNT -o 'StrictHostKeyChecking=no' -o 'ServerAliveInterval 300' -o 'ServerAliveCountMax 30' -R 80:localhost:" + port + " ssh.localhost.run &")
  get_ipython().system_raw("autossh -M 0 -fNT -o 'StrictHostKeyChecking=no' -o 'ServerAliveInterval 300' -o 'ServerAliveCountMax 30' -R " + name + ":80:localhost:" + port + " serveo.net &")

def Start_ServerMT():
  if CheckProcess("autossh",Random_NumberMT) != True:
      AutoSSH(Random_NumberMT, str(port))

try:
  if subdomain == "":
    Random_NumberMT = RandomGenerator()
  else:
    Random_NumberMT = subdomain
  if os.path.isfile("/usr/bin/autossh") == False:
    !apt update -qq -y
    !apt install autossh -qq -y
    clear_output()

  Start_ServerMT()
  display(SuccessRun)
  display(MakeButton("Recheck", Start_ServerMT))
  display(HTML("<h4 style=\"font-family:Trebuchet MS;color:#446785;\"><a style=\"font-family:Trebuchet MS;color:#356ebf;\" href=\"https://" + Random_NumberMT + ".localhost.run\" target=\"_blank\">Website 1</a><br>" \
               "<a style=\"font-family:Trebuchet MS;color:#356ebf;\" href=\"https://" + Random_NumberMT + ".serveo.net\" target=\"_blank\">Website 2 (FAST)</a></h4>"))
except:
  clear_output()
  display(UnsuccessfullyRun)

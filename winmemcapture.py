from subprocess import check_output
import shutil
import os
share = r"\\192.168.229.75\grrshare"
user = r"\username"
pwd = "password"

from contextlib import contextmanager

# Attach to network share
@contextmanager
def network_share_auth(share, user, pwd, drive_letter='P'):

   cmd_parts = ["NET USE %s: %s" % (drive_letter, share)]
   if user:
      cmd_parts.append(" /USER:%s " % user)
   if pwd:
       cmd_parts.append(pwd)
   os.system(" ".join(cmd_parts))
   try:
      yield
   finally:
      os.system("NET USE %s: /DELETE" % drive_letter)

# Get Ramcapture from share and upload to Windows node      
def get_memtool(bitnumber='64bit'):
   if bitnumber == '64bit':
      with network_share_auth(share, user, pwd):
          shutil.copyfile(r"P:\x64\RamCapture64.exe", r"C:\RamCapture64.exe")
          shutil.copyfile(r"P:\x64\RamCaptureDriver64.sys", r"C:\RamCaptureDriver64.sys")
          shutil.copyfile(r"P:\x64\msvcp110.dll", r"C:\msvcp110.dll")
          shutil.copyfile(r"P:\x64\msvcr110.dll", r"C:\msvcr110.dll")
          shutil.copyfile(r"P:\x64\ramcapturedriver.cat", r"C:\ramcapturedriver.cat")

# Run ramcapture on Windows node            
def run_memdump():
   output = check_output("c:\\RamCapture64.exe c:\\grr_memdump64.bin", shell=True)
   magic_return_str = "memdump output %s" % output

# Upload memory dump from ramcapture to share
def upload_memfile():
   with network_share_auth(share, user, pwd):
      sharename = r"P:\grr_memdump64.bin"
      shutil.copy(r"C:\grr_memdump64.bin", sharename)

get_memtool()
run_memdump()
upload_memfile()

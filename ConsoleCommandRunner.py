import subprocess

""" console command runner """
class ConsoleCommandRunner():

    def command_run(self, command):
        try:
            proc = subprocess.Popen(command,stdout=subprocess.PIPE, stderr=subprocess.PIPE,shell=True)
        except OSError, e:
            return e.strerror,"Error"
        (out,error) = proc.communicate()
        return out.strip(), error


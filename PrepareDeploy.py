#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
import subprocess

import PDLogger

class PrepareDeploy:

    def __init__(self, logger):
        self.logger = logger
        self.old_revision=""
        self.new_revision=""
        self.grup = "optimum"
        self.repo = "deney"
        self.TMP_ROOT_PATH = '/home/wwwtemp'
        self.ENCR_ROOT_PATH = '/home/wwwencr'

    def prepare(self):

        # fetch file list
        command = self.get_gitdiff_command()
        process_out = self.console_command_runner(command)
        report = self.analysis_process_result(process_out)
        self.logger.write_log_screen("fetch files list is done")

        """
        for i in report:
            print i
            print report[i]
            print "****************"
            for a in report[i]:
                print a
        """

        # create directories
        for path in report['tmp_paths']:
            self.create_directories(path)

        for path in report['encr_paths']:
            self.create_directories(path)

        """
        cmd = {'cmd':['git', 'show', 'c55c25e:root/eks/pic_db/upload_db.php'], 'stdout':['/home/wwwtemp/outbu.php']}
        print self.console_command_runner(cmd)
        """

        # extract file
        for file in report['file_list']:
            command = self.get_gitshow_command(file)
            self.console_command_runner(command)
            self.logger.write_log_screen(file + " extracted file")

        self.logger.write_log_screen("All files extracted..............")

        # ioncube_encoder run
        for file in report['file_list']:
            command = self.get_ioncube_command(file)
            self.console_command_runner(command)
            self.logger.write_log_screen(file + " ioncube_encoder run" + str(' '.join(command)) + "\n")

        self.git_client_runner(report['file_list'])


    def console_command_runner(self, command):
        cmd = command
        if type(command) is dict:
            out_file_path = str(command['stdout'][0])
            out_file = open(out_file_path,'w')
            out_file.wri
            cmd = command['cmd']
            process = subprocess.Popen(cmd,stdout=out_file, stderr=subprocess.PIPE)
            out, err = process.communicate()
            errcode = process.returncode

            process.wait()
            out_file.flush()
            out_file.clo
            print "if*****>",errcode
            print "if****************************************>\n",out,"\n<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<"

        else:
            process = subprocess.Popen(cmd,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out, err = process.communicate()
            errcode = process.returncode
            if errcode>0:
                print "else*****>\n",out,"\n<<<<<<<<"

        return out


    """ Push sonrasi degisen dosya listesini sorgulama komutu hazirlar """
    def get_gitdiff_command(self):
        command = ['git', 'diff', '--stat', self.old_revision + '...' + self.new_revision]
        self.logger.write_log_screen("Su komut hazirlandi:"+' '.join(command))
        return command

    """ Dosyayı object db den cikarir, tmp bolgesine koyma komutu hazirlar """
    def get_gitshow_command(self, file):
        command = {'cmd': ['git', 'show', self.new_revision + ':' + file],
                   'stdout':[self.TMP_ROOT_PATH + os.sep + self.grup + os.sep + self.repo + os.sep + file ]}
        return command

    """ Dosyayi tmp bolgesinden okuyup ioncube den gecirerek encrypted alana kopyalar """
    # todo: bazi ozel dosyalar icin expire date koyulacak
    def get_ioncube_command(self, file):
        command = ['ioncube_encoder',  self.TMP_ROOT_PATH + os.sep + self.grup + os.sep + self.repo + os.sep + file,
                   '-o', self.ENCR_ROOT_PATH + os.sep + self.grup + os.sep + self.repo + os.sep + file]
        return command

    def create_directories(self, path):
        if os.path.isdir(path)== False:
            os.makedirs(path)
            # todo:get exception
            self.logger.write_log_screen("Directories are created")
        return True

    def analysis_process_result(self, process_out):
        lines = process_out.split("\n")
        i=0
        file_list = []
        return_dict = {}

        for line in lines:
            i = i+1
            column = line.strip().split("|",2)
            if i < len(lines)-1:
                file_list.append(column[0].strip())

        return_dict["file_list"] = file_list
        full_tmp_path=[]
        full_encr_path=[]
        for file in file_list:
            file_path = file.strip().rsplit("/", 1)

            tmp_path = self.TMP_ROOT_PATH + os.sep + self.grup + os.sep + self.repo + os.sep + file_path[0]
            full_tmp_path.append(tmp_path)

            encr_path = self.ENCR_ROOT_PATH + os.sep + self.grup + os.sep + self.repo + os.sep + file_path[0]
            full_encr_path.append(encr_path)

        return_dict["tmp_paths"]  = full_tmp_path
        return_dict["encr_paths"] = full_encr_path

        return return_dict

    """ gitlab user """
    def git_client_runner(self, filelist):
        #for file in report['file_list']:
        command = ['git', 'add', filelist]
        print command
        #self.console_command_runner(command)



if __name__ == '__main__':
    print
    print
    print "________________________________________________________________________________________"

    (path, old_revision, new_revision, branch) = sys.argv
    logger = PDLogger.PDLogger()
    pd = PrepareDeploy(logger)
    #pd.old_revision = old_revision
    #pd.new_revision = new_revision

    # test icin bu örnek commit hashlerini kullaniyoruz
    #pd.old_revision = "f786183"
    #pd.new_revision = "c55c25e"
    pd.old_revision = "b2b3a64"
    pd.new_revision = "05eeadc"

    pd.prepare()



from __future__ import print_function
from IPython.core.magic import (Magics, 
                                magics_class, 
                                line_magic,
                                cell_magic, 
                                line_cell_magic)
import pexpect
import re

PIGPATH = 'pig -4 log4j.properties -x local '
PIGPROMPT = 'grunt> '
PIGCONT = '>> '

HIVEPATH = 'hive  '
HIVEPROMPT = 'hive> '
HIVECONT = '    > '


@magics_class
class bdMagic(Magics):

    def __init__(self, shell):
        super(bdMagic, self).__init__(shell)
        self.pig = None
        self.hive = None
        self.timeout = 30
        self.hive_supress_msg = False

    @line_magic
    def timeout(self, t):
        self.timeout = t
    
    ##
    ## Apache Pig
    ## 
    @line_magic
    def pig_init(self, line):
        if self.pig is not None:
            self.pig.close()
        self.pig = pexpect.spawn(PIGPATH, timeout=self.timeout)
        self.pig.expect(PIGPROMPT, timeout=self.timeout)
        for x in self.pig.before.decode().split('\r\n'):
            print(x)
        return None
            
    @cell_magic
    def pig(self, line, cell):
        if self.pig is None:
            self.pig_init(line)
        x = cell.split('\n')
        for row in x:
            self.pig.sendline(row)
            self.pig.expect(['\r\n'+PIGCONT, '\r\n'+PIGPROMPT], timeout=self.timeout)
            for text in self.pig.before.decode().split('\r\n'):
                if text not in x:
                    print(text)
        return None        
        
    ##
    ## Apache Hive
    ##
    
    @line_magic
    def hive_init(self, line):
        if self.hive is not None:
            self.hive.close()
        self.hive = pexpect.spawn(HIVEPATH, timeout=self.timeout)
        self.hive.expect(HIVEPROMPT, timeout=self.timeout)
        for x in self.hive.before.decode().split('\r\n'):
            print(x)
        return None
            
    @line_magic
    def hive_supress_msgs(self, line):
        self.hive_supress_msg = not self.hive_supress_msg
        
    @cell_magic
    def hive(self, line, cell):
        if self.hive is None:
            self.hive_init(line)
        x = cell.split('\n')
        for row in x:
            self.hive.sendline(row)
            self.hive.expect(['\r\n'+HIVECONT, '\r\n'+HIVEPROMPT], timeout=self.timeout)
            for text in self.hive.before.decode().split('\r\n'):
                if text not in x:
                    if self.hive_supress_msg is True:
                        if text.strip() == 'OK':
                            pass
                        elif text[:11] == 'Time taken:':
                            pass
                        else:
                            print(text)
                    else:
                        print(text)
                        
        return None        

        
def load_ipython_extension(ip):
    bdmagic = bdMagic(ip)
    ip.register_magics(bdmagic)


## esta linea se requiere para depuracion directa 
## en jupyter (commentar para el paquete)
load_ipython_extension(ip=get_ipython())

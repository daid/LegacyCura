#
# Copyright (c) 2011 Adam Tauno Williams <awilliam@whitemice.org>
#
# License: MIT/X11
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
import socket, random


class LPRError(Exception):
    pass


class LPR(object):

    def __init__(self, server, user=None):
        self.server = server
        self.socket = None
        self.hostname = socket.gethostname()
        if (user is None):
            self.user = 'OpenGroupware'
        else:
            self.user = user

    def connect(self):
        if (self.socket is None):
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.server, 515))

    def send_stream(self, queue, name, stream, job_name=None):
        self.command_receive(queue)
        self.subcommand_receive_controlfile(name, job_name=job_name)
        self.subcommand_receive_datafile(stream)

    def close(self):
        self.socket.close()

    def wait(self):
        d=self.socket.recv(1024)
        if d != "\000":
            raise LPRError('LPD Protocol Exception {0}'.format(ord(d)))

    def read(self):
        data = ''

        while True:
            bytes = self.socket.recv(1024)
            data += bytes

            if not bytes:
                return data

    def command_restart(self, queue_name):
        #  COMMAND: RESTART
        #  +----+-------+----+
        #  | 01 | Queue | LF |
        #  +----+-------+----+
        #  Command code - 1
        #   Operand - Printer queue name
        self.queue_name = queue_name
        payload = '\002{0}\012'.format(queue_name)
        self.socket.send(payload)
        self.wait()

    def command_close(self):
        self.socket.send("\000")
        self.wait()

    def command_receive(self, queue_name):
        # COMMAND: RECEIVE A PRINTER JOB
        #  +----+-------+----+
        #  | 02 | Queue | LF |
        #  +----+-------+----+
        #  Command code - 1
        #Operand - Printer queue name
        payload = '\002{0}\012'.format(queue_name)
        self.df = 'df{0}{1}'.format(str(random.randint(1000, 9999)), self.hostname)
        self.socket.send(payload)
        self.wait()

    def command_send_queue_state_short(self, queue_name):
        #+----+-------+----+------+----+
        #| 03 | Queue | SP | List | LF |
        #+----+-------+----+------+----+
        #Command code - 3
        #Operand 1 - Printer queue name
        #Other operands - User names or job numbers
        payload = '\003{0} \012'.format(queue_name)
        self.socket.send(payload)
        return self.read()

    def command_send_queue_state_long(self, queue_name):
        #+----+-------+----+------+----+
        #| 04 | Queue | SP | List | LF |
        #+----+-------+----+------+----+
        #Command code - 4
        #Operand 1 - Printer queue name
        #Other operands - User names or job numbers
        payload = '\004{0} \012'.format(queue_name)
        self.socket.send(payload)
        return self.read()

    def subcommand_abort(self):
        # SUBCMD: ABORT RECEIVE
        #  +----+----+
        #  | 01 | LF |
        #  +----+----+
        #   Command code - 2
        self.socket.send('\001\012')
        self.wait()

    def subcommand_receive_controlfile(self, filename, job_name=None):
        # SUBCMD: RECEIVE CONTROL FILE
        #  +----+-------+----+------+----+
        #  | 02 | Count | SP | Name | LF |
        #  +----+-------+----+------+----+
        #   Command code - 2
        #   Operand 1 - Number of bytes in control file
        #   Operand 2 - Name of control file
        #
        # Build a control string
        #
        # H hostname
        # C class for banner
        # J Job name
        # N source file
        # P user
        if (job_name is None):
            job_name = filename
        control='H{0}\012N{1}\012J{2}\012P{3}\012l{4}\012U{4}\012'.format(self.hostname,
                                                                          filename,
                                                                          job_name,
                                                                          self.user,
                                                                          self.df)
        payload = "\002{0} cfA000{1}\012".format(len(control), self.hostname)
        self.socket.send(payload)
        self.wait()
        self.socket.send(control)
        self.socket.send("\000")
        self.wait()

    def subcommand_receive_datafile(self, stream):
        # SUBCMD: RECEIVE DATA FILE
        #    +----+-------+----+------+----+
        #    | 03 | Count | SP | Name | LF |
        #    +----+-------+----+------+----+
        #     Command code - 3
        #     Operand 1 - Number of bytes in data file
        #     Operand 2 - Name of data file
        stream.seek(0, 2)
        length = stream.tell()
        payload = '\003{0} {1}\012'.format(length, self.df)
        self.socket.send(payload)
        self.wait()
        stream.seek(0, 0)
        x = 0
        while 1:
            data = stream.read(1024)
            if not data:
                break
            x += len(data)
            self.socket.send(data)
        self.socket.send('\000')

if __name__=="__main__":
    f = open('Draft.ps', 'rb')
    lpr = LPR('crew.mormail.com', user='adam')
    lpr.connect()
    lpr.send_stream('cisps', 'test job', f, job_name='my awesome job')
    lpr.close()
    f.close()

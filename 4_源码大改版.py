#!/usr/bin/env python

import codecs,os,sys,threading,serial,time
from serial.tools.list_ports import comports

#---------------------判断python2和python3的input
try:
    raw_input
except NameError:
    raw_input = input   # in python3 it's "raw"
    unichr = chr

#---------------对windows的操作-------------------------
if os.name == 'nt':            
    import msvcrt
    import ctypes

    class Out(object):
        """file-like wrapper that uses os.write"""

        def __init__(self, fd):
            self.fd = fd

        def flush(self):
            pass

        def write(self, s):
            os.write(self.fd, s)        #os.write() 方法用于写入字符串到文件描述符 fd 中. 返回实际写入的字符串长度。

    class Console(object): 
        def __init__(self):
            self.output = codecs.getwriter('UTF-8')(Out(sys.stdout.fileno()), 'replace')    #linux中: STDERR_FILENO 标准出错；stdout_fileno 标准输出；stdin_fileno 标准输入
            sys.stderr = codecs.getwriter('UTF-8')(Out(sys.stderr.fileno()), 'replace')     # https://blog.csdn.net/iamaiearner/article/details/9138865
            sys.stdout = self.output

        #-------------------------------------------
        def write(self, text):
            """Write string"""
            self.output.write(text)                 #write和flush是codecs的方法
            self.output.flush()

        #-----------------------获取键盘输入---------------
        def getkey(self):                           
            while True:
                z = msvcrt.getwch()                                                         #捕获键盘输入，https://blog.csdn.net/zyl_wjl_1413/article/details/84864482
                if z == unichr(13):                                                         # ascii 13 = \r 表示回车， ascii 10 = \n 表示换行
                    return unichr(10)                                                       
                elif z in (unichr(0), unichr(0x0e)):    # functions keys, ignore
                    msvcrt.getwch()
                else:
                    return z


class Transform(object):        
    """do-nothing: forward all data unchanged"""
    def rx(self, text):
        """text received from serial port"""
        return text

    def tx(self, text):
        """text to be sent to serial port"""
        return text

    def echo(self, text):
        """text to be sent but displayed on console"""
        return text


class CRLF(Transform):
    """ENTER sends CR+LF"""

    def tx(self, text):
        return text.replace('\n', '\r\n')


class NoTerminal(Transform):
    """remove typical terminal control codes from input"""

    REPLACEMENT_MAP = dict((x, 0x2400 + x) for x in range(32) if unichr(x) not in '\r\n\b\t')
    REPLACEMENT_MAP.update(
        {
            0x7F: 0x2421,  # DEL
            0x9B: 0x2425,  # CSI
        })

    def rx(self, text):
        return text.translate(self.REPLACEMENT_MAP)

    echo = rx


EOL_TRANSFORMATIONS = {      
    'crlf': CRLF,
}

TRANSFORMATIONS = {
    'direct': Transform,    # no transformation
    'default': NoTerminal,
}


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
def ask_for_port():
    """\
    Show a list of ports and ask the user for a choice. To make selection
    easier on systems with long device names, also allow the input of an
    index.
    """
    sys.stderr.write('\n--- Available ports:\n')
    ports = []
    for n, (port, desc, hwid) in enumerate(sorted(comports()), 1):                  #comport() 在模块serial.tools.list_ports中         
        sys.stderr.write('--- {:2}: {:20} {!r}\n'.format(n, port, desc))
        ports.append(port)
    while True:
        port = raw_input('--- Enter port index or full name: ')
        try:
            index = int(port) - 1
            if not 0 <= index < len(ports):
                sys.stderr.write('--- Invalid index!\n')
                continue
        except ValueError:
            pass
        else:
            port = ports[index]
        return port


class Miniterm(object):


    def __init__(self, serial_instance, echo=False, eol='crlf', filters=()):
        self.console = Console()
        self.serial = serial_instance
        self.input_encoding = 'UTF-8'
        self.output_encoding = 'UTF-8'
        self.eol = eol
        self.filters = filters
        self.update_transformations()    
        self.rx_decoder = None

    def _start_reader(self):         
        """Start reader thread"""
        self._reader_alive = True
        self.receiver_thread = threading.Thread(target=self.reader, name='rx')
        self.receiver_thread.daemon = True
        self.receiver_thread.start()


    def start(self, mode=0):
        """start worker threads"""
        self.alive = True
        self._start_reader()
        # enter console->serial loop
        if mode == 0:
            self.transmitter_thread = threading.Thread(target=self.writer, name='tx')
            self.transmitter_thread.daemon = True
            self.transmitter_thread.start()
            # self.console.setup()                    #modify
        elif mode == 1:
            self.transmitter_thread = threading.Thread(target=self.auto_writer_from_file, name='tx')
            self.transmitter_thread.daemon = True
            self.transmitter_thread.start()

    # def stop(self):
    #     """set flag to stop worker threads"""
    #     self.alive = False

    def join(self, transmit_only=False):
        """wait for worker threads to terminate"""
        self.transmitter_thread.join()
        if not transmit_only:
            if hasattr(self.serial, 'cancel_read'):
                self.serial.cancel_read()
            self.receiver_thread.join()

    # def close(self):
    #     self.serial.close()

    def update_transformations(self):
        """take list of transformation classes and instantiate them for rx and tx"""
        transformations = [EOL_TRANSFORMATIONS[self.eol]] + [TRANSFORMATIONS[f]
                                                             for f in self.filters]
        self.tx_transformations = [t() for t in transformations]
        # self.rx_transformations = list(reversed(self.tx_transformations))

    def set_rx_encoding(self, encoding, errors='replace'):
        """set encoding for received data"""
        self.input_encoding = encoding
        self.rx_decoder = codecs.getincrementaldecoder(encoding)(errors)

    def set_tx_encoding(self, encoding, errors='replace'):
        """set encoding for transmitted data"""
        self.output_encoding = encoding
        self.tx_encoder = codecs.getincrementalencoder(encoding)(errors)


    def reader(self):        
        while self.alive and self._reader_alive:                        
            data = self.serial.read(self.serial.in_waiting or 1).decode("utf-8")        
            if data:
                self.console.write(data)


    def writer(self):
        while self.alive:
            text = self.console.getkey()
            for transformation in self.tx_transformations:              #当exit退出设备后，敲回车能进入设备
                text = transformation.tx(text)
            self.serial.write(self.tx_encoder.encode(text))

    #------------------------modify------------------------------------------------------
    def auto_writer_from_file(self):

        self.serial.write(self.tx_encoder.encode('\n'))
        self.serial.write(self.tx_encoder.encode('\n'))
        self.serial.write(self.tx_encoder.encode('enable\n'))
        self.serial.write(self.tx_encoder.encode('config t\n'))
        for text in open(r'\\iv1\Intech\IT运维体系(ITSD)\2.基础架构组(AE.Infra)\Nero\Backup\1-网络\4-项目实施\8_NewWorld\NewWorld设备配置模板-Cisco'):
            self.serial.write(self.tx_encoder.encode(text))
            time.sleep(1)
        self.serial.write(self.tx_encoder.encode('do wr\n'))
        self.serial.write(self.tx_encoder.encode('wr\n'))
        confirm = input('配置下发完成，请回车进入手动模式')

        while self.alive:
            text = self.console.getkey()
            for transformation in self.tx_transformations:              #当exit退出设备后，敲回车能进入设备
                text = transformation.tx(text)
            self.serial.write(self.tx_encoder.encode(text))


#-------------------------------------------------------------------------------
def main(default_port=None, default_baudrate=9600, default_rts=None, default_dtr=None):

    #--------------例出com口列表，并让用户选择------------
    while True:
        default_port = ask_for_port()
        if default_port is not None:
            break

    #-------------初始化Serial_instance实例，并打开com口连接-----------
    serial_instance = serial.serial_for_url(
        default_port,
        default_baudrate,
        parity='N',
        rtscts=False,
        xonxoff=False,
        do_not_open=True)
    serial_instance.open()

    #-------------------------初始化Miniter 参数
    miniterm = Miniterm(
        serial_instance,
        echo=False,
        eol='CRLF'.lower(),
        filters=['default'])
    miniterm.set_rx_encoding('UTF-8')
    miniterm.set_tx_encoding('UTF-8')

    #---------------------调用Miniter start() 方法开始运行
    mode = int(input('--- Run Mode Code[0 Manual|1 Automatic]: ' ))
    miniterm.start(mode)
    miniterm.join()
    miniterm.close()

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
if __name__ == '__main__':
    main()
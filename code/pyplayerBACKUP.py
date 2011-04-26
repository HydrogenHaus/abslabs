#!/usr/bin/env python


import wave
import threading
import alsaaudio
import numpy
import struct

class track(threading.Thread):

    def __init__(self, file, loops=0):

        self.device = alsaaudio.PCM(card='default')
        self.file = wave.open(file, 'rb')
        self.chan = self.file.getnchannels()
        self.rate = self.file.getframerate()
        self.samp = self.file.getsampwidth()
        self.frms = self.file.getnframes()
        self.code = '<'

        self.device.setchannels(self.chan)
        self.device.setrate(self.rate)

        if self.samp == 1:
            self.device.setformat(alsaaudio.PCM_FORMAT_S8)
            self.code += 'B'
        elif self.samp == 2:
            self.device.setformat(alsaaudio.PCM_FORMAT_S16_LE)
            self.code += 'h'
        elif self.file.samp == 4:
            self.device.setformat(alsaaudio.PCM_FORMAT_S32_LE)
            self.code += 'i'
        else:
            raise ValueError('Unsupported format')

        self.data = self.file.readframes(self.frms)
        self.file.close()

        self.quit = False
        self.paus = False
        self.done = False
        self.step = 2048
        self.pos = 0
        threading.Thread.__init__(self)

    def __enter__(self):
        return self

    def __exit__(self):
        self.stop()

    def run(self):

        while not self.quit:

            if self.pos <= len(self.data):
                self.done = False

                data = self.data[self.pos:self.pos+self.step]
                if len(data) <> self.step:
                    data = data + " "*(self.step - len(data))
                    
                self.ch1 = []
                self.ch2 = []
                for i in range(len(data)/(self.samp*self.chan) - 2*self.samp*self.chan):
                    frame = data[i * self.samp * self.chan : (i+1) * self.samp * self.chan]
                    if self.chan == 1:
                        self.ch1.append(struct.unpack(self.code,frame))
                    if self.chan == 2:
                        self.ch1.append(*struct.unpack(self.code,frame[0:self.samp]))
                        self.ch2.append(*struct.unpack(self.code,frame[self.samp:2*self.samp]))
                
                self.fft = numpy.fft.rfft(numpy.array(self.ch1))
                temp_power = (self.fft*self.fft.conjugate())[0:45]
                self.power = list( numpy.real(temp_power/numpy.max(temp_power)) )

                if not self.paus:
                    self.device.write(data)
                    self.pos += self.step

            else:

                    self.done = True


    def stop(self):
        self.paus = True
        self.quit = True
        while self.isAlive():
            pass

    def skip(self, pos):
        pos = int(len(self.data)*(float(pos)/100))
        self.pos = pos + pos%self.step

    def pause(self):
        self.paus = True

    def unpause(self):
        self.paus = False



if __name__ == "__main__":
    import sys
    t = track(sys.argv[1])
    t.start()
    q = False
    while not q:
        cmd = raw_input("Type q to quit, s to skip, and p to pause: ")
        if cmd == 'q':
            t.stop()
            q = True
        elif cmd == 's':
            pos = float(raw_input("Enter the skip position (percent of song): "))
            t.skip(pos)
        elif cmd == 'p':
            if t.paus:
                t.unpause()
            else:
                t.pause()
        elif cmd == '':
            print 100*float(t.pos)/len(t.data)
        else:
            print "Command not understood!"

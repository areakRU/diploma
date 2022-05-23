import socket
import sys
from struct import *
import matplotlib.pyplot as plt
import numpy as np
from scipy import signal
import pygame as pg
from Classes.Circle import Circle

class EmgDriver:
    def __init__(self):
        self.interface_indicator = False

        self.EMG8x_ADDRESS                           = '192.168.1.207' ;
        self.CHANNELS_TO_MONITOR                     =  (1,)


        self.AD1299_NUM_CH                           = 8
        self.TRANSPORT_BLOCK_HEADER_SIZE             = 16
        self.PKT_COUNT_OFFSET                        = 2
        self.SAMPLES_PER_TRANSPORT_BLOCK             = 128
        self.TRANSPORT_QUE_SIZE                      = 4
        self.TCP_SERVER_PORT                         = 3000
        self.SPS                                     = 500
        self.SAMPLES_TO_COLLECT                      = self.SAMPLES_PER_TRANSPORT_BLOCK*8*5

        self.TCP_PACKET_SIZE                         = int(((self.TRANSPORT_BLOCK_HEADER_SIZE)/4+(self.AD1299_NUM_CH+1)*(self.SAMPLES_PER_TRANSPORT_BLOCK))*4)


        # Create a TCP/IP socket
        self.sock                                    = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Connect the socket to the port where the server is listening
        self.server_address                          = (self.EMG8x_ADDRESS, self.TCP_SERVER_PORT)
        self.sock.connect(self.server_address)
        self.receivedBuffer                          = bytes()
        self.rawSamples                              = np.zeros((self.SAMPLES_TO_COLLECT,len(self.CHANNELS_TO_MONITOR)))
        # Collected samples
        self.numSamples                              = 0


    def get_data(self, indicator: Circle) -> np.ndarray:
        try:
            while True:
                if len(self.receivedBuffer)>=self.TCP_PACKET_SIZE*2:
                    if not self.interface_indicator:
                        indicator.redraw_circle(0x9bcf53)
                        pg.display.update()
                        self.interface_indicator = True
                    # find sync bytes
                    self.startOfBlock = self.receivedBuffer.find('EMG8x'.encode())

                    if self.startOfBlock>=0:

                        # SAMPLES_PER_TRANSPORT_BLOCK*(AD1299_NUM_CH+1)+TRANSPORT_BLOCK_HEADER_SIZE/4
                        self.strFormat = '{:d}i'.format(round(self.SAMPLES_PER_TRANSPORT_BLOCK*(self.AD1299_NUM_CH+1)+self.TRANSPORT_BLOCK_HEADER_SIZE/4))
                        #'1156i'
                        self.samples = unpack(self.strFormat, self.receivedBuffer[self.startOfBlock:self.startOfBlock+self.TCP_PACKET_SIZE] )

                        # remove block from received buffer
                        self.receivedBuffer = self.receivedBuffer[self.startOfBlock+self.TCP_PACKET_SIZE:]

                        self.chCount = 0
                        for chIdx in self.CHANNELS_TO_MONITOR:

                            # get channel offset
                            self.offset_toch = int(self.TRANSPORT_BLOCK_HEADER_SIZE/4 + self.SAMPLES_PER_TRANSPORT_BLOCK*chIdx)

                            #print( samples[offset_to4ch:offset_to4ch+SAMPLES_PER_TRANSPORT_BLOCK] )
                            self.dataSamples = self.samples[self.offset_toch:self.offset_toch+self.SAMPLES_PER_TRANSPORT_BLOCK]

                            self.blockSamples = np.array(self.dataSamples)
                            # print( 'Ch#{0} Block #{1} mean:{2:10.1f},  var:{3:8.1f}, sec:{4:4.0f}'.format(chIdx, samples[PKT_COUNT_OFFSET],np.mean(blockSamples),np.var(blockSamples)/1e6, numSamples/SPS ) )

                            self.rawSamples[self.numSamples:self.numSamples+self.SAMPLES_PER_TRANSPORT_BLOCK,self.chCount] = self.blockSamples

                            self.chCount += 1

                        self.numSamples += self.SAMPLES_PER_TRANSPORT_BLOCK
                        if self.numSamples >= self.SAMPLES_TO_COLLECT:
                            break

                else:
                    self.receivedData = self.sock.recv( self.TCP_PACKET_SIZE )
                    if not self.receivedData:
                        # probably connection closed
                        break
                    self.receivedBuffer += self.receivedData ;

        finally:
            self.sock.close()
            indicator.redraw_circle(indicator.previous_color)
            self.interface_indicator = False
            pg.display.update()

        return self.rawSamples
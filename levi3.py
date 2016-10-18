#!/usr/bin/python
# -*- coding: utf-8 -*-
import cherrypy
import time
import minimalmodbus
import serial

WEB_ROOT = '/root/'

cherrypy.config.update({'server.socket_host': '0.0.0.0'})
instrumentA = minimalmodbus.Instrument('/dev/vport0p2', 1)
instrumentB = minimalmodbus.Instrument('/dev/vport0p2', 2)
instrumentA.serial.baudrate = 19200
instrumentA.serial.timeout = 1.0
instrumentB.serial.baudrate = 19200
instrumentB.serial.timeout = 1.0


# instrumentA  Schneider Electric IEM3150
# instrumentB  Phoenix Contact MA250

class StaticAndDynamic(object):

    @cherrypy.expose
    def SCH(self, **params):
        aram = instrumentA.read_float(2999, 3, 2)
        aram = str(aram)
        time.sleep(0.1)
        fesz = instrumentA.read_float(3027, 3, 2)
        fesz = str(fesz)
        time.sleep(0.1)
        telj = instrumentA.read_float(3053, 3, 2)
        telj = str(telj)
        time.sleep(0.1)
        freq = instrumentA.read_float(3109, 3, 2)
        freq = str(freq)
        time.sleep(0.1)
        hatfogy = instrumentA.read_float(45099, 3, 2)
        hatfogy = str(hatfogy)
        return (
            'I=',
            aram,
            ' Amper   ',
            ' U=',
            fesz,
            ' Volt   ',
            ' P=',
            telj,
            ' KW   ',
            ' f=',
            freq,
            ' Hz    ',
            ' KWH=',
            hatfogy,
            )

    @cherrypy.expose
    def PHO(self, **params):
        fesz2 = instrumentB.read_long(50520, 3, False)
        fesz2 = str(fesz2)
        time.sleep(0.1)
        freq2 = instrumentB.read_long(50526, 3, False)
        freq2 = str(freq2)
        time.sleep(0.1)
        aram2 = instrumentB.read_long(50528, 3, False)
        aram2 = str(aram2)
        time.sleep(0.1)
        pillP = instrumentB.read_long(50536, 3, False)
        pillP = str(pillP)
        time.sleep(0.1)
        pillQ = instrumentB.read_long(50538, 3, False)
        pillQ = str(pillQ)
        time.sleep(0.1)
        pillS = instrumentB.read_long(50540, 3, False)
        pillS = str(pillS)
        time.sleep(0.1)
        Phat = instrumentB.read_long(50780, 3, False)
        Phat = str(Phat)
        time.sleep(0.1)
        Pmed = instrumentB.read_long(50782, 3, False)
        Pmed = str(Pmed)
        return (
            'I=',
            aram2,
            ' mA   ',
            ' U=',
            fesz2,
            ' Volt   ',
            ' P=',
            pillP,
            ' KW   ',
            ' f=',
            freq2,
            ' Hz    ',
            ' P pill=',
            pillP,
            ' W  ',
            ' Q pill=',
            pillQ,
            ' W  ',
            ' S pill=',
            pillS,
            ' W  ',
            'P hatasos=',
            Phat,
            ' W  ',
            'P meddo=',
            Pmed,
            ' W   ',
            )


conf = {'/': {'tools.staticdir.on': True,
        'tools.staticdir.dir': WEB_ROOT,
        'tools.staticdir.index': 'index.html'}}

cherrypy.quickstart(StaticAndDynamic(), config=conf)

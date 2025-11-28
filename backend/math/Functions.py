import numpy as np
import sympy as sp

def Rz(var):
    var = sp.rad(var)
    return sp.Matrix([[sp.cos(var), -sp.sin(var), 0, 0],
                    [sp.sin(var), sp.cos(var), 0, 0],
                    [0, 0, 1, 0],
                    [0, 0, 0, 1]])

def Ry(var):
    var = sp.rad(var)
    return sp.Matrix([[sp.cos(var), 0, sp.sin(var), 0],
                    [0, 1, 0, 0],
                    [-sp.sin(var), 0, sp.cos(var), 0],
                    [0, 0, 0, 1]])

def Rx(var):
    var = sp.rad(var)
    return sp.Matrix([[1, 0, 0, 0],
                    [0, sp.cos(var), -sp.sin(var), 0],
                    [0, sp.sin(var), sp.cos(var), 0],
                    [0, 0, 0, 1]])

def Dz(var):
    return sp.Matrix([[1, 0, 0, 0],
                    [0, 1, 0, 0],
                    [0, 0, 1, var],
                    [0, 0, 0, 1]])

def Dy(var):
    return sp.Matrix([[1, 0, 0, 0],
                    [0, 1, 0, var],
                    [0, 0, 1, 0],
                    [0, 0, 0, 1]])

def Dx(var):
    return sp.Matrix([[1, 0, 0, var],
                    [0, 1, 0, 0],
                    [0, 0, 1, 0],
                    [0, 0, 0, 1]])

def RxDx(alfa, a) -> sp.Matrix:
    return Rx(alfa) * Dx(a)

def RzDz(tita, d) -> sp.Matrix:
    return Rz(tita) * Dz(d)

def T(alfa, a, tita, d) -> sp.Matrix:
    return Rx(alfa) * Dx(a) * Rz(tita) * Dz(d)
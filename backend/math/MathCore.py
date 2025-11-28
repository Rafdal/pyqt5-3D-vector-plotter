import numpy as np
import sympy as sp

from backend.math.Functions import Rz, Ry, Rx, Dz, Dy, Dx, RxDx, RzDz, T

import typing as ty

class Line3D:
    P0: np.ndarray
    P1: np.ndarray
    P2: np.ndarray
    def __init__(self, P0: np.ndarray = None, P1: np.ndarray = None, P2: np.ndarray = None):
        self.P0 = P0
        self.P1 = P1
        self.P2 = P2

class DHParams:
    def __init__(self, alfa: float, a: float, tita: float, d: float):
        self.alfa = alfa
        self.a = a
        self.tita = tita
        self.d = d

    def T(self) -> sp.Matrix:
        return T(self.alfa, self.a, self.tita, self.d)
    
    def RxDx(self) -> sp.Matrix:
        return RxDx(self.alfa, self.a)
    
    def RzDz(self) -> sp.Matrix:
        return RzDz(self.tita, self.d)
    
    def Tf(self) -> np.ndarray:
        T_sym = self.T()
        T_num = T_sym.evalf()
        T_np = np.array(T_num).astype(np.float64)
        return T_np

class JointChain:
    def __init__(self):
        self.end_effector = sp.Identity(4)
        self.origin = sp.Identity(4)
        self.joints = []
        self.lines = []

    def clear(self):
        self.joints = []
        self.lines = []

    def append(self, joint: DHParams):
        self.joints.append(joint)

    def compute(self):
        current = self.origin
        for joint in self.joints:
            line = Line3D()
            line.P0 = current.evalf()
            current = current * joint.RxDx()
            line.P1 = current.evalf()
            current = current * joint.RzDz()
            line.P2 = current.evalf()
            self.lines.append(line)
        self.end_effector = current

    def length(self) -> int:
        return len(self.joints)
    
    def latex(self, expr):
        return sp.latex(expr)
    
    def evalf(self, expr, subs_dict={}):
        return self.end_effector.evalf(subs=subs_dict)

import coptpy as cp
from coptpy import COPT
from coptpy import QuadExpr
from structure import Parking

class AreaOptimizer:
    def __init__(self) -> None:
        self.env = cp.Envr()
        self.model = self.env.createModel(name='Area')
    
    def optimize(self,division_num:int,parking_area:Parking.ParkingArea())-> None:
        
        min_x=parking_area.get_minX()
        max_x=parking_area.get_maxX()
        min_y=parking_area.get_minY()
        max_y=parking_area.get_maxY()
        # add variables
        # x = self.model.addVars(division_num, 1,lb=min_x, ub=max_x,vtype=COPT.INTEGER)
        # y = self.model.addVars(division_num, 1,lb=min_y, ub=max_y,vtype=COPT.INTEGER)
        # w = self.model.addVars(division_num, 1,lb=10, ub=max_x,vtype=COPT.INTEGER)
        # d = self.model.addVars(division_num, 1,lb=10, ub=max_x,vtype=COPT.INTEGER)

        # print(x.select())
        
        # # add constraints
        # self.model.addConstrs(x[i] + y[i] >= 2.0 for i in range(10))
        
        
        x1=self.model.addVar(lb=min_x,ub=max_x,vtype=COPT.INTEGER)
        y1=self.model.addVar(lb=min_y,ub=max_y,vtype=COPT.INTEGER)
        x2=self.model.addVar(lb=min_x,ub=max_x,vtype=COPT.INTEGER)
        y2=self.model.addVar(lb=min_y,ub=max_y,vtype=COPT.INTEGER)
        w1=self.model.addVar(lb=5,ub=10)
        d1=self.model.addVar(lb=0,ub=10,vtype=COPT.INTEGER)
        w2=self.model.addVar(lb=0,ub=10,vtype=COPT.INTEGER)
        d2=self.model.addVar(lb=0,ub=10,vtype=COPT.INTEGER)
        # add constraints
        
        # self.model.addQConstr(w1*w1 <= 5, name="q1")
        
        
        # add objective
        # quadexpr2 = QuadExpr(w1*w1-2*w1)
        self.model.setObjective(w1*w1, sense=COPT.MINIMIZE)
        
        # Set parameter
        self.model.setParam(COPT.Param.TimeLimit, 10.0)

        # Solve the model
        self.model.solve()
        # Analyze solution
        if self.model.status == COPT.OPTIMAL:
            print("Objective value: {}".format(self.model.objval))
            allvars = self.model.getVars()

        print("Variable solution:")
        for var in allvars:
            print(" x[{0}]: {1}".format(var.index, var.x))

        print("Variable basis status:")
        for var in allvars:
            print(" x[{0}]: {1}".format(var.index, var.basis))
        
    
    

    
    
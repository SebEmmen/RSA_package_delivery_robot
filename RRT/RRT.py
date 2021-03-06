#RRT
import pygame
from RRTbasePY import RRTGraph
from RRTbasePY import RRTMap
import time

def main():
    dimensions = (1000, 1000)
    start = (50, 50)
    goal = (900,850)
    obsdim = 30
    obsnum = 30
    iteration = 0
    t1=0


    pygame.init()
    map = RRTMap(start, goal, dimensions, obsdim, obsnum)
    graph = RRTGraph(start, goal,dimensions, obsdim, obsnum)

    obstacles = graph.makeobs()

    map.drawMap(obstacles)
    t1=time.time()
    while (not graph.path_to_goal()):
        elapsed=time.time()-t1
        t1=time.time()
        if elapsed > 10:
            raise
            
        if iteration % 10 == 0:
            X, Y, Parent = graph.bias(goal)
            pygame.draw.circle(map.map, map.grey, (X[-1], Y[-1]), map.nodeRad+2, 0)
            pygame.draw.line(map.map, map.Blue, (X[-1], Y[-1]), (X[Parent[-1]], Y[Parent[-1]]), map.edgeThickness)
        else:
            X, Y, Parent = graph.expand()
            pygame.draw.circle(map.map, map.grey, (X[-1], Y[-1]), map.nodeRad+2, 0)
            pygame.draw.line(map.map, map.Blue, (X[-1], Y[-1]), (X[Parent[-1]], Y[Parent[-1]]), map.edgeThickness)
        if iteration % 5 ==0:
            pygame.display.update()
        iteration += 1
    map.drawPath(graph.getPathCoords())
    pygame.display.update()
    pygame.event.clear()
    pygame.event.wait(0)


if __name__ == '__main__':
    result = False
    try:
        main()
        result=True
    except:
        result=False
import os
import sys

sys.path.append(str(os.path.abspath(os.getcwd())))

from planner.sampling_based_torus.prm_component import PRMTorusRedundantComponent


class PRMTorusRedundantBase(PRMTorusRedundantComponent):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def build_graph(self, numNodes):  # build from stratch (batch PRM)
        # XRand = [self.uni_sampling() for _ in range(numNodes)]
        XRand = self.grid_sampling()
        for xRand in XRand:
            XNear, distXNear = self.near_wrap(XRand, xRand, None)
            for xNear in XNear:
                if not self.is_collision(xRand, xNear):
                    cost = self.cost_line(xRand, xNear)
                    if not xNear in xRand.edgeNodes:
                        xRand.edgeNodes.append(xNear)
                        xRand.edgeCosts.append(cost)
                    if not xRand in xNear.edgeNodes:
                        xNear.edgeNodes.append(xRand)
                        xNear.edgeCosts.append(cost)
                    if not xRand in self.nodes:
                        self.nodes.append(xRand)
                    if not xNear in self.nodes:
                        self.nodes.append(xNear)

        print("Building Roadmap Done.")
        print(f"Current NumNodes = [{len(self.nodes)}]")
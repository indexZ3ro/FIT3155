class tableau:
    def __init__(self, objective, constraint_lhs, constraint_rhs):
        self.matrix = []
        self.basic = [0] * len(constraint_rhs)
        self.CJ_ZJ = 2 * len(objective) * [None]
        self.Cj = objective + len(objective) * [0]
        self.rhs = constraint_rhs
        self.theta = len(constraint_rhs) * [None]
        self.z = None

        self.makeMatrix(constraint_lhs)

    def makeMatrix(self, constraint_lhs):
        self.matrix = constraint_lhs
        for i in range(len(self.matrix)):
            # double length with 0s and set 1 columns
            base_len = len(self.matrix[i])
            self.matrix[i] = self.matrix[i] + base_len * [0]
            self.matrix[i][i + base_len] = 1

    def compute(self):
        while (True):
            # compute cj-zi
            # i represents a row and j represents a column
            max_index = None
            for j in range(len(self.matrix[0])):
                zj = 0
                for i in range(len(self.matrix)):
                    zj += self.basic[i] * self.matrix[i][j]
                self.CJ_ZJ[j] = self.Cj[j] - zj
                if self.CJ_ZJ[j] > 0 and (max_index is None or self.CJ_ZJ[j] > self.CJ_ZJ[max_index]):
                    max_index = j

            # compute new z
            new_z = 0
            for i in range(len(self.rhs)):
                new_z += self.rhs[i] * self.basic[i]
            self.z = new_z

            # break
            if max_index is None:
                print('---')
                print(self.z)
                break

            # compute theta
            min_theta_index = None
            for i in range(len(self.theta)):
                self.theta[i] = self.rhs[i] / self.matrix[i][max_index]
                if self.theta[i] > 0 and (min_theta_index is None or self.theta[i] < self.theta[min_theta_index]):
                    min_theta_index = i

            # new basic
            self.basic[min_theta_index] = self.Cj[max_index]

            # pivot
            divisor = self.matrix[min_theta_index][max_index]
            new_matrix = [[None for _ in range(len(self.matrix[0]))] for _ in range(len(self.matrix))]
            for i in range(len(self.matrix)):
                for j in range(len(self.matrix[i])):
                    if j == max_index:
                        if i == min_theta_index:
                            new_matrix[i][j] = 1
                        else:
                            new_matrix[i][j] = 0
                    else:
                        if i == min_theta_index:
                            new_matrix[i][j] = self.matrix[i][j] / divisor
                        else:
                            new_matrix[i][j] = self.matrix[i][j] - self.matrix[i][max_index] * \
                                               self.matrix[min_theta_index][j] / divisor

            # do the same for the rhs
            new_rhs = [None] * len(self.rhs)
            for i in range(len(self.rhs)):
                if i == min_theta_index:
                    new_rhs[i] = self.rhs[i] / divisor
                else:
                    new_rhs[i] = self.rhs[i] - self.matrix[i][max_index] * self.rhs[min_theta_index] / divisor

            # set new values
            self.matrix = new_matrix
            self.rhs = new_rhs
            # print(self.matrix)
            # print(self.rhs)

table = tableau([6, 5], [[1, 1], [3, 2]], [5, 12])
table.compute()

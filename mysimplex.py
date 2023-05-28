import sys


class tableau:
    def __init__(self, objective, constraint_lhs, constraint_rhs):
        self.matrix = []
        self.basic = [0] * len(constraint_rhs)
        self.basic_index = list(range(len(objective), len(constraint_rhs) + len(objective)))
        self.CJ_ZJ = (len(constraint_rhs) + len(objective)) * [None]
        self.Cj = objective + len(constraint_rhs) * [0]
        self.rhs = constraint_rhs
        self.theta = len(constraint_rhs) * [None]
        self.z = None
        self.objective_len = len(objective)

        self.makeMatrix(constraint_lhs)

    def makeMatrix(self, constraint_lhs):
        self.matrix = constraint_lhs
        base_len = len(self.matrix[0])
        for i in range(len(self.matrix)):
            # ass length with 0s and set 1 columns
            constraint_len = len(constraint_lhs)
            self.matrix[i] = self.matrix[i] + constraint_len * [0]
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
                filtered_rhs = [str(self.rhs[i]) if self.basic[i] != 0 else '0' for i in range(len(self.rhs))]
                objective_values = []
                for i in range(self.objective_len):
                    try:
                        objective_values.append(filtered_rhs[self.basic_index.index(i)])
                    except ValueError:
                        objective_values.append('0')
                return self.z, objective_values
                break

            # compute theta
            min_theta_index = None
            for i in range(len(self.theta)):
                try:
                    self.theta[i] = self.rhs[i] / self.matrix[i][max_index]
                except ZeroDivisionError:
                    self.theta[i] = float('inf')
                if self.theta[i] > 0 and (min_theta_index is None or self.theta[i] < self.theta[min_theta_index]):
                    min_theta_index = i

            # new basic
            self.basic[min_theta_index] = self.Cj[max_index]
            self.basic_index[min_theta_index] = max_index

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


def read_input(path):
    with open(path, 'r') as file:
        lines = file.readlines()

    objective = []
    constraint_lhs = []
    constraint_rhs = []

    i = 0
    stage = None
    num_constraints = 0
    while i < len(lines):
        line = lines[i].strip()
        if line == '# numConstraints':
            stage = 1
        elif line == '#objective':
            stage = 2
        elif line == '# constraintsLHSMatrix':
            stage = 3
        elif line == '# constraintsRHSVector':
            stage = 4
        elif stage == 1:
            num_constraints = int(lines[i])
        elif stage == 2:
            objective = [int(num) for num in lines[i].split(',')]
        elif stage == 3:
            constraint_lhs.append([int(num) for num in lines[i].split(',')])
        elif stage == 4:
            constraint_rhs.append(int(lines[i]))
        i += 1
    return objective, constraint_lhs, constraint_rhs


def clear_file(filename):
    with open(filename, 'w') as file:
        pass


def write_to_file(filename, optimalObjective, optimalDecisions):
    with open(filename, 'w') as file:
        file.write('# optimalDecisions\n')
        file.write(', '.join(optimalDecisions) + '\n')
        file.write('# optimalObjective\n')
        file.write(str(optimalObjective) + '\n')


if __name__ == '__main__':
    clear_file('lpsolution.txt')
    if len(sys.argv) != 2:
        print("Usage: python mysimplex.py <text filename>")
        sys.exit(1)

    text_file = sys.argv[1]
    objective, constraint_lhs, constraint_rhs = read_input(text_file)
    table = tableau(objective, constraint_lhs, constraint_rhs)
    optimalObjective, optimalDecisions = table.compute()

    write_to_file("lpsolution.txt", optimalObjective, optimalDecisions)

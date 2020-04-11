import numpy as np


def rotate_matrix_with_angle(matrix, dim, angle):
    times = 0
    if int(angle) == 315:
        times = 1
    elif int(angle) == 45:
        times = 3
    elif int(angle) == 135:
        times = 5
    elif int(angle) == 225:
        times = 7
    else:
        return matrix
    for i in range (0, times):
        matrix = rotate_matrix(matrix, dim)
    print(angle)
    print_matrix(matrix, dim)
    return matrix


def rotate_matrix(matrix, dim):
    rotated_matrix = np.zeros((dim, dim))
    rotated_matrix[0, 0] = matrix[0, 1]
    rotated_matrix[0, 1] = matrix[0, 2]
    rotated_matrix[0, 2] = matrix[1, 2]
    rotated_matrix[1, 0] = matrix[0, 0]
    rotated_matrix[1, 1] = matrix[1, 1]
    rotated_matrix[1, 2] = matrix[2, 2]
    rotated_matrix[2, 0] = matrix[1, 0]
    rotated_matrix[2, 1] = matrix[2, 0]
    rotated_matrix[2, 2] = matrix[2, 1]
    return rotated_matrix


def print_matrix(matrix, dim):
    for i in range(0, dim):
        for j in range(0, dim):
            print("%d " % (int(matrix[i][j])), end='')
        print("")
    print("")

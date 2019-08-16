import sys
import os

#MARK: -variables
vertices = []
awns = []
visited = []
reverted = []
scc = []
component = []

#MARK: -prepare the archive erasing all the blank spaces to avoid errors
def erasingBlankLines(eraseFile, filePath):
    #pass the entire file to a list
    #adds not blank spaces lines to a list
    #rewrite the file with the new list
    lines = eraseFile.readlines()
    eraseFile.close()
    validLines = []
    for line in lines:
        if not line.isspace():
            validLines.append(line)
    eraseFile = open(filePath, "w")
    eraseFile.write("".join(validLines))
    eraseFile.close()

#MARK: -fills the vertices and edges list
def verticesAndEdges(edge1 ,edge2, counter):
    awns.append(edge1)
    awns[counter] += ":"
    awns[counter] += edge2
    if edge1 not in vertices:
        vertices.append(edge1)
    if edge2 not in vertices:
        vertices.append(edge2)

#MARK: -file principal call
def handlingArchive():
    lineCounter = 0
    #path = (raw_input("arrastre el archivo a leer: "))
    path = "/Users/sofiarodriguezmorales/Desktop/projet-atom/grafo1.txt"
    #print(path)
    if not os.path.isfile(path):
        sys.exit("Archivo no encontrado")
    file = open(path,"r")
    erasingBlankLines(file, path)
    file = open(path)
    for line in file:
        #deleting /n at the end of each line
        line = line[:-1]
        if line == "grafo":
            sys.exit("This algorithm is only valid in digraphs")

        if (len(line.split(",")) == 2 or len(line.split(",")) == 3):
            #ine = line[:-1]
            verticesAndEdges(line.split(",")[0], line.split(",")[1], lineCounter)
            lineCounter += 1


#MARK: -creates matrix (0 = normal, 1 = transposed)
def createMatrix(vertices, transposed):
    newMatrix = [["."] * (len(vertices) + 1) for row in range(len(vertices) + 1)]
    for column in range(len(vertices) + 1):
        row = 0
        for row in range(len(vertices) + 1):
            if column == 0:
                if row == 0:
                    newMatrix[column][row] = "-"
                else:
                    newMatrix[column][row] = vertices[row - 1]
            else:
                if row == 0:
                    newMatrix[column][row] = vertices[column - 1]
                else:
                    newMatrix[column][row] = "."
    #Adding awns
    for i in range(len(vertices) + 1):
        k = 0
        for j in range(len(vertices) + 1):
            for k in range(len(awns)):
                # si tipo grafo = 0 se pone arista en ambas si = 1 solo de la que sale a la que es dirigida
                if (newMatrix[i][0] == awns[k].split(":")[0]) and (newMatrix[0][j] == awns[k].split(":")[1]):
                    if transposed == 0:
                        newMatrix[i][j] = "*"
                    else:
                        newMatrix[j][i] = "*"
    return newMatrix

#MARK: -depth search
def depthFirstSearch(yAxis, matrix):
    if not matrix[yAxis][0] in visited:
        visited.append(matrix[yAxis][0])
    scc.append(matrix[yAxis][0])
    for xAxis in range(1,len(vertices) + 1):
        if (matrix[yAxis][xAxis] == "*" and not matrix[xAxis][0] in visited):
            depthFirstSearch(xAxis,matrix)
    reverted.append(matrix[yAxis][0])
    component.append(matrix[yAxis][0])
    return

#MARK: -principal call
    #read the file
    #we add the first element of vertices array at he end bc when creating the matrix
    #screate the principal matrix
    #first deep search to register trail
    #reverting the list to make a matrix with the same order thats going to be trail and creating transposed matrix
    #second deep first search printing strogly connectedcomponents
    #preparing lists for the new search

handlingArchive()
graphMatrix = createMatrix(vertices,0)
for row in graphMatrix:
    print row
for vertex in range(1, len(vertices)):
    if vertices[vertex] not in visited:
        depthFirstSearch(vertex + 1, graphMatrix)
reverted = reverted[::-1]
graphMatrix = createMatrix(reverted,1)
scc = []
visited = []
print "Las componentes conexas son:"
for vertex in range(len(reverted)):
    if scc.count(reverted[vertex]) == 0:
        component = []
        depthFirstSearch(vertex + 1, graphMatrix)
        print component

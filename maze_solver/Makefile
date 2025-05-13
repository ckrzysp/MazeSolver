########################################
##
## Makefile
## LINUX compilation 
##
##############################################

# FLAGS
C++FLAG = -g -std=c++17

MATH_LIBS = -lm

EXEC_DIR = .

.cc.o:
	g++ $(C++FLAG) $(INCLUDES) -c $< -o $@

# Including
INCLUDES = -I.

# --> All libraries
LIBS_ALL = -L/usr/lib -L/usr/local/lib

# Maze Detector Programs
CC_OBJ_1 = image.o maze_detector.o 
CC_OBJ_2 = image.o maze_detector.o h2.o
CC_OBJ_3 = image.o maze_detector.o h3.o
CC_OBJ_4 = image.o maze_detector.o h4.o

PROGRAM_NAME_1 = maze_detector
PROGRAM_NAME_2 = h2
PROGRAM_NAME_3 = h3
PROGRAM_NAME_4 = h4

$(PROGRAM_NAME_1): $(CC_OBJ_1)
	g++ $(C++FLAG) -o $(EXEC_DIR)/$@ $(CC_OBJ_1) $(INCLUDES) $(LIBS_ALL)

$(PROGRAM_NAME_2): $(CC_OBJ_2)
	g++ $(C++FLAG) -o $(EXEC_DIR)/$@ $(CC_OBJ_2) $(INCLUDES) $(LIBS_ALL)

$(PROGRAM_NAME_3): $(CC_OBJ_3)
	g++ $(C++FLAG) -o $(EXEC_DIR)/$@ $(CC_OBJ_3) $(INCLUDES) $(LIBS_ALL)

$(PROGRAM_NAME_4): $(CC_OBJ_4)
	g++ $(C++FLAG) -o $(EXEC_DIR)/$@ $(CC_OBJ_4) $(INCLUDES) $(LIBS_ALL)

all:
	make $(PROGRAM_NAME_1)
	make $(PROGRAM_NAME_2)
	make $(PROGRAM_NAME_3)
	make $(PROGRAM_NAME_4)

clean:
	(rm -f *.o; rm maze_detector; rm h2; rm h3; rm h4)

CC = g++
CFLAGS = -std=c++11 -g -Wall
INCLUDE =-I minisat -I minisat/minisat/core -I minisat/minisat/mtl -I minisat/minisat/simp -I aiger -I simpleIC3 -I simpleIC3/aiglib -I simpleIC3/util
LDFLAGS = -lz

TOPDIR = $(PWD)
SRCDIR = $(TOPDIR)/simpleIC3
AIGDIR = $(SRCDIR)/aiglib
IC3DIR = $(SRCDIR)/ic3
UTIDIR = $(SRCDIR)/util

SRC = $(wildcard $(IC3DIR)/*.cpp)
OBJ=${patsubst %.cpp, $(IC3DIR)/%.o, ${notdir ${SRC}}}

# main : test

# test:
# 	@echo $(SRC)
# 	@echo $(OBJ)

TARGET = main
BIN_TARGET=${TOPDIR}/${TARGET}

${BIN_TARGET}: ${OBJ} minisat/build/release/minisat/core/Solver.o\
					 minisat/build/release/minisat/simp/SimpSolver.o \
					 minisat/build/release/minisat/utils/Options.o \
					 minisat/build/release/minisat/utils/System.o \
					 aiger/aiger.o
	$(CC) ${CFLAGS} ${OBJ} \
					minisat/build/release/minisat/core/Solver.o \
					minisat/build/release/minisat/simp/SimpSolver.o \
					minisat/build/release/minisat/utils/Options.o \
					minisat/build/release/minisat/utils/System.o \
					aiger/aiger.o \
					${SRCDIR}/main.cpp -o $@ \
					${LDFLAGS} ${INCLUDE}

${IC3DIR}/%.o : ${IC3DIR}/%.cpp 
	$(CC) ${CFLAGS} -c $< -o $@ ${INCLUDE}

clean:
	find ${IC3DIR} -name *.o -exec rm -rf {} \; 
	rm ${TOPDIR}/main



# ic3 :	minisat/build/dynamic/lib/libminisat.so aiger/aiger.o
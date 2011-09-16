#  Copyright (c) 1996 - 2001 Caldera International, Inc.
#                    All Rights Reserved
#
CC=cc
CCOPT=-O
LDOPT=-lm 

CFLAGS= $(CCOPT)

SRCS =  add.c disk1.c div.c fun.c funcal.c mul.c \
	ram.c creat-clo.c disk_src.c int_fcns.c num_fcns.c pipe_test.c \
	fillin.c rand.c rtmsec.c

TASKS = add.o disk1.o div.o fun.o funcal.o mul.o \
	ram.o creat-clo.o disk_src.o int_fcns.o num_fcns.o pipe_test.o

OBJS = fillin.o rand.o rtmsec.o $(TASKS)

# ugly but portable, even on (very) dumb makes..

.c.o:	suite.h
	$(CC) $(CFLAGS) -c $*.c

all:	singleuser rpt9
	echo "#!/bin/sh" > true
	chmod +x true

singleuser: singleuser.o suite.h files.h $(OBJS)
	$(CC) $(CFLAGS) -o singleuser singleuser.o $(OBJS) $(LDOPT)

rpt9: rpt9.o
	$(CC) $(CFLAGS) -o rpt9 rpt9.o $(LDOPT)

add.o : add.c suite.h

creat-clo.o : creat-clo.c suite.h

disk1.o : disk1.c suite.h

disk_src.o : disk_src.c suite.h

div.o : div.c suite.h

fillin.o : fillin.c suite.h

fun.o : fun.c suite.h funcal.h

funcal.o : funcal.c suite.h funcal.h

mul.o : mul.c suite.h

singleuser.o : singleuser.c suite.h files.h

int_fcns.o : int_fcns.c suite.h

num_fcns.o : num_fcns.c suite.h

pipe_test.o : pipe_test.c suite.h

ram.o : ram.c suite.h

rand.o : rand.c suite.h

rtmsec.o : rtmsec.c suite.h testerr.h

clean newrun:
	@echo "Resetting AIM Independent Resource Benchmark - Suite IX for another run."
	@rm -f tmp* core *.o

reset:
	@echo "Resetting AIM Independent Resource Benchmark - Suite IX to new install condition."
	@rm -f s9workfile suite9.ss logfile.suite9 results
	@rm -f input singleuser nohup.out
	@rm -f tmp* core *.o
	@cp Makefile.setup Makefile


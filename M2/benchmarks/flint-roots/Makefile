CXX ?= c++
CXXFLAGS ?= -O2 -std=c++17 -Wall -Wextra
LDLIBS = -lflint -lmps -lgmpxx -lmpfr -lgmp -lpthread
roots: roots.cpp
	$(CXX) $(CPPFLAGS) $(CXXFLAGS) $< -o $@ $(LDFLAGS) $(LDLIBS)
.PHONY: benchmark
benchmark: roots
	python3 benchmark.py --binary ./roots --output results

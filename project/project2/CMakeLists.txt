cmake_minimum_required(VERSION 3.9)
project(project2)

set(CMAKE_CXX_STANDARD 11)

add_executable(project2
        auto_ack_test.py
        duty_cycle_test.py
        example-broadcast.c
        Makefile
        Makefile.target
        project-conf.h
        receiver.c
        sender.c
        symbols.c
        symbols.h
        test.py)

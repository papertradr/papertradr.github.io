#pragma once
#ifndef MLOCK_WRAPPER_H_
#define MLOCK_WRAPPER_H_

#include "exception_wrappers.h"
#include "mmap_wrapper.h"
#include <iostream>
#include <string>

// forward declaration of MmapHandler
template <typename T>
class MmapHandler;


template <typename T>
class Mlock
{
protected:
    Mmap<T> m_mmap;

public:
    T &data();
    int m_lock_status;
    Mlock(int, std::string, bool);
    ~Mlock();
};

#include "mlock_wrapper.inl"

#endif

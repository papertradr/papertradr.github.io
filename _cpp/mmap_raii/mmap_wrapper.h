#pragma once
#ifndef MMAP_WRAPPER_H_
#define MMAP_WRAPPER_H_

#include "exception_wrappers.h"
#include <assert.h>
#include <config.hpp>
#include <fcntl.h>
#include <iostream>
#include <new>
#include <string>
#include <sys/file.h>
#include <sys/mman.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <unistd.h>

// forward declaration of Mlock and MmapHandler
template <typename T>
class Mlock;

template <typename T>
class MmapHandler;

/**
 * @brief
 *
 * @tparam T
 */
template <typename T>
class Mmap
{
protected:
    std::string m_filename; // shared data filename
    bool m_readonly;        // read only flag
    size_t m_mapsize;       // final mapsize (page aligned)
    int m_fid;              // file descriptor
    int m_lock_status;      // mlock prevents page swap
    void *m_ptr;            // mmap return pointer
    T *m_data_ptr;          // data ptr casted as T*
public:
    Mmap(int, std::string, bool);
    ~Mmap();

    T &data();
    void mmapWrapper(int);
    long getFilesize();


    friend class Mlock<T>;
    friend class MmapHandler<T>;
};

#include "mmap_wrapper.inl"

#endif

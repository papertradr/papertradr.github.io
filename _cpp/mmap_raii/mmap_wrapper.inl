/**
 * @brief Construct a new Mmap:: Mmap object
 *
 * @param size
 * @param filename
 * @param readonly
 */
template <typename T>
inline Mmap<T>::Mmap(int size, std::string filename, bool readonly) : m_filename(filename), m_readonly(readonly)
{
    mmapWrapper(size);
    std::cout << "mmap at " << m_ptr << " size: " << m_mapsize << "\n";
};


/**
 * @brief Destroy the Mmap:: Mmap object
 *
 */
template <typename T>
inline Mmap<T>::~Mmap()
{
    if (m_ptr != MAP_FAILED) // we want pid that mapped to unmap
    {
        ::munmap(static_cast<void *>(m_ptr), m_mapsize);
        ::close(m_fid);
        std::cout << "munmap at " << m_ptr << "\n";
    }
};

/**
 * @brief
 *
 * @return size_t
 */
template <typename T>
inline long Mmap<T>::getFilesize()
{
    struct stat st;
    fstat(m_fid, &st);
    return st.st_size;
}


/**
 * @brief
 *
 * @tparam T
 * @return
 */
template <typename T>
inline T &Mmap<T>::data()
{
    return *m_data_ptr;
}

/**
 * @brief
 *
 * @param size
 */
template <typename T>
inline void Mmap<T>::mmapWrapper(int size)
{
    if (size <= 0)
    {
        throw MmapInvalidSizeException();
    }

    int nb_pages = ((size - 1) / getpagesize()) + 1;
    RASSERT(nb_pages > 0);
    m_mapsize = static_cast<size_t>(nb_pages * getpagesize());

    m_fid = ::open(m_filename.c_str(), O_CREAT | O_RDWR, S_IRWXU | S_IRWXG);
    if (m_fid == -1)
    {
        throw MmapFileOpenException();
    }

    m_ptr = ::mmap(nullptr,   // addr: if addr is NULL, then kernel chooses the (page   aligned) address
                              // at which to create the mapping
                   m_mapsize, // length: number of bytes
                   m_readonly ? PROT_READ : PROT_READ | PROT_WRITE, // set whether readonly
                   MAP_SHARED,                                      // flags: share this mapping to other processes
                   m_fid,                                           // file descriptor
                   0                                                // offset
    );
    if (m_ptr == MAP_FAILED)
    {
        throw MmapFailException();
    }

    while (::flock(m_fid, LOCK_EX) != 0)
    {
        ::usleep(1000);
    }

    if (getFilesize() == 0)
    {
        if (m_readonly)
        {
            std::cerr << m_filename << " does not exist!\n";
            throw MmapFailException();
        }
        std::cout << "File size is 0" << std::endl;
        ::ftruncate(m_fid, static_cast<long>(m_mapsize));
        m_data_ptr = new (m_ptr) T;
    }
    else
    {
        std::cout << "File size is " << getFilesize() << std::endl;
        m_data_ptr = reinterpret_cast<T *>(m_ptr);
    }

    ::flock(m_fid, LOCK_UN);
}

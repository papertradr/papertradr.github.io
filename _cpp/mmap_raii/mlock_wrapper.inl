/**
 * @brief Construct a new Mlock< T>:: Mlock object
 *
 * @tparam T
 * @param size
 * @param filename
 * @param readonly
 */
template <typename T>
inline Mlock<T>::Mlock(int size, std::string filename, bool readonly)
    : m_mmap(Mmap<T>(size, filename, readonly)), m_lock_status(-1)
{
    m_lock_status = ::mlock(m_mmap.m_ptr, m_mmap.m_mapsize);
    if (m_lock_status < 0)
    {
        throw MlockFailException();
    }
    std::cout << "mlock at " << m_mmap.m_ptr << " status " << m_lock_status << "\n";
};


template <typename T>
inline T &Mlock<T>::data()
{
    return m_mmap.data();
}

/**
 * @brief Destroy the Mlock< T>:: Mlock object
 *
 * @tparam T
 */
template <typename T>
inline Mlock<T>::~Mlock()
{
    if (m_lock_status >= 0)
    {
        ::munlock(static_cast<void *>(m_mmap.m_ptr), m_mmap.m_mapsize);
        std::cout << "munlock at " << m_mmap.m_ptr << "\n";
    }
};

#pragma once
#ifndef TORCHTOOLS_H_
#define TORCHTOOLS_H_

#include <torch/script.h>
#include <torch/torch.h>
#include <vector>

namespace torchtools
{

/**
 * @brief
 *
 * @tparam T
 * @param x
 * @return std::vector<T>
 */
template <typename T>
std::vector<T> tensorToVector(torch::Tensor x)
{
    auto type = x.options().dtype().name();
    x = x.contiguous();
    std::cout << type << std::endl;
    if (type == "double")
    {
        return std::vector<T>(x.data_ptr<double>(), x.data_ptr<double>() + x.numel());
    }
    else if (type == "float")
    {
        return std::vector<T>(x.data_ptr<float>(), x.data_ptr<float>() + x.numel());
    }
    else
    {
        std::cerr << "TensorToVector does not support type " << type << std::endl;
        return std::vector<T>{};
    }
}


/**
 * @brief
 *
 * @param x
 * @param shape
 * @return torch::Tensor
 */
inline torch::Tensor vectorToTensor(std::vector<float> x, c10::IntArrayRef shape)
{
    auto torch_options = torch::TensorOptions().dtype(torch::kFloat32);
    return torch::from_blob(x.data(), shape, torch_options).clone();
}

/**
 * @brief
 *
 * @tparam T
 * @param x
 * @param shape
 * @return torch::Tensor
 */
inline torch::Tensor vectorToTensor(std::vector<double> x, c10::IntArrayRef shape)
{
    auto torch_options = torch::TensorOptions().dtype(torch::kFloat64);
    return torch::from_blob(x.data(), shape, torch_options).clone();
}

/**
 * @brief
 *
 * @param array_ptr
 * @param shape
 * @return torch::Tensor
 */
inline torch::Tensor arrayToTensor(double *array_ptr, c10::IntArrayRef shape)
{
    auto torch_options = torch::TensorOptions().dtype(torch::kFloat64);
    return torch::from_blob(array_ptr, shape, torch_options).clone();
}

/**
 * @brief
 *
 * @param array_ptr
 * @param shape
 * @return torch::Tensor
 */
inline torch::Tensor arrayToTensor(float *array_ptr, c10::IntArrayRef shape)
{
    auto torch_options = torch::TensorOptions().dtype(torch::kFloat32);
    return torch::from_blob(array_ptr, shape, torch_options).clone();
}

/**
 * @brief
 *
 * @tparam T
 * @param x
 * @return T
 */
template <typename T>
T tensorToScalar(torch::Tensor x)
{
    int total_size = 0;
    std::for_each(std::begin(x.sizes()), std::end(x.sizes()), [&](const auto d) { total_size += d; });
    assert(total_size == 0);

    return std::vector<T>(x.data_ptr<T>(), x.data_ptr<T>() + x.numel())[0];
}


/**
 * @brief
 *
 * @tparam T
 * @param x
 */
template <typename T>
void print_vector(std::vector<T> x)
{
    std::for_each(std::begin(x), std::end(x), [&](const T d) { std::cout << d << ", "; });
    std::cout << std::endl;
}


/**
 * @brief
 *
 * @tparam T
 * @param x
 */
template <typename T>
void print_intarrayref(T x)
{
    std::for_each(std::begin(x), std::end(x), [&](auto d) { std::cout << d << ", "; });
    std::cout << std::endl;
}

/**
 * @brief
 *
 * @param x
 */
inline void print_tensor(torch::Tensor x)
{
    std::cout << x << std::endl;
}

} // namespace torchtools


#endif

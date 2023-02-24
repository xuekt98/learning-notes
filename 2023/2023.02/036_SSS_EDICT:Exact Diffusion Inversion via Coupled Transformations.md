# EDICT: Exact Diffusion Inversion via Coupled Transformations

## 1. Introduction
Diffusion模型可以在给定噪声的条件下生成图像，那么类似于GAN Inversion，如何对于一张图像找到一个与之对应的噪声对于Diffusion模型也是一个很重要的问题，称作 Diffusion Inversion。现有的方法是基于DDIM的Inversion方法，但是真实图像通过DDIM的Inversion是不稳定的，因为它依赖于局部线性化的假设，这会导致错误传播，从而导致不正确的图像重建和内容丢失。

本文提出了一种新的Diffusion Inversion的方法，一种从Flow的设计中汲取灵感的方法，称作 Exact Diffusion Inversion via Coupled Transformations（EDICT）
  

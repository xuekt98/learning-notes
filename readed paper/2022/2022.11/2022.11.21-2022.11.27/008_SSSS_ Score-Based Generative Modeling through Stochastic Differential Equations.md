# Score-Based Generative Modeling through Stochastic Differential Equations

## 1.Introduction
本文在Score-Based Model和DDPM的基础上，将离散的过程转化为更一般的连续的随机微分方程（Stochastic Differential Equation，SDE）的形式。前向的随机过程逐步将复杂的数据平滑的转化到已知的分布（比如标准正态分布）上，而反向的过程则通过神经网络来学习前向过程对应的反向SDE。

本文的主要贡献：  
1. 本文提出了利用连续的随机微分方程的形式建模生成模型。并相应的设计了flexible采样过程，可以用于不同的设计的SDE。第一种采样过程使用了Predictor-Corrector的结构。第二种则是将SDE转化为其对应的SDE从而达到可控的目的。
2. 本文提出了一种在不改变无条件SDE的前提下，额外增加一个分类器网络，从而达到有条件生成的方法。
3. 作者通过实验证明本文的SDE的方法将现有的SMLD和DDPM等模型统一起来，

## 2.Method
gamma = self.gammas[k]

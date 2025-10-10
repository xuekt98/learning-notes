### 2015.11.04 Unsupervised-Pretraining
#### [Semi-supervised Sequence Learning](https://arxiv.org/pdf/1511.01432.pdf)  
Google的工作提出了一个重要的思想，从无监督步骤获得的参数可以用作其他监督训练模型的起点。比如对于自然语言处理（Natural Language Processing，NLP）问题，可以先用VAE将输入语言序列编码，然后重建。之后将这种无监督训练的VAE用于其他有监督的任务。

### 2017.12.06 Transformer
#### [Attention is all you need!](https://arxiv.org/pdf/1706.03762.pdf)   
2017年 Google Brain提出的Transformer模型是之后所有GPT系列模型的基础。


### 2018.06.11 GPT
#### [Improving language understanding with unsupervised learning](https://openai.com/research/language-unsupervised)  
#### [Improving Language Understanding by Generative Pre-Training](https://cdn.openai.com/research-covers/language-unsupervised/language_understanding_paper.pdf)  
2018年，OpenAI训练了GPT第一代模型。GPT（Generative Pre-Training）生成式预训练。GPT是Transformer和unsupervised pre-training结合的产物。  

首先，在未标记数据上使用语言建模目标来学习神经网络模型的初始参数。随后，使用相应的监督目标使这些参数适应目标任务。

本文在四个任务上测试方法的有效性：Natural Language Inference；Question Answering；Semantic Similarity；Text Classification

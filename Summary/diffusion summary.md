# Diffusion Summary

## 0. ORIGIN
#### [Deep Unsupervised Learning using Nonequilibrium Thermodynamics](https://arxiv.org/pdf/1503.03585.pdf)
**<font color=#CC00CC>grade:</font>** <font color=yellow>$\bigstar\bigstar\bigstar\bigstar\bigstar$</font>  
**<font color=#CC00CC>source&date:</font>** <font color=Yellow>ICML 2015, 2015-11-18</font>  
**<font color=#CC00CC>author:</font>** Jascha Sohl-Dickstein, Eric A. Weiss, Niru Maheswaranathan, Surya Ganguli       
**<font color=#CC00CC>institution:</font>** Stanford, UC Berkeley   
**<font color=#CC00CC>applications:</font>** <font color=LimeGreen>unconditional image synthesis</font>  
**<font color=#CC00CC>description:</font>** 开山鼻祖  

#### [Denoising diffusion probabilistic models](https://arxiv.org/pdf/2006.11239.pdf)
**<font color=#CC00CC>grade:</font>** <font color=yellow>$\bigstar\bigstar\bigstar\bigstar\bigstar$</font>   
**<font color=#CC00CC>source&date:</font>** <font color=Yellow>NIPS 2020, 2020-12-16</font>     
**<font color=#CC00CC>author:</font>** Jonathan Ho, Ajay Jain, Pieter Abbeel      
**<font color=#CC00CC>institution:</font>** UC Berkeley  
**<font color=#CC00CC>applications:</font>** <font color=LimeGreen>unconditional image synthesis</font>  
**<font color=#CC00CC>description:</font>** 集大成者  
**<font color=#CC00CC>other info:</font>** [笔记链接](https://blog.csdn.net/D_Trump/article/details/125419693?spm=1001.2014.3001.5501)  


## 1. Classical Papers
#### [Score-Based Generative Modeling through Stochastic Differential Equations](https://arxiv.org/abs/2011.13456)
**<font color=#CC00CC>grade:</font>** <font color=yellow>$\bigstar\bigstar\bigstar\bigstar$</font>  
**<font color=#CC00CC>source&date:</font>** ICLR 2021, 2021.2.10  
**<font color=#CC00CC>author:</font>** Yang Song, Jascha Sohl-Dickstein, Diederik P. Kingma, Abhishek Kumar, Stefano Ermon, Ben Poole       
**<font color=#CC00CC>institution:</font>** Stanford University, Google Brain  
**<font color=#CC00CC>applications:</font>** <font color=LimeGreen>Unconditional Image Synthesis; Class-conditional Image Synthesis</font>  
**<font color=#CC00CC>description:</font>**  
**<font color=#CC00CC>other info:</font>**



## 2. Application and Generalization Papers
### 2.1 2D synthesis and manipulation

#### [Anti-DreamBooth: Protecting users from personalized text-to-image synthesis](https://arxiv.org/pdf/2303.15433.pdf)  
**<font color=#CC00CC>grade:</font>** <font color=yellow>$\bigstar$</font>  
**<font color=#CC00CC>source&date:</font>** Arxiv 2023.03.27  
**<font color=#CC00CC>author:</font>** Thanh Van Le, Hao Phung, Thuan Hoang Nguyen, Quan Dao, Ngoc Tran, Anh Tran  
**<font color=#CC00CC>institution:</font>** VinAI Research  
**<font color=#CC00CC>applications:</font>** <font color=LimeGreen>text-to-image synthesis</font>  
**<font color=#CC00CC>description:</font>** 现有的文本-图像模型DreamBooth的功能过于强大，如果被错误使用会带来社会问题。本文旨在防止DreamBooth的这种滥用。做法是给每个用户的图像添加细微的噪声扰动，以破坏在这些扰动图像上DreamBooth的生成质量，从而保护用户信息。  
**<font color=#CC00CC>other info:</font>** <font color=Wheat>与我们的方向相关性不太大</font>  


#### [Your Diffusion Model is Secretly a Zero-Shot Classifier](https://arxiv.org/abs/2303.16203)
**<font color=#CC00CC>grade:</font>** <font color=yellow>$\bigstar\bigstar\bigstar$</font>  
**<font color=#CC00CC>source&date:</font>** Arxiv 2023.03.29  
**<font color=#CC00CC>author:</font>** Alexander C. Li, Mihir Prabhudesai, Shivam Duggal, Ellis Brown, Deepak Pathak       
**<font color=#CC00CC>institution:</font>** Carnegie Mellon University   
**<font color=#CC00CC>applications:</font>** <font color=LimeGreen>Classification</font>  
**<font color=#CC00CC>description:</font>** 本文的主要思想是利用生成模型来做判别，利用预训练好的Diffusion进行分类。具体做法就是对于给定的图片，通过将不同类别作为条件输入给diffusion的某一步，找到损失最小的条件就是该图片的分类。  
**<font color=#CC00CC>other info:</font>**  


#### [Diffusion Models as Masked Autoencoders](https://arxiv.org/abs/2304.03283)
**<font color=#CC00CC>grade:</font>** <font color=yellow>$\bigstar\bigstar$</font>  
**<font color=#CC00CC>source&date:</font>** Arxiv 2023.04.06  
**<font color=#CC00CC>author:</font>** Chen Wei, Karttikeya Mangalam, Po-Yao Huang, Yanghao Li, Haoqi Fan, Hu Xu, Huiyu Wang, Cihang Xie, Alan Yuille, Christoph Feichtenhofer       
**<font color=#CC00CC>institution:</font>** Johns Hopkins University, Meta AI, UC Santa Cruz  
**<font color=#CC00CC>applications:</font>** <font color=LimeGreen>Inpainting</font>  
**<font color=#CC00CC>description:</font>** 结合了Diffusion和MaskedVAE，但是从本质上来看主要对Diffusion有两个方面改动，一方面是利用无mask部分来预测mask部分，另一方面是不再利用UNet，而是利用Vision Transformer的结构。  
**<font color=#CC00CC>other info:</font>** <font color=yellow>本文对我们主要的启发是在于另辟蹊径，用diffusion做recognition的先验。</font>  




### 2.2 3D synthesis and manipulation
#### [Debiasing Scores and Prompts of 2D Diffusion for Robust Text-to-3D Generation](https://arxiv.org/abs/2303.15413)
**<font color=#CC00CC>grade:</font>** <font color=yellow>$\bigstar \bigstar \bigstar$</font>  
**<font color=#CC00CC>source&date:</font>** Arxiv 2023.03.27   
**<font color=#CC00CC>author:</font>** Susung Hong, Donghoon Ahn, Seungryong Kim   
**<font color=#CC00CC>institution:</font>** Korea University  
**<font color=#CC00CC>applications:</font>** <font color=LimeGreen>text-to-3D synthesis</font>  
**<font color=#CC00CC>description:</font>** 本文主要解决text-to-3D生成过程中的view inconsistency问题。基于的baseline是DreamFusion，方法是加入了score debiasing来使得2D的score无偏，加入prompt debiasing使得文本信息无偏。   
**<font color=#CC00CC>other info:</font>** <font color=yellow>本文的方法比较有启发性。特别是3D与2D之间联系的推导部分。</font>



## 3. Schrodinger Bridge
#### [Diffusion Schrödinger Bridge with Applications to Score-Based Generative Modeling](https://arxiv.org/pdf/2106.01357.pdf)
**<font color=#CC00CC>grade:</font>** <font color=yellow>$\bigstar\bigstar\bigstar$</font>  
**<font color=#CC00CC>source&date:</font>** NIPS 2021，2021.05.22   
**<font color=#CC00CC>author:</font>** Valentin De Bortoli, James Thornton, Jeremy Heng, Arnaud Doucet       
**<font color=#CC00CC>institution:</font>** Oxford  
**<font color=#CC00CC>applications:</font>** <font color=LimeGreen>2D Toy, unconditional image synthesis</font>  
**<font color=#CC00CC>description:</font>**   
IPF训练两个SDE。  
问题：实验简单，分辨率低32x32，IPF训练时间长  
**<font color=#CC00CC>other info:</font>**  


#### [Deep Generative Learning via Schrödinger Bridge](https://arxiv.org/abs/2106.10410)
**<font color=#CC00CC>grade:</font>** <font color=yellow>$\bigstar\bigstar\bigstar$</font>  
**<font color=#CC00CC>source&date:</font>** ICML 2021, 2021.07.30  
**<font color=#CC00CC>author:</font>** Gefei Wang, Yuling Jiao, Qian Xu, Yang Wang, Can Yang       
**<font color=#CC00CC>institution:</font>** Wuhan University  
**<font color=#CC00CC>applications:</font>** <font color=LimeGreen>2D Toy, unconditional image synthesis, image interpolation, inpainting</font>  
**<font color=#CC00CC>description:</font>**  
Arguments：（1）现有的生成模型的理论和实际效果之间存在差距。（2）对于数据分布需要有较强的假设。  
薛定谔桥，两阶段采样，先从0采到一个带噪声图像，第二阶段细化结果。  
问题：（1）实验简单，分辨率低 64x64  
**<font color=#CC00CC>other info:</font>**  


#### [Solving Schrödinger Bridges via Maximum Likelihood](https://arxiv.org/abs/2106.02081)
**<font color=#CC00CC>grade:</font>** <font color=yellow>$\bigstar\bigstar\bigstar$</font>  
**<font color=#CC00CC>source&date:</font>** MDPI Entropy 2021.08.31  
**<font color=#CC00CC>author:</font>** Francisco Vargas, Pierre Thodoroff, Neil D. Lawrence, Austen Lamacraft       
**<font color=#CC00CC>institution:</font>** Cambridge University  
**<font color=#CC00CC>applications:</font>** <font color=LimeGreen>1D Toy, 2D Toy</font>  
**<font color=#CC00CC>description:</font>** 本文的主要贡献是证明了解决SBP和自回归最大似然估计目标之间的等价性。提出了IPML。  
问题：实验简单，没有图像实验。  
**<font color=#CC00CC>other info:</font>**


#### [Likelihood Training of Schrödinger Bridge using Forward-Backward SDEs Theory](https://arxiv.org/abs/2110.11291)
**<font color=#CC00CC>grade:</font>** <font color=yellow>$\bigstar\bigstar\bigstar\bigstar$</font>  
**<font color=#CC00CC>source&date:</font>** ICLR 2022， 2022.01.29  
**<font color=#CC00CC>author:</font>** Tianrong Chen, Guan-Horng Liu, Evangelos A. Theodorou       
**<font color=#CC00CC>institution:</font>** Georgia Institute of Technology, USA  
**<font color=#CC00CC>applications:</font>** <font color=LimeGreen>Toy, Image Synthesis MNIST CelebA CIFAR10</font>  
**<font color=#CC00CC>description:</font>**  
Arguments：原来的方法依赖于mean-matching，或者IPF  
Methodology：利用求log似然来求SB问题，建立了求解SB问题和生成模型训练之间的联系。
问题：实验简单  
**<font color=#CC00CC>other info:</font>**  


#### [Consistency Models](https://arxiv.org/abs/2303.01469)
**<font color=#CC00CC>grade:</font>** <font color=yellow>$\bigstar\bigstar\bigstar\bigstar$</font>  
**<font color=#CC00CC>source&date:</font>** Arxiv 2023.03.02  
**<font color=#CC00CC>author:</font>** Yang Song, Prafulla Dhariwal, Mark Chen, Ilya Sutskever       
**<font color=#CC00CC>institution:</font>** unknown  
**<font color=#CC00CC>applications:</font>** <font color=LimeGreen>Image Synthsis</font>  
**<font color=#CC00CC>description:</font>** 整合ODE和SDE的方法，提出了既可以一步得到结果，又可以多步修正的模型  
**<font color=#CC00CC>other info:</font>**


#### [Stochastic Interpolants: A Unifying Framework for Flows and Diffusions](https://arxiv.org/abs/2303.08797)
**<font color=#CC00CC>grade:</font>** <font color=yellow>$\bigstar\bigstar\bigstar\bigstar$</font>  
**<font color=#CC00CC>source&date:</font>** Arxiv 2023.03.27  
**<font color=#CC00CC>author:</font>** Michael S. Albergo, Nicholas M. Boffi, Eric Vanden-Eijnden       
**<font color=#CC00CC>institution:</font>** New York University  
**<font color=#CC00CC>applications:</font>** <font color=LimeGreen>Toy</font>  
**<font color=#CC00CC>description:</font>** 将Flow，Diffusion，ODE，SDE全部用Stochastic Interpolants统一起来。很具有借鉴意义。但是本文没有在图像上的实验。  
**<font color=#CC00CC>other info:</font>**  



#### [Diffusion Schrödinger Bridge Matching](https://arxiv.org/abs/2303.16852)
**<font color=#CC00CC>grade:</font>** <font color=yellow>$\bigstar\bigstar\bigstar$</font>  
**<font color=#CC00CC>source&date:</font>** Arxiv 2023.03.29  
**<font color=#CC00CC>author:</font>** Yuyang Shi, Valentin De Bortoli, Andrew Campbell, Arnaud Doucet       
**<font color=#CC00CC>institution:</font>** Oxford  
**<font color=#CC00CC>applications:</font>** <font color=LimeGreen>Toy, MNIST</font>  
**<font color=#CC00CC>description:</font>** 将Diffusion和Flow用DSBM统一起来。  
**<font color=#CC00CC>other info:</font>**  


#### [I2SB: Image-to-Image Schrödinger Bridge](https://arxiv.org/abs/2302.05872)
**<font color=#CC00CC>grade:</font>** <font color=yellow>$\bigstar\bigstar\bigstar$</font>  
**<font color=#CC00CC>source&date:</font>** Arxiv 2023.04.01  
**<font color=#CC00CC>author:</font>** Guan-Horng Liu, Arash Vahdat, De-An Huang, Evangelos A. Theodorou, Weili Nie, Anima Anandkumar       
**<font color=#CC00CC>institution:</font>** unknown  
**<font color=#CC00CC>applications:</font>** <font color=LimeGreen>Inpainting，Super-Resolution，Deblurring，JPEG restoration</font>  
**<font color=#CC00CC>description:</font>** 用SB来解释Diffusion，其实跟Diffusion差别不大，只是在设计上有些不同   
**<font color=#CC00CC>other info:</font>**


#### [Diffusion Bridge Mixture Transports, Schrödinger Bridge Problems and Generative Modeling](https://arxiv.org/abs/2304.00917)
**<font color=#CC00CC>grade:</font>** <font color=yellow>$\bigstar\bigstar\bigstar$</font>  
**<font color=#CC00CC>source&date:</font>** Arxiv 2023.04.03  
**<font color=#CC00CC>author:</font>** Stefano Peluchetti       
**<font color=#CC00CC>institution:</font>** Cogent Labs  
**<font color=#CC00CC>applications:</font>** <font color=LimeGreen>Toy， unconditional image synthesis</font>  
**<font color=#CC00CC>description:</font>**  
Arguments: IPF需要大量的迭代；sampling-based方法有simulation-Inference mismatch  
本文提出了一种新的sample-based iterative algorithm，IDBM，可以解决这两个问题
**<font color=#CC00CC>other info:</font>**  





#### [title](link)
**<font color=#CC00CC>grade:</font>** <font color=yellow>$\bigstar$</font>  
**<font color=#CC00CC>source&date:</font>**  
**<font color=#CC00CC>author:</font>**       
**<font color=#CC00CC>institution:</font>**  
**<font color=#CC00CC>applications:</font>** <font color=LimeGreen></font>  
**<font color=#CC00CC>description:</font>**  
**<font color=#CC00CC>other info:</font>**  

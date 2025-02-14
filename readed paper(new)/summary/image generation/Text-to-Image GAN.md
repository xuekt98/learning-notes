#### 001. [Generative Adversarial Nets](https://proceedings.neurips.cc/paper_files/paper/2014/file/5ca3e9b122f61f8f06494c97b1afccf3-Paper.pdf)

**NIPS 2014** 

GAN的最原始的文章

</br>


#### 002. [Generative Adversarial Text to Image Synthesis](https://proceedings.mlr.press/v48/reed16.pdf)

**ICML 2016**

![img](res/T2I%20GAN/002-1.png)

本文基于Conditional GAN实现text-to-image generation, 是GAN在T2I上的foundational work

</br>


#### 003. [GALIP: Generative Adversarial CLIPs for Text-to-Image Synthesis](https://openaccess.thecvf.com/content/CVPR2023/papers/Tao_GALIP_Generative_Adversarial_CLIPs_for_Text-to-Image_Synthesis_CVPR_2023_paper.pdf)

**CVPR 2023**

![img](res/T2I%20GAN/003-1.png)

本文结合了CLIP-ViT和GAN进行text-to-image generation

</br>


#### 004. [StackGAN: Text to Photo-Realistic Image Synthesis With Stacked Generative Adversarial Networks](https://openaccess.thecvf.com/content_ICCV_2017/papers/Zhang_StackGAN_Text_to_ICCV_2017_paper.pdf)

**ICCV 2017**

![img](res/T2I%20GAN/004-1.png)

Two-stage GAN. In the first stage, basic shapes and colors were drawn on the basis of the given text description to produce low-resolution images. In the second stage, the output from the first stage was refined by combining it with the text description to generate high-resolution images. 

</br>


#### 005. [StackGAN++: Realistic Image Synthesis with Stacked Generative Adversarial Networks](https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=8411144)

**TPAMI 2019**

![img](res/T2I%20GAN/005-1.png)

与StackGAN的区别在于, adopt a tree structure with multiple generators and
discriminators to improve image generation

</br>


#### 006. [AttnGAN: Fine-Grained Text to Image Generation With Attentional Generative Adversarial Networks](https://openaccess.thecvf.com/content_cvpr_2018/papers/Xu_AttnGAN_Fine-Grained_Text_CVPR_2018_paper.pdf)

**CVPR 2018**

![img](res/T2I%20GAN/006-1.png)

在StackGAN的基础上加入了Attention

</br>


#### 007. [Semi-supervised FusedGAN for Conditional Image Generation](https://openaccess.thecvf.com/content_ECCV_2018/papers/Navaneeth_Bodla_Semi-supervised_FusedGAN_for_ECCV_2018_paper.pdf)

**CVPR 2018**

![img](res/T2I%20GAN/007-1.png)

采用了两个generator分别用于unconditional和conditional generation

</br>


#### 008. [Photographic text-to-image synthesis with a hierarchically-nested adversarial network](https://openaccess.thecvf.com/content_cvpr_2018/papers/Zhang_Photographic_Text-to-Image_Synthesis_CVPR_2018_paper.pdf)

**CVPR 2018**

![img](res/T2I%20GAN/008-1.png)

HDGAN与stackGAN的不同之处在于end-to-end的训练

</br>


#### 009 

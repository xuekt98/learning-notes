# High Resolution Image Editing via Multi-Stage Blended diffusion
本文写的不是那么正规，应该是放在Arxiv上占坑的，懂得都懂（/doge）

本文通过多个阶段的Blended Diffusion实现了高分辨率的图像编辑。

![img](res/018/001.png)

具体的操作是首先将高分辨率的要编辑的图像中需要编辑的部分进行crop， 对于crop的图降采样从而满足diffusion模型输入的要求。之后用Blended Latent Diffusion得到一组5个编辑后的结果，这里作者结合了Repaint的方法。之后通过CLIP，从5个结果中选择一个最好的结果。最后再用Real-ESRGAN上采样到高分辨率的图像上。

当输出图像的分辨率过于大的时候，本文将图像分割成重叠的块，然后再用alpha compositing拼接起来。

![img](res/018/002.png)

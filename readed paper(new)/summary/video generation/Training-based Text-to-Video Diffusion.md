# Training-based Text-to-Video Diffusion

#### 001 [Video Diffusion Models](https://proceedings.neurips.cc/paper_files/paper/2022/file/39235c56aef13fb05a6adc95eb9d8d66-Paper-Conference.pdf)

**NIPS 2022**

![img](res/Training-based%20Text-to-Video%20Diffusion/001-1.png)

VDM将原始的Diffusion的2D U-Net替换成3D U-Net, 其中的2D卷积替换成3D卷积, temporal Attention通过在frame轴进行Attention实现.  

joint training with both images and videos to improve performance

一次只能生成固定长度16帧的视频. requires paired video-text datasets

</br>


#### 002 [Make-A-Video: Text-to-Video Generation without Text-Video Data](https://arxiv.org/pdf/2209.14792)

**ICLR 2023**

![img](res/Training-based%20Text-to-Video%20Diffusion/002-1.png)

learn what the world looks like and how it is described from paired text-image data, and learn how the world moves from unsupervised video footage.

整体包含了四个部分, 文本prior模型, 图像Diffusion, 两个超分辨率模型. Prior 在image-text pair上训练, 其他各个部分先在图像数据集(no aligned text)上训练, 之后加入temporal模块并在unconditional的视频上fine-tune. 其 3D convolution 和 temporal Attention的设计与VDM类似.  

</br>


#### 003 [MagicVideo: Efficient Video Generation With Latent Diffusion Models](https://arxiv.org/pdf/2211.11018)

**Arxiv 2022**

![img](res/Training-based%20Text-to-Video%20Diffusion/003-1.png)

早期采用LDM类似的隐空间实现T2V的工作. 额外训练video VAE.  

</br>


#### 004 [Latent Video Diffusion Models for High-Fidelity Long Video Generation](https://arxiv.org/pdf/2211.13221)

**Arxiv 2023**

![img](res/Training-based%20Text-to-Video%20Diffusion/004-1.png)

hierarchical framework

</br>


#### 005 [Swap Attention in Spatiotemporal Diffusions for Text-to-Video Generation](https://arxiv.org/pdf/2305.10874)  

**Arxiv 2023**

![img](res/Training-based%20Text-to-Video%20Diffusion/005-1.png)

提出了一种新的swap Attention结构

</br>


#### 006 [ModelScope Text-to-Video Technical Report](https://arxiv.org/pdf/2308.06571)

**Arxiv 2023**

![img](res/Training-based%20Text-to-Video%20Diffusion/006-1.png)

![img](res/Training-based%20Text-to-Video%20Diffusion/006-2.png)

ModelScope

基于LDM类似的latent space结构, 引入spatial temporal convolution and attention

</br>


#### 007 [Latent-Shift: Latent Diffusion with Temporal Shift for Efficient Text-to-Video Generation](https://arxiv.org/pdf/2304.08477)

**Arxiv 2023**

![img](res/Training-based%20Text-to-Video%20Diffusion/007-1.png)

shifts channels between adjacent frames in convolution blocks for temporal modeling. the model maintains the original T2I capability while generating videos.  

</br>


#### 008 [Imagen Video: High Definition Video Generation with Diffusion Models](https://arxiv.org/pdf/2210.02303)

**Arxiv 2022**

![img](res/Training-based%20Text-to-Video%20Diffusion/008-1.png)

using a cascaded video diffusion model composed of seven sub-models: one for base video generation, three for spatial super-resolution, and three for temporal super-resolution.  

</br>


#### 009 [Align Your Latents: High-Resolution Video Synthesis With Latent Diffusion Models](https://openaccess.thecvf.com/content/CVPR2023/papers/Blattmann_Align_Your_Latents_High-Resolution_Video_Synthesis_With_Latent_Diffusion_Models_CVPR_2023_paper.pdf)

**CVPR 2023**



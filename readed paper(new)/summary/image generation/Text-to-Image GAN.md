#### 001 [Generative Adversarial Nets](https://proceedings.neurips.cc/paper_files/paper/2014/file/5ca3e9b122f61f8f06494c97b1afccf3-Paper.pdf)

**NIPS 2014** 

GAN的最原始的文章

</br>


#### 002 [Generative Adversarial Text to Image Synthesis](https://proceedings.mlr.press/v48/reed16.pdf)

**ICML 2016**

![img](res/T2I%20GAN/002-1.png)

本文基于Conditional GAN实现text-to-image generation, 是GAN在T2I上的foundational work

</br>


#### 003 [GALIP: Generative Adversarial CLIPs for Text-to-Image Synthesis](https://openaccess.thecvf.com/content/CVPR2023/papers/Tao_GALIP_Generative_Adversarial_CLIPs_for_Text-to-Image_Synthesis_CVPR_2023_paper.pdf)

**CVPR 2023**

![img](res/T2I%20GAN/003-1.png)

本文结合了CLIP-ViT和GAN进行text-to-image generation

</br>


#### 004 [StackGAN: Text to Photo-Realistic Image Synthesis With Stacked Generative Adversarial Networks](https://openaccess.thecvf.com/content_ICCV_2017/papers/Zhang_StackGAN_Text_to_ICCV_2017_paper.pdf)

**ICCV 2017**

![img](res/T2I%20GAN/004-1.png)

Two-stage GAN. In the first stage, basic shapes and colors were drawn on the basis of the given text description to produce low-resolution images. In the second stage, the output from the first stage was refined by combining it with the text description to generate high-resolution images. 

</br>


#### 005 [StackGAN++: Realistic Image Synthesis with Stacked Generative Adversarial Networks](https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=8411144)

**TPAMI 2019**

![img](res/T2I%20GAN/005-1.png)

与StackGAN的区别在于, adopt a tree structure with multiple generators and
discriminators to improve image generation

</br>


#### 006 [AttnGAN: Fine-Grained Text to Image Generation With Attentional Generative Adversarial Networks](https://openaccess.thecvf.com/content_cvpr_2018/papers/Xu_AttnGAN_Fine-Grained_Text_CVPR_2018_paper.pdf)

**CVPR 2018**

![img](res/T2I%20GAN/006-1.png)

在StackGAN的基础上加入了Attention

</br>


#### 007 [Semi-supervised FusedGAN for Conditional Image Generation](https://openaccess.thecvf.com/content_ECCV_2018/papers/Navaneeth_Bodla_Semi-supervised_FusedGAN_for_ECCV_2018_paper.pdf)

**CVPR 2018**

![img](res/T2I%20GAN/007-1.png)

采用了两个generator分别用于unconditional和conditional generation

</br>


#### 008 [Photographic text-to-image synthesis with a hierarchically-nested adversarial network](https://openaccess.thecvf.com/content_cvpr_2018/papers/Zhang_Photographic_Text-to-Image_Synthesis_CVPR_2018_paper.pdf)

**CVPR 2018**

![img](res/T2I%20GAN/008-1.png)

HDGAN与stackGAN的不同之处在于end-to-end的训练

</br>


#### 009 [Controllable generative adversarial network](https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=8641270)

**IEEE Access 2019**

![img](res/T2I%20GAN/009-1.png)

ControlGAN plays a three-player game, the Generator, Discriminator and Classifier. It could also control the specitic attributes of the generated content. 

</br>


#### 010 [DM-GAN: Dynamic Memory Generative Adversarial Networks for Text-To-Image Synthesis](https://openaccess.thecvf.com/content_CVPR_2019/papers/Zhu_DM-GAN_Dynamic_Memory_Generative_Adversarial_Networks_for_Text-To-Image_Synthesis_CVPR_2019_paper.pdf)

**CVPR 2019**

![img](res/T2I%20GAN/010-1.png)

DM-GAN integrated diffusion model concepts and introduced a dynamic memory module to refine blurred image content, helping to prevent poor results during initial image generation.

</br>


#### 011 [Semantic Image Synthesis With Spatially-Adaptive Normalization](https://openaccess.thecvf.com/content_CVPR_2019/papers/Park_Semantic_Image_Synthesis_With_Spatially-Adaptive_Normalization_CVPR_2019_paper.pdf)

**CVPR 2019**

![img](res/T2I%20GAN/011-1.png)

SPADE/GauGAN proposed a novel spatially-adaptive normalization layer for semantic layout guided image generation. It can generate reaistic images from user-drawn sketches, use semantic layouts to produce photorealistic effects, thereby provide an interactive image generation experience.

</br>


#### 012 [Second-Order Attention Network for Single Image Super-Resolution](https://openaccess.thecvf.com/content_CVPR_2019/papers/Dai_Second-Order_Attention_Network_for_Single_Image_Super-Resolution_CVPR_2019_paper.pdf)


**CVPR 2019**

![img](res/T2I%20GAN/012-1.png)

MirrorGAN employed a bidirectional generation mechanism to map text to images and back, improving semantic coherence in the outputs. This model introduced a new framework that combined global and local attention with semantic preservation, redefining text-to-image generation.

</br>


#### 013 [Object-Driven Text-To-Image Synthesis via Adversarial Training](https://openaccess.thecvf.com/content_CVPR_2019/papers/Li_Object-Driven_Text-To-Image_Synthesis_via_Adversarial_Training_CVPR_2019_paper.pdf)

**CVPR 2019**

![img](res/T2I%20GAN/013-1.png)
![img](res/T2I%20GAN/013-2.png)

ObjGAN contained two stages. The first stage was using LSTM to generate the layout from text. The second  stage utilized GAN to generate image from the layout. 

</br>


#### 014 [Adversarial Learning of Semantic Relevance in Text to Image Synthesis](https://www.eecs.harvard.edu/~htk/publication/2019-aaai-cha-gwon-kung.pdf)

**AAAI 2019**

![img](res/T2I%20GAN/014-1.png)
![img](res/T2I%20GAN/014-2.png)

Text-SeGAN used semantic discriminator to solve the one-to-many problem of class label. The discriminator didn't predict the image class but the semantical coherence with the image.  

</br>


#### 015 [Panoptic-DeepLab: A Simple, Strong, and Fast Baseline for Bottom-Up Panoptic Segmentation](https://openaccess.thecvf.com/content_CVPR_2020/papers/Cheng_Panoptic-DeepLab_A_Simple_Strong_and_Fast_Baseline_for_Bottom-Up_Panoptic_CVPR_2020_paper.pdf)

**CVPR 2020**

![img](res/T2I%20GAN/015-1.png)

CookGAN/Panoptic-DeepLab adopts dual-context and dual-decoder modules for semantic segmentation and instance segmentation predictions.

</br>


#### 016 [CPGAN: Content-Parsing Generative Adversarial Networks for Text-to-Image Synthesis](https://www.ecva.net/papers/eccv_2020/papers_ECCV/papers/123490477.pdf)

**ECCV 2020**

![img](res/T2I%20GAN/016-1.png)

CPGAN [28] enhanced semantic consistency between text and images by delving deeply into their content.

</br>


#### 017 [RiFeGAN: Rich Feature Generation for Text-to-Image Synthesis From Prior Knowledge](https://openaccess.thecvf.com/content_CVPR_2020/papers/Cheng_RiFeGAN_Rich_Feature_Generation_for_Text-to-Image_Synthesis_From_Prior_Knowledge_CVPR_2020_paper.pdf)

**CVPR 2020**

![img](res/T2I%20GAN/017-1.png)
![img](res/T2I%20GAN/017-2.png)

This paper introduce a RiFeGAN. It firstly retrieve compatible captions from prior knowledge using caption matching method. Then the detailed captions are used to generate image with rich feature.  

</br>


#### 018 [SegAttnGAN: Text to Image Generation with Segmentation Attention](https://arxiv.org/pdf/2005.12444)

**Arxiv 2020**

![img](res/T2I%20GAN/018-1.png)

SegAttnGAN integrated additional segmentation information with attention mechanisms, further improving the realism of generated images.

</br>


#### 019 [Taming Transformers for High-Resolution Image Synthesis](https://openaccess.thecvf.com/content/CVPR2021/papers/Esser_Taming_Transformers_for_High-Resolution_Image_Synthesis_CVPR_2021_paper.pdf)

**CVPR 2021**

![img](res/T2I%20GAN/019-1.png)

VQGAN is the most widely used encoder and decoder and latent space for currently prevalent diffusion and VLMs.

</br>


#### 020 [Dense Contrastive Learning for Self-Supervised Visual Pre-Training](https://openaccess.thecvf.com/content/CVPR2021/papers/Wang_Dense_Contrastive_Learning_for_Self-Supervised_Visual_Pre-Training_CVPR_2021_paper.pdf)

**CVPR 2021**

![img](res/T2I%20GAN/020-1.png)

DenseCL/XMC-GAN presented a method of dense contrastive learning that implemented self-supervised learning by optimizing a pairwise contrastive similarity loss at the pixel level between two views of input images.

</br>


#### 021 [DAE-GAN: Dynamic Aspect-aware GAN for Text-to-Image Synthesis](https://openaccess.thecvf.com/content/ICCV2021/papers/Ruan_DAE-GAN_Dynamic_Aspect-Aware_GAN_for_Text-to-Image_Synthesis_ICCV_2021_paper.pdf)

**ICCV 2021**

![img](res/T2I%20GAN/021-1.png)

DAE-GAN incorporated the concepts of denoising autoencoders to improve the robustness of generated images. 

</br>


#### 022 [Cycle-Consistent Inverse GAN for Text-to-Image Synthesis](https://dl.acm.org/doi/pdf/10.1145/3474085.3475226)

**ACM MM 2021**

![img](res/T2I%20GAN/022-1.png)

CI-GAN is a three-stage model. In the first stage, a StyleGAN model is trained to generate hight quality image. In the second stage, a inversion model is trained to get the latent of the input image. In the third stage, textual input is aligned with the latent of image. The model can be used for text-to-image generation and manipulation.  

</br>


#### 023 [R-GAN: Exploring Human-like Way for Reasonable Text-to-Image Synthesis via Generative Adversarial Networks](https://dl.acm.org/doi/pdf/10.1145/3474085.3475363)

**ACM MM 2021**

![img](res/T2I%20GAN/023-1.png)

R-GAN generated coherent images in a human-like manner, demonstrating naturalness and consistency in its generation process. Four stages of generation, text -> layout -> corse-to-fine shape -> image

</br>


#### 024 [DF-GAN: A Simple and Effective Baseline for Text-to-Image Synthesis](https://openaccess.thecvf.com/content/CVPR2022/papers/Tao_DF-GAN_A_Simple_and_Effective_Baseline_for_Text-to-Image_Synthesis_CVPR_2022_paper.pdf)

**CVPR 2022**

![img](res/T2I%20GAN/024-1.png)

DF-GAN directly generated high-resolution images in the first stage and introduced a novel target-aware discriminator in the second stage to improve the consistency between text and image

</br>


#### 025 [Towards Language-Free Training for Text-to-Image Generation](https://openaccess.thecvf.com/content/CVPR2022/papers/Zhou_Towards_Language-Free_Training_for_Text-to-Image_Generation_CVPR_2022_paper.pdf)

**CVPR 2022**

![img](res/T2I%20GAN/025-1.png)

LAFITE used CLIP to guide the generation process, enhancing the quality and interpretability of the generated images.

</br>


#### 026 [Text to Image Generation With Semantic-Spatial Aware GAN](https://openaccess.thecvf.com/content/CVPR2022/papers/Liao_Text_to_Image_Generation_With_Semantic-Spatial_Aware_GAN_CVPR_2022_paper.pdf)

**CVPR 2022**

![img](res/T2I%20GAN/026-1.png)

SAGAM introduced Semantic-Spatial Aware block that learns semantic-adaptive transformation conditioned on text to effectively fuse text features and image features, and learns a semantic mask in a weakly-supervised way that depends on the current text-image fusion process in order to guide the transformation spatially.  

</br>


#### 027 [Vision-Language Matching for Text-to-Image Synthesis via Generative Adversarial Networks](https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=9930667)

**IEEE TMM**

![img](res/T2I%20GAN/027-1.png)

VLMGAN combined visual and language models to improve semantic understanding capabilities in image generation.  

</br>


#### 028 [VQGAN-CLIP: Open Domain Image Generation and Editing with Natural Language Guidance](https://arxiv.org/pdf/2204.08583)

**ECCV 2022**

![img](res/T2I%20GAN/028-1.png)

VQGAN-CLIP is a training-free method for text-to-image generation and manipulation. It used CLIP similarity to optimize the latent vector of VQGAN. But the manipulation results suffer from information leakage.  

</br>


#### 029 [TISE: Bag of Metrics for Text-to-Image Synthesis Evaluation](https://arxiv.org/pdf/2112.01398)

**ECCV 2022**

![img](res/T2I%20GAN/029-1.png)

This paper proposed several novel image generation metrics and AttnGAN++  

</br>


#### 030 [Recurrent Affine Transformation for Text-to-Image Synthesis](https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=10100901)

**IEEE TMM 2023**

![img](res/T2I%20GAN/030-1.png)

RAT-GAN adopted recursive affine transformations to incorporate conditional information during generation. A novel kind of information injecting mechanism.  

</br>


#### 031 [GALIP: Generative Adversarial CLIPs for Text-to-Image Synthesis](https://openaccess.thecvf.com/content/CVPR2023/papers/Tao_GALIP_Generative_Adversarial_CLIPs_for_Text-to-Image_Synthesis_CVPR_2023_paper.pdf)

**CVPR 2023**

![img](res/T2I%20GAN/031-1.png)

GALIP legerages CLIP model both in the generator and discriminator.

</br>


#### 032 [Scaling Up GANs for Text-to-Image Synthesis](https://openaccess.thecvf.com/content/CVPR2023/papers/Kang_Scaling_Up_GANs_for_Text-to-Image_Synthesis_CVPR_2023_paper.pdf)

**CVPR 2023**

![img](res/T2I%20GAN/032-1.png)

This paper proposed GigaGAN to increase the text-to-image generation capacity of GAN models based the investigation that naively increasing the capacity of the StyleGAN architecture quickly becomes unstable. GigaGAN achieved high-quality image generation through large-scale data training, surpassing the state-of-the-art performance of diffusion model.

</br>


#### 033 [StyleGAN-T: Unlocking the Power of GANs for Fast Large-Scale Text-to-Image Synthesis](https://proceedings.mlr.press/v202/sauer23a/sauer23a.pdf)

**ICML PMLR 2023**

![img](res/T2I%20GAN/033-1.png)

StyleGAN-T utilized the structure of StyleGAN for text-to-image generation. It could also achieve style transfer with text condition.

</br>


#### 034 [Text-to-Image Synthesis Based on Object-Guided Joint-Decoding Transformer](https://openaccess.thecvf.com/content/CVPR2022/papers/Wu_Text-to-Image_Synthesis_Based_on_Object-Guided_Joint-Decoding_Transformer_CVPR_2022_paper.pdf)

**CVPR 2022**

![img](res/T2I%20GAN/034-1.png)

Layout-VQGAN used layout information to generate complex scenes, enchancing the structural representation of the generated images.

</br>


#### 035 [Drag Your GAN: Interactive Point-based Manipulation on the Generative Image Manifold](https://dl.acm.org/doi/pdf/10.1145/3588432.3591500)

**ACM SIGGRAPH 2023**

![img](res/T2I%20GAN/035-1.png)

DragGAN introduced a point-based interactive image editing method, allowing pixel-level precision in the editing results.

</br>


#### 036 [UFOGen: You Forward Once Large Scale Text-to-Image Generation via Diffusion GANs](https://openaccess.thecvf.com/content/CVPR2024/papers/Xu_UFOGen_You_Forward_Once_Large_Scale_Text-to-Image_Generation_via_Diffusion_CVPR_2024_paper.pdf)

**CVPR 2024**

![img](res/T2I%20GAN/036-1.png)

UFOGen aims at ultra-fast one-step T2I using a hybrid approach that combines diffusion models with GAN objectives.

</br>


#### 037 [Adversarial Text to Continuous Image Generation](https://openaccess.thecvf.com/content/CVPR2024/papers/Haydarov_Adversarial_Text_to_Continuous_Image_Generation_CVPR_2024_paper.pdf)

**CVPR 2024**

![img](res/T2I%20GAN/037-1.png)

HyperCGAN addresses the T2I task from a different perspective, representing two-dimensional images as implicit neural representations (INRs) and controlling the INR-GAN generation process using weight modulation operators based on wordlevel attention, through the use of a supernetwork.

</br>






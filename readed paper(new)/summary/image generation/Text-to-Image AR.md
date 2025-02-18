#### 001 [Generative Pretraining From Pixels](https://proceedings.mlr.press/v119/chen20s/chen20s.pdf)

**ICML 2020**

![img](res/T2I%20AR/001-1.png)

iGPT is a significant work that brought Transformers into the realm of image generation. 尝试了sequential AR和BERT两种结构.

</br>


#### 002 [Zero-Shot Text-to-Image Generation](https://proceedings.mlr.press/v139/ramesh21a/ramesh21a.pdf)

**ICML 2021**

![img](res/T2I%20AR/002-1.png)

DALL-E包含了两个阶段的模型, 第一个阶段训练VQ-VAE, 第二个阶段训练Transformer.

</br>


#### 003 [CogView: Mastering Text-to-Image Generation via Transformers](https://proceedings.neurips.cc/paper_files/paper/2021/file/a4d92e2cd541fca87e4620aba658316d-Paper.pdf)

**NIPS 2021**

![img](res/T2I%20AR/003-1.png)

CogView实现思路与DALL-E类似, 包含了两个阶段的模型, 第一阶段VQVAE对图像进行量化, 第二阶段Transformer.   

</br>


#### 004 [M6: A Chinese Multimodal Pretrainer](https://arxiv.org/pdf/2103.00823)

**Arxiv 2021**

![img](res/T2I%20AR/004-1.png)

M6 provided a large dataset for multimodal pre-training in Chinese.

</br>


#### 005 [Scaling Autoregressive Models for Content-Rich Text-to-Image Generation](https://3dvar.com/Yu2022Scaling.pdf)

**TMLR 2022**

![img](res/T2I%20AR/005-1.png)

Parti used ViT-VQGAN as the image tokenizer, and generated image tokens in machine translation style.  

</br>


### 006 [CogView2: Faster and Better Text-to-Image Generation via Hierarchical Transformers](https://proceedings.neurips.cc/paper_files/paper/2022/file/6baec7c4ba0a8734ccbd528a8090cb1f-Paper-Conference.pdf)

**NIPS 2022**

![img](res/T2I%20AR/006-1.png)
![img](res/T2I%20AR/006-2.png)

CogView2, an upgraded version of CogView, not only improved generation quality but also supported text-based interactive image editing.

</br>


### 007 [Make-A-Scene: Scene-Based Text-to-Image Generation with Human Priors](https://arxiv.org/pdf/2203.13131)

**ECCV 2022**

![img](res/T2I%20AR/007-1.png)

Make-A-Scene introduced secene understanding capabilities, allowing users to specify elements in the generated images more precisely.

</br>


### 008 [NÜWA: Visual Synthesis Pre-training for Neural visUal World creAtion](https://arxiv.org/pdf/2111.12417)

**ECCV 2022**

![img](res/T2I%20AR/008-1.png)

NUWA is a unified multimodal pretrained model. It proposed a 3D transformer encoder-decocder framework to achieve unified training.

</br>


### 009 [Scaling Autoregressive Multi-Modal Models: Pretraining and Instruction Tuning](https://aicommenter.com/wp-content/uploads/2023/07/Scaling-Autoregressive-Multi-Modal-Models-Pretraining-and-Instruction-Tuning.pdf)

**Arxiv 2023**

![img](res/T2I%20AR/009-1.png)

CM3Leon used an improved autoregressive mechanism and became the first multimodal model trained using an approach adapted from text-specific language models.

</br>


### 010 [Generating Images with Multimodal Language Models](https://proceedings.neurips.cc/paper_files/paper/2023/file/43a69d143273bd8215578bde887bb552-Paper-Conference.pdf)

**NIPS 2023**

![img](res/T2I%20AR/010-1.png)
![img](res/T2I%20AR/010-2.png)

GILL fused frozen text-only LLMs with pre-trained image encoder and decoder models by mapping between their embedding spaces.  

</br>


### 011 [MARS: Mixture of Auto-Regressive Models for Fine-grained Text-to-image Synthesis](https://arxiv.org/pdf/2407.07614)

**Arxiv 2024**

![img](res/T2I%20AR/011-1.png)

MARS retained the NLP capabilities of LLMs while also providing them with enhanced visual understanding.  

</br>


#### 012 [Unified-IO 2: Scaling Autoregressive Multimodal Models with Vision Language Audio and Action](https://openaccess.thecvf.com/content/CVPR2024/papers/Lu_Unified-IO_2_Scaling_Autoregressive_Multimodal_Models_with_Vision_Language_Audio_CVPR_2024_paper.pdf)

**CVPR 2024**

![img](res/T2I%20AR/012-1.png)
![img](res/T2I%20AR/012-2.png)

Unified-IO 2 is the first autoregressive multi-modal model that is capable of understanding and generating image, text, audio and action.  

</br>


#### 013 [STAR: Scale-wise Text-to-image generation via Auto-Regressive representations](https://arxiv.org/pdf/2406.10797)

**Arxiv 2024**

![img](res/T2I%20AR/013-1.png)

STAR adopted a scale-wise autoregressive paradigm for T2I modeling, enhancing the coherence of the generated images and improving alignment with the text descriptions.

</br>


#### 014 [HART: Efficient Visual Generation with Hybrid Autoregressive Transformer](https://arxiv.org/pdf/2410.10812)

**Arxiv 2024**

![img](res/T2I%20AR/014-1.png)
![img](res/T2I%20AR/014-2.png)

HART introduced a hybrid tokenizer to achieve efficient high-resolution visual synthesis, combining autoregressive models with adversarial generation to enhance the diversity and realism of the generated images.

</br>


#### 015 [Accelerating Auto-regressive Text-to-Image Generation with Training-free Speculative Jacobi Decoding](https://arxiv.org/pdf/2410.01699)

**Arxiv 2024**

![img](res/T2I%20AR/015-1.png)

In this paper proposed a training-free probabilistic parallel decoding algorithm, Speculative Jacobi Decoding (SJD), to accelerate auto-regressive text-to-image generation.

</br>


#### 016 [DART: Denoising Autoregressive Transformer for Scalable Text-to-Image Generation](https://arxiv.org/pdf/2410.08159)

**Arxiv 2025**

![img](res/T2I%20AR/016-1.png)

DART utilized a denoising autoregressive encoder, incorporating a dynamic adjustment mechanism into the generation process, thus improving the adaptability to complex text descriptions and increasing the diversity of generated outputs.

#### 001 [Deep unsupervised learning using nonequilibrium thermodynamics](https://proceedings.mlr.press/v37/sohl-dickstein15.pdf)

**ICML 2015**

Diffusion model前身

</br>


#### 002 [Denoising Diffusion Probabilistic Models](https://proceedings.neurips.cc/paper_files/paper/2020/file/4c5bcfec8584af0d967f1ab10179ca4b-Paper.pdf)

**NIPS 2020**

DDPM

</br>


#### 003 [GLIDE: Towards Photorealistic Image Generation and Editing with Text-Guided Diffusion Models](https://arxiv.org/pdf/2112.10741)

**ACMMM 2024**

The first work to explore T2I using DDPM. This study compared two different guidance strategies: CLIP guidance and classifier-free guidance. The latter achieved more realistic and detailed images. 

</br>


#### 004 [High-Resolution Image Synthesis With Latent Diffusion Models](https://openaccess.thecvf.com/content/CVPR2022/papers/Rombach_High-Resolution_Image_Synthesis_With_Latent_Diffusion_Models_CVPR_2022_paper.pdf)

**CVPR 2022**

![img](res/T2I%20Diffusion/004-1.png)

Latent Diffusion Model, Stable Diffusion

两个阶段, 第一阶段是VQGAN, 第二阶段是Diffusion

</br>


#### 005 [Emu: Enhancing Image Generation Models Using Photogenic Needles in a Haystack](https://arxiv.org/pdf/2309.15807)

**Arxiv 2023**

Emu used the latent diffusion architecture and proposed quality tuning method that effectively guided the pretrained model to generate visually appealing images while maintaining generality with respect to visual concepts. 

</br>


#### 006 [Vector Quantized Diffusion Model for Text-to-Image Synthesis](https://openaccess.thecvf.com/content/CVPR2022/papers/Gu_Vector_Quantized_Diffusion_Model_for_Text-to-Image_Synthesis_CVPR_2022_paper.pdf)

**CVPR 2022**

![img](res/T2I%20Diffusion/006-1.png)

VQ-Diffusion uses vector quantization technology for efficient generation.

</br>


#### 007 [Photorealistic Text-to-Image Diffusion Models with Deep Language Understanding](https://proceedings.neurips.cc/paper_files/paper/2022/file/ec795aeadae0b7d230fa35cbaf04c041-Paper-Conference.pdf)

**NIPS 2022**

![img](res/T2I%20Diffusion/007-1.png)

Imagen builds on the power of LLM in understanding text and hinges on the strength of diffusion models in high-fidelity image generation. It discovered that generic LLM (T5) are surprisingly effective at encoding text for image synthesis.  

</br>


### 008 [Hierarchical Text-Conditional Image Generation with CLIP Latents](https://3dvar.com/Ramesh2022Hierarchical.pdf)

**Arxiv 2022**

![img](res/T2I%20Diffusion/008-1.png)

DALL-E 2/unCLIP is a two-stage model: first, a prior model generates CLIP image embeddings based on text descriptions, and then a decoder generates images conditioned on these embeddings.  

</br>


### 009 [Blended Diffusion for Text-Driven Editing of Natural Images](https://openaccess.thecvf.com/content/CVPR2022/papers/Avrahami_Blended_Diffusion_for_Text-Driven_Editing_of_Natural_Images_CVPR_2022_paper.pdf)

**CVPR 2022**

![img](res/T2I%20Diffusion/009-1.png)

Blended Diffusion uses natural language guidance to generate realistic and diverse images. It proposed a language driven local region manipulation method.  

</br>


### 010 [PixArt-α: Fast Training of Diffusion Transformer for Photorealistic Text-to-Image Synthesis](https://arxiv.org/pdf/2310.00426)

**Arxiv 2023**

![img](res/T2I%20Diffusion/010-1.png)

PixArt-α used DiT architecture for text-to-image geneation.  

</br>


### 011 [SDXL: Improving Latent Diffusion Models for High-Resolution Image Synthesis](https://arxiv.org/pdf/2307.01952)

**Arxiv 2023**

![img](res/T2I%20Diffusion/011-1.png)

SDXL: Stable Diffusion + Refiner

</br>


### 012 [DreamBooth: Fine Tuning Text-to-Image Diffusion Models for Subject-Driven Generation](https://openaccess.thecvf.com/content/CVPR2023/papers/Ruiz_DreamBooth_Fine_Tuning_Text-to-Image_Diffusion_Models_for_Subject-Driven_Generation_CVPR_2023_paper.pdf)

**CVPR 2023**

![img](res/T2I%20Diffusion/012-1.png)

DreamBooth proposed a novel approach for 'personalization' of text-to-image diffusion models. It fine-tune a pretrained T2I model such that it learns to bind a unique identifier with specific subject given a few images of a subject.  

</br>


### 013 [Adding Conditional Control to Text-to-Image Diffusion Models](https://openaccess.thecvf.com/content/ICCV2023/papers/Zhang_Adding_Conditional_Control_to_Text-to-Image_Diffusion_Models_ICCV_2023_paper.pdf)

**ICCV 2023**

![img](res/T2I%20Diffusion/013-1.png)

ControlNet introduces additional control parameters into the generation process, enhancing flexibility.  

</br>


### 014 [Specialist Diffusion: Plug-and-Play Sample-Efficient Fine-Tuning of Text-to-Image Diffusion Models To Learn Any Unseen Style](https://openaccess.thecvf.com/content/CVPR2023/papers/Lu_Specialist_Diffusion_Plug-and-Play_Sample-Efficient_Fine-Tuning_of_Text-to-Image_Diffusion_Models_To_CVPR_2023_paper.pdf)

**CVPR 2023**

![img](res/T2I%20Diffusion/014-1.png)

In this paper, we aim to learn an unseen style by simply fine-tuning a pre-trained diffusion model with a handful of images (e.g., less than 10), so that the fine-tuned model can generate high-quality images of arbitrary objects in this style.

</br>


### 015 [One Transformer Fits All Distributions in Multi-Modal Diffusion at Scale](https://proceedings.mlr.press/v202/bao23a/bao23a.pdf)

**PMLR 2023**

![img](res/T2I%20Diffusion/015-1.png)

UniDiffuser integrates various generative capabilities based on a Transformer framework that accommodates multimodal data distributions, allowing it to process text-to-image, image-totext, and joint image-text tasks simultaneously.

</br>


### 016 [Multimodal Chain-of-Thought Reasoning in Language Models](https://arxiv.org/pdf/2411.16164#page=5.92)

**Arxiv 2023**

![img](res/T2I%20Diffusion/016-1.png)

MultimodalCoT uses a chain-of-thought mechanism to combine language (text) and visual (image) modalities in a twostage framework that separates inference generation from answer reasoning.

</br>


### 017 [Versatile Diffusion: Text, Images and Variations All in One Diffusion Model](https://openaccess.thecvf.com/content/ICCV2023/papers/Xu_Versatile_Diffusion_Text_Images_and_Variations_All_in_One_Diffusion_ICCV_2023_paper.pdf)

**ICCV 2023**

![img](res/T2I%20Diffusion/017-1.png)

Versatile Diffusion is the first unified multistream multimodal diffusion framework.

</br>


### 018 [Multi-Concept Customization of Text-to-Image Diffusion](https://openaccess.thecvf.com/content/CVPR2023/papers/Kumari_Multi-Concept_Customization_of_Text-to-Image_Diffusion_CVPR_2023_paper.pdf)

**CVPR 2023**

![img](res/T2I%20Diffusion/018-1.png)

SVDiff involves finetuning the singular values of weight matrices, creating a compact and efficient parameter space that reduces the risk of overfitting and language drift.

</br>


### 019 [ERNIE-ViLG 2.0: Improving Text-to-Image Diffusion Model With Knowledge-Enhanced Mixture-of-Denoising-Experts](https://openaccess.thecvf.com/content/CVPR2023/papers/Feng_ERNIE-ViLG_2.0_Improving_Text-to-Image_Diffusion_Model_With_Knowledge-Enhanced_Mixture-of-Denoising-Experts_CVPR_2023_paper.pdf#page=1.95)

**CVPR 2023**

![img](res/T2I%20Diffusion/019-1.png)

ERNIE-ViLG 2 is the first large T2I model in the Chinese language domain. (1) incorporating fine-grained textual and visual knowledge of key elements in the scene, and (2) utilizing different denoising experts at different denoising stages.

</br>


### 020 [Shifted Diffusion for Text-to-Image Generation](https://openaccess.thecvf.com/content/CVPR2023/papers/Zhou_Shifted_Diffusion_for_Text-to-Image_Generation_CVPR_2023_paper.pdf)

**CVPR 2023**

![img](res/T2I%20Diffusion/020-1.png)

Corgi trained the diffusion model to generate the image embeddings from text.

</br>


### 021 [Wuerstchen: An Efficient Architecture for Large-Scale Text-to-Image Diffusion Models](https://arxiv.org/pdf/2306.00637)

**Arxiv 2023**

![img](res/T2I%20Diffusion/021-1.png)

Wurstchen develops a latent diffusion technique that uses a detailed yet compact semantic image representation to guide the diffusion process.  

</br>


### 022 [Improving Diffusion-Based Image Synthesis with Context Prediction](https://proceedings.neurips.cc/paper_files/paper/2023/file/7664a7e946a84ac5e97649a967717cf2-Paper-Conference.pdf)

**NIPS 2023**

![img](res/T2I%20Diffusion/022-1.png)

ConPreDiff improves diffusion-based image synthesis through context prediction.

</br>


### 023 [Cross-Modal Contextualized Diffusion Models for Text-Guided Visual Generation and Editing](https://openreview.net/pdf?id=nFMS6wF2xq)

**ICLR 2024**

![img](res/T2I%20Diffusion/023-1.png)

ContextDiff incorporates the cross-modal context, including interactions and alignment between text conditions and visual samples, into both forward and backward diffusion processes.

</br>


### 024 [CogView3: Finer and Faster Text-to-Image Generation via Relay Diffusion](https://arxiv.org/pdf/2403.05121)

**ECCV 2024**

![img](res/T2I%20Diffusion/024-1.png)

CogView3 is the first model to implement relay diffusion in T2I.

</br>


### 025 [Scaling Rectified Flow Transformers for High-Resolution Image Synthesis](https://openreview.net/pdf?id=FPnUhsQJ5B)

**ICML 2024**

![img](res/T2I%20Diffusion/025-1.png)

Stable Diffusion 3 (SD3) introduces a new Transformer-based architecture for T2I that assigns different weights to text and image modalities, allowing bidirectional information flow between images and text annotations.

</br>


### 026 [Ranni: Taming Text-to-Image Diffusion for Accurate Instruction Following](https://openaccess.thecvf.com/content/CVPR2024/papers/Feng_Ranni_Taming_Text-to-Image_Diffusion_for_Accurate_Instruction_Following_CVPR_2024_paper.pdf)

**CVPR 2024**

![img](res/T2I%20Diffusion/026-1.png)

Ranni used LLM to create a panel of the coarse image content from text. And use the pannel to guide the generation of image.  

</br>


### 027 [Mastering Text-to-Image Diffusion: Recaptioning, Planning, and Generating with Multimodal LLMs](https://openreview.net/pdf?id=DgLFkAPwuZ)

**ICML 2024**

![img](res/T2I%20Diffusion/027-1.png)
![img](res/T2I%20Diffusion/027-2.png)

RPG uses a Multimodal Large Language Model (MLLM) as a global planner. It breaks down the process of generating complex images into simple generation tasks across multiple subregions, using complementary regional diffusion to achieve regionlevel combinatorial generation.  

</br>


### 028 [InstanceDiffusion: Instance-level Control for Image Generation](https://openaccess.thecvf.com/content/CVPR2024/papers/Wang_InstanceDiffusion_Instance-level_Control_for_Image_Generation_CVPR_2024_paper.pdf)

**CVPR 2024**

![img](res/T2I%20Diffusion/028-1.png)

InstanceDiffusion offered precise instance-level control for image generation through three changes: UniFusion Block, ScaleU Block. 

</br>


### 029 [Instruct-Imagen: Image Generation with Multi-modal Instruction](https://openaccess.thecvf.com/content/CVPR2024/papers/Hu_Instruct-Imagen_Image_Generation_with_Multi-modal_Instruction_CVPR_2024_paper.pdf)

**CVPR 2024**

![img](res/T2I%20Diffusion/029-1.png)
![img](res/T2I%20Diffusion/029-2.png)

Instruct-Imagen firstly proposed the task of multi-modal instrcution for image generation. It fine-tune Imagen model for multi-modal instruction guided image generation.  

</br>


### 030 [ElasticDiffusion: Training-free Arbitrary Size Image Generation through Global-Local Content Separation](https://openaccess.thecvf.com/content/CVPR2024/papers/Haji-Ali_ElasticDiffusion_Training-free_Arbitrary_Size_Image_Generation_through_Global-Local_Content_Separation_CVPR_2024_paper.pdf)

**CVPR 2024**

![img](res/T2I%20Diffusion/030-1.png)

ElasticDiffusion a novel training-free decoding method that enables pretrained text-to-image diffusion models to generate images with various sizes. ElasticDiffusion attempts to decouple the generation trajectory of a pretrained model into local and global signals.

</br>


### 031 [PIXART-δ: Fast and Controllable Image Generation with Latent Consistency Models](https://arxiv.org/pdf/2401.05252)

**Arxiv 2024**

![img](res/T2I%20Diffusion/031-1.png)
![img](res/T2I%20Diffusion/031-2.png)

PIXART-δ significantly accelerates inference speed through the integration of LCM, enabling high-quality image generation in just 2-4 steps. It also introduces an innovative ControlNetTransformer architecture specifically designed for transformers, providing explicit controllability and high-quality image generation.

</br>


### 032 [PixArt-Σ: Weak-to-Strong Training of Diffusion Transformer for 4K Text-to-Image Generation](https://arxiv.org/pdf/2403.04692)

**ECCV 2024**

![img](res/T2I%20Diffusion/032-1.png)

PixArt-Σ offers significantly higher image fidelity and better alignment with text prompts.  

</br>


### 033 [Fast High-Resolution Image Synthesis with Latent Adversarial Diffusion Distillation](https://dl.acm.org/doi/pdf/10.1145/3680528.3687625)

**SIGGRAPH Asia 2024**

![img](res/T2I%20Diffusion/033-1.png)

SD3-Turbo introduced Latent Adversarial Diffusion Distillation (LADD), a novel distillation method that overcomes the limitations of Adversarial Diffusion Distillation (ADD).

</br>


### 034 [SemanticDraw: Towards Real-Time Interactive Content Creation from Image Diffusion Models](https://arxiv.org/pdf/2403.09055)

**Arxiv 2024**

![img](res/T2I%20Diffusion/034-1.png)

StreamMultiDiffusion is the first real-time region-based T2I generation framework.  

</br>


### 035 [OmniGen: Unified Image Generation](https://arxiv.org/pdf/2409.11340)

**Arxiv 2024**

![img](res/T2I%20Diffusion/035-1.png)
![img](res/T2I%20Diffusion/035-2.png)

OmniGen presents a new type of diffusion model for unified image generation

</br>


### 036 [Hunyuan-DiT: A Powerful Multi-Resolution Diffusion Transformer with Fine-Grained Chinese Understanding](https://arxiv.org/pdf/2405.08748)

**Arxiv 2024**

![img](res/T2I%20Diffusion/036-1.png)
![img](res/T2I%20Diffusion/036-2.png)

Hunyuan-DiT, a text-to-image diffusion transformer with fine-grained understanding of both English and Chinese

</br>


#### 037 [DragDiffusion: Harnessing Diffusion Models for Interactive Point-based Image Editing](https://openaccess.thecvf.com/content/CVPR2024/papers/Shi_DragDiffusion_Harnessing_Diffusion_Models_for_Interactive_Point-based_Image_Editing_CVPR_2024_paper.pdf)

**CVPR 2024**

![img](res/T2I%20Diffusion/037-1.png)

DragDiffusion optimizes only the latent variables for a single time step, achieving efficient and precise spatial control, which significantly enhances the applicability of interactive pointbased editing for both real and diffusion-generated images.

</br>


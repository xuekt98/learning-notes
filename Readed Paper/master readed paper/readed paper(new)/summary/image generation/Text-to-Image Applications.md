# Text-to-Image Applications

## Part 1 Personalization

#### 1-001 [An Image is Worth One Word: Personalizing Text-to-Image Generation using Textual Inversion](https://arxiv.org/pdf/2208.01618)

**ICLR 2023**

![img](res/T2I%20Applications/1-001-1.png)

Texutal Inversion used one specified symbol to represent the given image and optimize the representation of this symbol for a given group of image, so that the symbol can represent the specified content of the given image.  

</br>


#### 1-002 [PIA: Your Personalized Image Animator via Plug-and-Play Modules in Text-to-Image Models](https://openaccess.thecvf.com/content/CVPR2024/papers/Zhang_PIA_Your_Personalized_Image_Animator_via_Plug-and-Play_Modules_in_Text-to-Image_CVPR_2024_paper.pdf)

**CVPR 2024**

![img](res/T2I%20Applications/1-002-1.png)

PIA a Personalized Image Animator that excels in aligning with condition images achieving motion controllability by text and the compatibility with various personalized T2I models without specific tuning. 

</br>


#### 1-003 [Prompt-Free Diffusion: Taking "Text" out of Text-to-Image Diffusion Models](https://openaccess.thecvf.com/content/CVPR2024/papers/Xu_Prompt-Free_Diffusion_Taking_Text_out_of_Text-to-Image_Diffusion_Models_CVPR_2024_paper.pdf)

**CVPR 2024**

![img](res/T2I%20Applications/1-003-1.png)
![img](res/T2I%20Applications/1-003-2.png)

Prompt-Free Diffusion improves image generation quality by eliminating the need for prompts, thereby simplifying the personalized generation process.

</br>


#### 1-004 [PALP: Prompt Aligned Personalization of Text-to-Image Models](https://dl.acm.org/doi/pdf/10.1145/3680528.3687604)

**SIGGRAPH Asia 2024**

![img](res/T2I%20Applications/1-004-1.png)
![img](res/T2I%20Applications/1-004-2.png)

PALP maintains consistency between text and generated images, even under complex prompting conditions, demonstrating excellent performance.

</br>


#### 1-005 [PhotoMaker: Customizing Realistic Human Photos via Stacked ID Embedding](https://openaccess.thecvf.com/content/CVPR2024/papers/Li_PhotoMaker_Customizing_Realistic_Human_Photos_via_Stacked_ID_Embedding_CVPR_2024_paper.pdf)

**CVPR 2024**

![img](res/T2I%20Applications/1-005-1.png)
![img](res/T2I%20Applications/1-005-2.png)

PhotoMaker efficiently encodes the input ID images using stacked ID embeddings, ensuring the retention of identity information.  

</br>


#### 1-006 [Learning Disentangled Identifiers for Action-Customized Text-to-Image Generation](https://openaccess.thecvf.com/content/CVPR2024/papers/Huang_Learning_Disentangled_Identifiers_for_Action-Customized_Text-to-Image_Generation_CVPR_2024_paper.pdf)

**CVPR 2024**

![img](res/T2I%20Applications/1-006-1.png)
![img](res/T2I%20Applications/1-006-2.png)

ADI introduces disentangled identifiers, which enable the generation of new images with shared actions through specific symbols, enhancing the diversity of output.

</br>


#### 1-007 [DreamTuner: Single Image is Enough for Subject-Driven Generation](https://arxiv.org/pdf/2312.13691)

**Arxiv 2023**

![img](res/T2I%20Applications/1-007-1.png)
![img](res/T2I%20Applications/1-007-2.png)

DreamTurner achieves theme-driven image generation through a theme encoder, allowing for more detailed preservation of subject identity.

</br>


#### 1-008 [ELITE: Encoding Visual Concepts into Textual Embeddings for Customized Text-to-Image Generation](https://openaccess.thecvf.com/content/ICCV2023/papers/Wei_ELITE_Encoding_Visual_Concepts_into_Textual_Embeddings_for_Customized_Text-to-Image_ICCV_2023_paper.pdf)

**ICCV 2023**

![img](res/T2I%20Applications/1-008-1.png)
![img](res/T2I%20Applications/1-008-2.png)

ELITE introduces a combination of global and local mapping networks to enable fast and accurate customized generation.

</br>


#### 1-009 [Tailored Visions: Enhancing Text-to-Image Generation with Personalized Prompt Rewriting](https://openaccess.thecvf.com/content/CVPR2024/papers/Chen_Tailored_Visions_Enhancing_Text-to-Image_Generation_with_Personalized_Prompt_Rewriting_CVPR_2024_paper.pdf)

**CVPR 2024**

![img](res/T2I%20Applications/1-009-1.png)
![img](res/T2I%20Applications/1-009-2.png)

Tailored Visions enhances personalization by rewriting user prompts based on historical interactions.

</br>


#### 1-010 [LayoutDiffusion: Controllable Diffusion Model for Layout-to-Image Generation](https://openaccess.thecvf.com/content/CVPR2023/papers/Zheng_LayoutDiffusion_Controllable_Diffusion_Model_for_Layout-to-Image_Generation_CVPR_2023_paper.pdf)

**CVPR 2023**

![img](res/T2I%20Applications/1-010-1.png)
![img](res/T2I%20Applications/1-010-2.png)

Layout Diffusion proposed to construct a structural image patch with region information and transform the patched image into a special layout ot fuse with the normal layout in a unified form. It also proposed a novel Layout Fusion Module(LFM) and Object-aware Cross Attention. 

</br>


#### 1-011 [HyperDreamBooth: HyperNetworks for Fast Personalization of Text-to-Image Models](https://openaccess.thecvf.com/content/CVPR2024/papers/Ruiz_HyperDreamBooth_HyperNetworks_for_Fast_Personalization_of_Text-to-Image_Models_CVPR_2024_paper.pdf)

**CVPR 2024**

![img](res/T2I%20Applications/1-011-1.png)
![img](res/T2I%20Applications/1-011-2.png)
![img](res/T2I%20Applications/1-011-3.png)

HyperDreamBooth uses a hypernetwork to generate personalized weights from a single image, allowing for efficient style and context switching.  

</br>


#### 1-012 [Improving Subject-Driven Image Synthesis with Subject-Agnostic Guidance](https://openaccess.thecvf.com/content/CVPR2024/papers/Chan_Improving_Subject-Driven_Image_Synthesis_with_Subject-Agnostic_Guidance_CVPR_2024_paper.pdf)

**CVPR 2024**

![img](res/T2I%20Applications/1-012-1.png)
![img](res/T2I%20Applications/1-012-2.png)

SAG employed dual classifier-free guidance to ensure that generated outputs align with both themes and input text prompts, enhancing generation accuracy

</br>


#### 1-013 [Personalized Residuals for Concept-Driven Text-to-Image Generation](https://openaccess.thecvf.com/content/CVPR2024/papers/Ham_Personalized_Residuals_for_Concept-Driven_Text-to-Image_Generation_CVPR_2024_paper.pdf)

**CVPR 2024**

![img](res/T2I%20Applications/1-013-1.png)
![img](res/T2I%20Applications/1-013-2.png)

Personalized Residuals freezed the weights of a pretrained text-conditional diffusion model and learned low-rank residuals for a small subset of the model's layers. The residual-based approach then directly enables application of our proposed sampling technique, which applies the learned residuals only in areas where the concept is localized via cross-attention and applies the original diffusion weights in all other regions.  

</br>


#### 1-014 [FastComposer: Tuning-Free Multi-subject Image Generation with Localized Attention](https://link.springer.com/content/pdf/10.1007/s11263-024-02227-z.pdf)

**IJCV 2024**

![img](res/T2I%20Applications/1-014-1.png)
![img](res/T2I%20Applications/1-014-2.png)
![img](res/T2I%20Applications/1-014-3.png)

FastComposer is a multi-theme generation method that does not require fine-tuning, using an image encoder to extract theme embeddings for efficient personalized generation.  

</br>


#### 1-015 [InstantID: Zero-shot Identity-Preserving Generation in Seconds](https://arxiv.org/pdf/2401.07519)

**Arxiv 2024**

![img](res/T2I%20Applications/1-015-1.png)
![img](res/T2I%20Applications/1-015-2.png)

InstantID proposed a plug-and-play module adeptly handles image personalization in various styles using just a single facial image, while ensuring high fidelity. It designed a novel IdentityNet by imposing strong semantic and weak spatial conditions, integrating facial and landmark images with textual prompts to steer the image generation.  

</br>


#### 1-016 [Specialist Diffusion: Plug-and-Play Sample-Efficient Fine-Tuning of Text-to-Image Diffusion Models To Learn Any Unseen Style](https://openaccess.thecvf.com/content/CVPR2023/papers/Lu_Specialist_Diffusion_Plug-and-Play_Sample-Efficient_Fine-Tuning_of_Text-to-Image_Diffusion_Models_To_CVPR_2023_paper.pdf)

**CVPR 2023**

Specialist Diffusion can be seamlessly integrated into existing models, learning complex styles and demonstrating efficient tuning capabilities with high-quality samples.

</br>


#### 1-017 [ControlStyle: Text-Driven Stylized Image Generation Using Diffusion Priors](https://dl.acm.org/doi/pdf/10.1145/3581783.3612524)

**ACM MM 2023**

![img](res/T2I%20Applications/1-017-1.png)
![img](res/T2I%20Applications/1-017-2.png)

ControlStyle focused on text-driven stylized image generation. It proposed a new diffusion model (ControlStyle) via upgrading a pre-trained textto-image model with a trainable modulation network enabling more conditions of text prompts and style images.

</br>


#### 1-018 [UniPortrait: A Unified Framework for Identity-Preserving Single- and Multi-Human Image Personalization](https://arxiv.org/pdf/2408.05939)

**Arxiv 2024**

![img](res/T2I%20Applications/1-018-1.png)
![img](res/T2I%20Applications/1-018-2.png)

UniPortrait offers a unified framework for portrait image personalization, supporting customization for both single and multiple identities.

</br>


#### 1-019 [High-fidelity Person-centric Subject-to-Image Synthesis](https://openaccess.thecvf.com/content/CVPR2024/papers/Wang_High-fidelity_Person-centric_Subject-to-Image_Synthesis_CVPR_2024_paper.pdf)

**CVPR 2024**

![img](res/T2I%20Applications/1-019-1.png)
![img](res/T2I%20Applications/1-019-2.png)

Face-Diffuser generates high-fidelity images by jointly learning scenes and characters, using a saliency-adaptive noise fusion mechanism to improve image quality.


#### 1-020 [Tuning-Free Image Customization with Image and Text Guidance](https://arxiv.org/pdf/2403.12658v1)

**ECCV 2024**

![img](res/T2I%20Applications/1-020-1.png)
![img](res/T2I%20Applications/1-020-2.png)

TIGC introduces a non-tuning image customization framework that modifies detailed attributes based on text descriptions while preserving key subject features.

</br>


#### 1-021 [Decoupled Textual Embeddings for Customized Image Generation](https://arxiv.org/pdf/2312.11826)

**AAAI 2024**

![img](res/T2I%20Applications/1-021-1.png)
![img](res/T2I%20Applications/1-021-2.png)

DETEX learns the disentangled concept embedding for flexible customized text-to-image genration.  

</br>


#### 1-022 [FlashFace: Human Image Personalization with High-fidelity Identity Preservation](https://arxiv.org/pdf/2403.17008)

**Arxiv 2024**

![img](res/T2I%20Applications/1-022-1.png)
![img](res/T2I%20Applications/1-022-2.png)

FlashFace improves identity retention accuracy by encoding facial identity through feature maps.  

</br>


#### 1-023 [IDAdapter: Learning Mixed Features for Tuning-Free Personalization of Text-to-Image Models](https://openaccess.thecvf.com/content/CVPR2024W/FAS2024/papers/Cui_IDAdapter_Learning_Mixed_Features_for_Tuning-Free_Personalization_of_Text-to-Image_Models_CVPRW_2024_paper.pdf)

**CVPR 2024**

![img](res/T2I%20Applications/1-023-1.png)
![img](res/T2I%20Applications/1-023-2.png)

IDAdapter and enhance generation diversity and text alignment accuracy using non-tuning methods and contextual regularization techniques, respectively.

</br>


#### 1-024 [Imagine yourself: Tuning-Free Personalized Image Generation](https://arxiv.org/pdf/2409.13346)

**Arxiv 2024**

![img](res/T2I%20Applications/1-024-1.png)
![img](res/T2I%20Applications/1-024-2.png)
![img](res/T2I%20Applications/1-024-3.png)

Imagine Yourself represents an advanced model that requires no fine-tuning, pushing the boundaries of personalized image generation through a novel synthesis pairing mechanism and parallel attention architecture.

</br>




# Controllable T2I Generation

#### 2-001 [Uni-ControlNet: All-in-One Control to Text-to-Image Diffusion Models](https://proceedings.neurips.cc/paper_files/paper/2023/file/2468f84a13ff8bb6767a67518fb596eb-Paper-Conference.pdf)

**NIPS 2023**

![img](res/T2I%20Applications/2-001-1.png)

Uni-ControlNet offers a unified framework that simultaneously utilizes local controls (such as edge maps, depth maps, and segmentation masks) and global controls (such as CLIP image embeddings), significantly reducing the cost of training from scratch.

</br>


#### 2-002 [T2I-Adapter: Learning Adapters to Dig out More Controllable Ability for Text-to-Image Diffusion Models](https://arxiv.org/pdf/2302.08453)

**AAAI 2024**

![img](res/T2I%20Applications/2-002-1.png)

T2IAdapter acts as a pluggable module, enhancing the control capabilities of T2I models by injecting additional conditional information, including text descriptions, image templates, and keypoints, into the generation process.

</br>


#### 2-003 [Multi-Concept Customization of Text-to-Image Diffusion](https://openaccess.thecvf.com/content/CVPR2023/papers/Kumari_Multi-Concept_Customization_of_Text-to-Image_Diffusion_CVPR_2023_paper.pdf)

**CVPR 2023**

![img](res/T2I%20Applications/2-003-1.png)
![img](res/T2I%20Applications/2-003-2.png)

Custom Diffusion achieves rapid model adjustments to represent new concepts by optimizing a minimal number of parameters, with the ability to train multiple concepts concurrently.  

</br>


#### 2-004 [JeDi: Joint-Image Diffusion Models for Finetuning-Free Personalized Text-to-Image Generation](https://openaccess.thecvf.com/content/CVPR2024/papers/Zeng_JeDi_Joint-Image_Diffusion_Models_for_Finetuning-Free_Personalized_Text-to-Image_Generation_CVPR_2024_paper.pdf)

**CVPR 2024**

![img](res/T2I%20Applications/2-004-1.png)
![img](res/T2I%20Applications/2-004-2.png)

Jedi generates personalized images based on an arbitrary number of reference images, constructing a synthetic dataset of related images to learn the shared distribution of multiple text-image pairs.

</br>


#### 2-005 [ViCo: Plug-and-play Visual Condition for Personalized Text-to-image Generation](https://arxiv.org/pdf/2306.00971)

**Arxiv 2023**

![img](res/T2I%20Applications/2-005-1.png)

ViCo provides a fast and lightweight solution for personalized generation, supporting plug-and-play features that avoid fine-tuning the original diffusion model while preserving the details of newly generated concepts.  

</br>


#### 2-006 [ReCo: Region-Controlled Text-to-Image Generation](https://openaccess.thecvf.com/content/CVPR2023/papers/Yang_ReCo_Region-Controlled_Text-to-Image_Generation_CVPR_2023_paper.pdf)

**CVPR 2023**

![img](res/T2I%20Applications/2-006-1.png)

ReCo allows users to control arbitrary objects using open text by adding location markers and natural language region descriptions.

</br>


#### 2-007 [SpaText: Spatio-Textual Representation for Controllable Image Generation](https://openaccess.thecvf.com/content/CVPR2023/papers/Avrahami_SpaText_Spatio-Textual_Representation_for_Controllable_Image_Generation_CVPR_2023_paper.pdf)

**CVPR 2023**

![img](res/T2I%20Applications/2-007-1.png)
![img](res/T2I%20Applications/2-007-2.png)

SpaText employs open-vocabulary scene control, combining global text prompts and segmentation maps to generate high-fidelity images.

</br>


#### 2-008 [BLIP-Diffusion: Pre-trained Subject Representation for Controllable Text-to-Image Generation and Editing](https://proceedings.neurips.cc/paper_files/paper/2023/file/602e1a5de9c47df34cae39353a7f5bb1-Paper-Conference.pdf)

**NIPS 2023**

![img](res/T2I%20Applications/2-008-1.png)
![img](res/T2I%20Applications/2-008-2.png)

BLIP-Diffusion introduces a new multimodal encoder pretrained in BLIP-2 to achieve improved controllable generation.

</br>


#### 2-009 [Zero-Painter: Training-Free Layout Control for Text-to-Image Synthesis](https://openaccess.thecvf.com/content/CVPR2024/papers/Ohanyan_Zero-Painter_Training-Free_Layout_Control_for_Text-to-Image_Synthesis_CVPR_2024_paper.pdf)

**CVPR 2024**

![img](res/T2I%20Applications/2-009-1.png)
![img](res/T2I%20Applications/2-009-2.png)

Zero-Painter is an innovative training-free framework that generates images based on text layout conditions.

</br>


#### 2-010 [FreeControl: Training-Free Spatial Control of Any Text-to-Image Diffusion Model with Any Condition](https://openaccess.thecvf.com/content/CVPR2024/papers/Mo_FreeControl_Training-Free_Spatial_Control_of_Any_Text-to-Image_Diffusion_Model_with_CVPR_2024_paper.pdf)

**CVPR 2024**

![img](res/T2I%20Applications/2-010-1.png)
![img](res/T2I%20Applications/2-010-2.png)

FreeControl serves as a general-purpose zerotraining solution supporting controllable generation across different conditions and architectures.

</br>


#### 2-011 [MultiDiffusion: Fusing Diffusion Paths for Controlled Image Generation](https://openreview.net/pdf?id=D4ajVWmgLB)

**ICML 2023**

![img](res/T2I%20Applications/2-011-1.png)
![img](res/T2I%20Applications/2-011-2.png)

MultiDiffusion provides a unified framework that leverages pretrained T2I diffusion models to achieve diverseand controllable image generation without requiring further training or fine-tuning. 

</br>



# Text-guided Image Generation

#### 3-001 [Imagic: Text-Based Real Image Editing with Diffusion Models](https://openaccess.thecvf.com/content/CVPR2023/papers/Kawar_Imagic_Text-Based_Real_Image_Editing_With_Diffusion_Models_CVPR_2023_paper.pdf)

**CVPR 2023**

![img](res/T2I%20Applications/3-001-1.png)
![img](res/T2I%20Applications/3-001-2.png)

Imagic as the first method aimed at semantic editing of a single image through text, significantly improves the precision of image editing by optimizing text embeddings and finetuning pretrained diffusion models, establishing itself as a benchmark in the field.  

</br>


#### 3-002 [Attention Calibration for Disentangled Text-to-Image Personalization](https://openaccess.thecvf.com/content/CVPR2024/papers/Zhang_Attention_Calibration_for_Disentangled_Text-to-Image_Personalization_CVPR_2024_paper.pdf)

**CVPR 2024**

![img](res/T2I%20Applications/3-002-1.png)

DisenDiff, on the contrary, uses a cross-attention mechanism to disentangle multiple concepts within a single image, allowing users to describe different elements independently, thus increasing the flexibility of image generation. 

</br>


#### 3-003 [Noise Map Guidance: Inversion with Spatial Context for Real Image Editing](https://arxiv.org/pdf/2402.04625)

**ICLR 2024**

![img](res/T2I%20Applications/3-003-1.png)

Noise Map Guidance (NMG) provides a contextrich inversion approach for editing real images, enhancing the naturalness of the editing results.

</br>


#### 3-004 [SINE: SINgle Image Editing With Text-to-Image Diffusion Models](https://openaccess.thecvf.com/content/CVPR2023/papers/Zhang_SINE_SINgle_Image_Editing_With_Text-to-Image_Diffusion_Models_CVPR_2023_paper.pdf#page=5.95)

**CVPR 2023**

![img](res/T2I%20Applications/3-004-1.png)

SINE introduced a novel classifier-free guiding model that facilitates the extraction of knowledge from a single image for application to pretrained diffusion models, enabling effective content creation from a single image.  

</br>


#### 3-005 [AdapEdit: Spatio-Temporal Guided Adaptive Editing Algorithm for Text-Based Continuity-Sensitive Image Editing](https://arxiv.org/pdf/2312.08019)

**AAAI 2024**

![img](res/T2I%20Applications/3-005-1.png)

AdapEdit addresses complex, continuity-sensitive image editing tasks by employing variable spatiotemporal guiding scales, which enhance the naturalness and contextual consistency of edits.

</br>


#### 3-006 [Accelerating Text-to-Image Editing via Cache-Enabled Sparse Diffusion Inference](https://arxiv.org/pdf/2305.17423)

**AAAI 2024**

![img](res/T2I%20Applications/3-006-1.png)

FISEdit integrates cachesupported sparse diffusion model inference, allowing users to perform efficient image editing through minor text modifications, thus reducing inference time.

</br>


#### 
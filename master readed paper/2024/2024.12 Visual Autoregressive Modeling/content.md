# 文章阅读记录

* [<font size=3>**Template**</font>](template)  
<font color=orange>**Origin:**</font>**[[Project Code](https://github.com/SooLab/Free-Bloom)]**  
<font color=orange>**Authors:**</font>  
<font color=orange>**Label:**</font>  
<font color=orange>**Abastract:**</font>  

</br>


[<back to top\>](#文章阅读记录)
# Visual Autoregressive Modeling

## Highly Relevant

* [<font size=3>**001($\bigstar\bigstar\bigstar$) Visual Autoregressive Modeling: Scalable Image Generation via Next-Scale Prediction**</font>](2024.12.04-2024.12.11/001%20Visual%20Autoregressive%20Modeling.md)  
<font color=orange>**Origin:**</font> NIPS2024; Peking University; Bytedance **[[Project Code](https://github.com/FoundationVision/VAR)]**  
<font color=orange>**Authors:**</font> Keyu Tian, Yi Jiang, Zehuan Yuan; etc.  
<font color=orange>**Label:**</font> Image Generation; Autoregressive Models;    
<font color=orange>**Abastract:**</font> Using multi-scale VQGAN codebook to generate image with autoregressive model. Next-scale prediction.    


* [<font size=3>**005($\bigstar\bigstar\bigstar$) CONTROLVAR: EXPLORING CONTROLLABLE VISUAL AUTOREGRESSIVE MODELING**</font>](2024.12.04-2024.12.11/004%20Alleviating%20Distortion%20in%20Image%20Generation.md)  
<font color=orange>**Origin:**</font> Arxiv 2024.10; Carnegie Mellon University; Adobe Research; **[[Project Code](https://github.com/lxa9867/ControlVAR)]**  
<font color=orange>**Authors:**</font> Xiang Li, Kai Qiu, Hao Chen; etc.  
<font color=orange>**Label:**</font> VAR; Controllable Generation  
<font color=orange>**Abastract:**</font> ControlVAR jointly models the distribution of image and pixel-level conditions during training and imposes conditional controls during testing. To enhance the joint modeling, we adopt the next-scale AR prediction paradigm and unify control and image representations. A teacher-forcing guidance strategy is proposed to further facilitate controllable generation with joint modeling.


* [<font size=3>**008($\bigstar\bigstar\bigstar$) VAR-CLIP: Text-to-Image Generator with Visual Auto-Regressive Modeling**</font>](2024.12.04-2024.12.11/008%20VAR-CLIP.md)  
<font color=orange>**Origin:**</font> Arxiv 2024.08; Shanghai Jiaotong University **[[Project Code](https://github.com/daixiangzi/VAR-CLIP)]**  
<font color=orange>**Authors:**</font> Qian Zhang; Xiangzi Dai; Ninghua Yang; etc.  
<font color=orange>**Label:**</font> CLIP, VAR, Autoregressive Image Generation;  
<font color=orange>**Abastract:**</font> The VAR-CLIP framework encodes captions into text embeddings, which are then utilized as textual conditions for image generation. To facilitate training on extensive datasets, such as ImageNet, we have constructed a substantial image-text dataset leveraging BLIP2.


* [<font size=3>**012($\bigstar\bigstar\bigstar$) G3PT: Unleash the power of Autoregressive Modeling in 3D Generation via Cross-scale Querying Transformer**</font>](2024.12.04-2024.12.11/012%20G3PT%20Unleash%20the%20power%20of%20Autoregressive%20Modeling%20in%203D%20Generation.md)  
<font color=orange>**Origin:**</font> Arxiv 2024.09; Alibaba Inc **[[No Code]()]**  
<font color=orange>**Authors:**</font> Jinzhi Zhang; Feng Xiong; Mu Xu    
<font color=orange>**Label:**</font> 3D Generation; Autoregressive Modeling; Cross-scale;  
<font color=orange>**Abastract:**</font> we introduce G3PT, a scalable coarse-to-fine 3D generative model utilizing a crossscale querying transformer. The key is to map point-based 3D data into discrete tokens with different levels of detail, naturally establishing a sequential relationship between different levels suitable for autoregressive modeling. Additionally, the cross-scale querying transformer connects tokens globally across different levels of detail without requiring an ordered sequence


* [<font size=3>**015($\bigstar\bigstar\bigstar$) DepthART: Monocular Depth Estimation as Autoregressive Refinement Task**</font>](2024.12.04-2024.12.11/015%20DepthART%20Monocular%20Depth%20Estimation%20as%20Autoregressive%20Refinement%20Task.md)  
<font color=orange>**Origin:**</font> Arxiv 2024.10; AIRI, Moscow, Russia **[[Project Code](https://bulatko.github.io/depthart-pp/)]**  
<font color=orange>**Authors:**</font> Bulat Gabdullin; Nina Konovalova; etc.  
<font color=orange>**Label:**</font> Monocular Depth Estimation; VAR  
<font color=orange>**Abastract:**</font> Unlike the original VAR training procedure, which employs static targets, our method utilizes a dynamic target formulation that enables model self-refinement and incorporates multi-modal guidance during training. Specifically, we use model predictions as inputs instead of ground truth token maps during training, framing the objective as residual minimization.


* [<font size=3>**016($\bigstar\bigstar\bigstar$) MaskBit: Embedding-free Image Generation via Bit Tokens**</font>](2024.12.04-2024.12.11/016%20MaskBIT.md)  
<font color=orange>**Origin:**</font> Arxiv 2024.09; ByteDance **[[Project Code](https://weber-mark.github.io/projects/maskbit.html)]**  
<font color=orange>**Authors:**</font> Mark Weber; etc.    
<font color=orange>**Label:**</font> VQGAN; Transformer;  
<font color=orange>**Abastract:**</font> Firstly, an empirical and systematic examination of VQGANs, leading to a modernized VQGAN. Secondly, a novel embedding-free generation network operating directly on bit tokens – a binary quantized representation of tokens with rich semantics.


* [<font size=3>**017($\bigstar\bigstar\bigstar$) CONTROLAR: CONTROLLABLE IMAGE GENERATION WITH AUTOREGRESSIVE MODELS**</font>](2024.12.04-2024.12.11/017%20ControlAR.md)  
<font color=orange>**Origin:**</font> Arxiv 2024.10; Huazhong University of Science and Technology; The University of Hong Kong **[[Project Code](https://weber-mark.github.io/projects/maskbit.html)]**  
<font color=orange>**Authors:**</font> Zongming Li, Tianheng Cheng; etc.    
<font color=orange>**Label:**</font> AR; Control;  
<font color=orange>**Abastract:**</font> Firstly, we explore control encoding for AR models and propose a lightweight control encoder to transform spatial inputs (e.g., canny edges or depth maps) into control tokens. Then ControlAR exploits the conditional decoding method to generate the next image token conditioned on the per-token fusion between control and image tokens, similar to positional encodings. Compared to prefilling tokens, using conditional decoding significantly strengthens the control capability of AR models but also maintains the model efficiency


* [<font size=3>**018($\bigstar\bigstar\bigstar$) Loong: Generating Minute-level Long Videos with Autoregressive Language Models**</font>](2024.12.04-2024.12.11/018%20Loong.md)  
<font color=orange>**Origin:**</font> CoRR 2024; The University of Hong Kong; ByteDance **[[Project Code](https://epiphqny.github.io/Loong-video)]**   
<font color=orange>**Authors:**</font> Yuqing Wang; Tianwei Xiong; etc.    
<font color=orange>**Label:**</font> AR; Video Generation;  
<font color=orange>**Abastract:**</font> we model the text tokens and video tokens as a unified sequence for autoregressive LLMs and train the model from scratch. We propose progressive short-to-long training with a loss re-weighting scheme to mitigate the loss imbalance problem for long video training. We further investigate inference strategies, including video token re-encoding and sampling strategies, to diminish error accumulation during inference.


* [<font size=3>**019($\bigstar\bigstar\bigstar$) OCCVAR: SCALABLE 4D OCCUPANCY WORLD MODEL VIA NEXT-SCALE PREDICTION**</font>](2024.12.04-2024.12.11/019%20OCCVAR.md)  
<font color=orange>**Origin:**</font> The University of Hong Kong; ByteDance **[[No Code]()]**   
<font color=orange>**Authors:**</font> Anonymous      
<font color=orange>**Label:**</font> Occupancy; VAR;  
<font color=orange>**Abastract:**</font> we propose a spatial-temporal transformer via temporal next-scale prediction, aiming at predicting the 4D occupancy scenes from coarse to fine scales.


* [<font size=3>**020($\bigstar\bigstar\bigstar$) HART: EFFICIENT VISUAL GENERATION WITH HYBRID AUTOREGRESSIVE TRANSFORMER**</font>](2024.12.04-2024.12.11/020%20HART.md)  
<font color=orange>**Origin:**</font> **[[No Code]()]**   
<font color=orange>**Authors:**</font> Anonymous      
<font color=orange>**Label:**</font> VAR, Autoregressive;  
<font color=orange>**Abastract:**</font> we present the hybrid tokenizer, which decomposes the continuous latents from the autoencoder into two components: discrete tokens representing the big picture and continuous tokens representing the residual components that cannot be represented by the discrete tokens.


* [<font size=3>**021($\bigstar\bigstar\bigstar$) INJECTING VISION LANGUAGE INTO AUTOREGRESSIVE IMAGE GENERATION**</font>](2024.12.04-2024.12.11/021%20Injecting%20Visual.md)  
<font color=orange>**Origin:**</font> **[[No Code]()]**   
<font color=orange>**Authors:**</font> Anonymous      
<font color=orange>**Label:**</font> VAR, Autoregressive;  
<font color=orange>**Abastract:**</font> with only a few newly introduced parameters and minimal training, a pre-trained AR generation model can successfully accommodate both text and image conditions and produce visually appealing results. To manage the relationship between textual and visual inputs, we reinforce InjectAR with a hierarchical attention mechanism, which subdivides the attention scores for textual tokens into their corresponding visual components, preventing either modality from dominating the output.


* [<font size=3>**022($\bigstar\bigstar\bigstar$) CAR: Controllable Autoregressive Modeling for Visual Generation**</font>](2024.12.04-2024.12.11/022%20Car.md)  
<font color=orange>**Origin:**</font> **[[No Code]()]**   
<font color=orange>**Authors:**</font> Anonymous      
<font color=orange>**Label:**</font> VAR, Autoregressive;  
<font color=orange>**Abastract:**</font> Controllable AutoRegressive Modeling (CAR), a novel, plug-and-play framework that integrates conditional control into multi-scale latent variable modeling, enabling efficient control generation within a pre-trained visual autoregressive model. CAR progressively refines and captures control representations, which are injected into each autoregressive step of the pre-trained model to guide the generation process.

</br>


[<back to top\>](#文章阅读记录)
## Others


* [<font size=3>**002 Autoregressive Model Beats Diffusion: Llama for Scalable Image Generation**</font>](2024.12.04-2024.12.11/002%20Autoregressive%20Model%20Beats%20Diffusion.md)  
<font color=orange>**Origin:**</font> Arxiv 2024.06; The University of Hong Kong; Bytedance **[[Project Code](https://github.com/FoundationVision/LlamaGen)]**  
<font color=orange>**Authors:**</font> Peize Sun; Yi Jiang; Shoufa Chen; etc.  
<font color=orange>**Label:**</font> Image Generation; LlamaGen;  
<font color=orange>**Abastract:**</font> Using Llama structure to generate image, next-token prediction  


* [<font size=3>**003 OmniTokenizer: A Joint Image-Video Tokenizer for Visual Generation**</font>](2024.12.04-2024.12.11/003%20OmniTokenizer%20A%20Joint%20Image-Video%20Tokenizer%20for%20Visual%20Generation.md)  
<font color=orange>**Origin:**</font> Arxiv 2024.06; Fudan University; Bytedance **[[Project Code](https://github.com/FoundationVision/OmniTokenizer)]**  
<font color=orange>**Authors:**</font> Junke Wang, Yi Jiang, Zehuan Yuan.  
<font color=orange>**Label:**</font> Image Video tokenizer;  
<font color=orange>**Abastract:**</font> a transformer-based tokenizer for joint image and video tokenization  


* [<font size=3>**004 Alleviating Distortion in Image Generation via Multi-Resolution Diffusion Models and Time-Dependent Layer Normalization**</font>](2024.12.04-2024.12.11/004%20Alleviating%20Distortion%20in%20Image%20Generation.md)  
<font color=orange>**Origin:**</font> Arxiv 2024.06; Johns Hopkins University; Bytedance **[[Project Code](https://qihao067.github.io/projects/DiMR)]**  
<font color=orange>**Authors:**</font> Qihao Liu; Zhanpeng Zeng; Ju He; etc.  
<font color=orange>**Label:**</font> Diffusion model; multi-resolution  
<font color=orange>**Abastract:**</font> augmenting the Diffusion model with the Multi-Resolution network (DiMR), a framework that refines features across multiple resolutions, progressively enhancing detail from low to high resolution.    


* [<font size=3>**006 Scaling the Codebook Size of VQGAN to 100,000 with a Utilization Rate of 99%**</font>](2024.12.04-2024.12.11/006%20Scaling%20the%20Codebook%20Size%20of%20VQGAN.md)  
<font color=orange>**Origin:**</font> Arxiv 2024.06; Peking University Microsoft Research Asia **[[Project Code](https://github.com/zh460045050/VQGAN-LC)]**  
<font color=orange>**Authors:**</font> Lei Zhu; FangyunWei; Yanye Lu; Dong Chen;  
<font color=orange>**Label:**</font> VQGAN; Codebook  
<font color=orange>**Abastract:**</font> Unlike previous methods that optimize each codebook entry, our approach begins with a codebook initialized with 100,000 features extracted by a pre-trained vision encoder. Optimization then focuses on training a projector that aligns the entire codebook with the feature distributions of the encoder in VQGAN-LC.  


* [<font size=3>**007 WAVELETS ARE ALL YOU NEED FOR AUTOREGRESSIVE IMAGE GENERATION**</font>](2024.12.04-2024.12.11/006%20Scaling%20the%20Codebook%20Size%20of%20VQGAN.md)  
<font color=orange>**Origin:**</font> Arxiv 2024.11; **[[No code]()]**  
<font color=orange>**Authors:**</font> WAEL MATTAR, IDAN LEVY, NIR SHARON AND SHAI DEKEL  
<font color=orange>**Label:**</font> Wavelet; Autoregressive Image Generation;  
<font color=orange>**Abastract:**</font> wavelet image encoding; a variant of a language transformer whose architecture is re-designed and optimized for token sequences in this ‘wavelet language’.


* [<font size=3>**009 Scalable Autoregressive Image Generation with Mamba**</font>](2024.12.04-2024.12.11/009%20Scalable%20Autoregressive%20Image%20Generation%20with%20Mamba.md)  
<font color=orange>**Origin:**</font> CoRR 2024; Beijing University of Posts and Telecommunications; University of Chinese Academy of Sciences; The Hong Kong Polytechnic University **[[Project Code](https://github.com/hp-l33/AiM)]**  
<font color=orange>**Authors:**</font> Haopeng Li; Jinyue Yang; Kexin Wang; etc.  
<font color=orange>**Label:**</font> Mamba, VAR, Autoregressive Image Generation;  
<font color=orange>**Abastract:**</font> We introduce AiM, an autoregressive (AR) image generative model based on Mamba architecture. AiM employs Mamba, a novel state-space model characterized by its exceptional performance for long-sequence modeling with linear time complexity, to supplant the commonly utilized Transformers in AR image generation models, aiming to achieve both superior generation quality and enhanced inference speed.


* [<font size=3>**010 OPEN-MAGVIT2: AN OPEN-SOURCE PROJECT TOWARD DEMOCRATIZING AUTO-REGRESSIVE VISUAL GENERATION**</font>](2024.12.04-2024.12.11/010%20OpenMAGVIT.md)  
<font color=orange>**Origin:**</font> Arxiv 2024.09; ARC Lab Tencent Tsinghua University **[[Project Code](https://github.com/TencentARC/Open-MAGVIT2)]**  
<font color=orange>**Authors:**</font> Zhuoyan Luo; Fengyuan Shi; Yixiao Ge; etc.  
<font color=orange>**Label:**</font> Llama, Autoregressive Image Generation;  
<font color=orange>**Abastract:**</font> The Open-MAGVIT2 project produces an opensource replication of Google’s MAGVIT-v2 tokenizer, a tokenizer with a superlarge codebook (i.e., 218 codes), and achieves the state-of-the-art reconstruction performance (1.17 rFID) on ImageNet 256 ˆ 256. Furthermore, we explore its application in plain auto-regressive models and validate scalability properties. To assist auto-regressive models in predicting with a super-large vocabulary, we factorize it into two sub-vocabulary of different sizes by asymmetric token factorization, and further introduce “next sub-token prediction” to enhance sub-token interaction for better generation quality.


* [<font size=3>**011 SGC-VQGAN: SGC-VQGAN: Towards Complex Scene Representation via Semantic Guided Clustering Codebook**</font>](2024.12.04-2024.12.11/010%20OpenMAGVIT.md)  
<font color=orange>**Origin:**</font> Arxiv 2024.09; Sensetime Research; Tsinghua University **[[Project Code](https://github.com/TencentARC/Open-MAGVIT2)]**  
<font color=orange>**Authors:**</font> Chenjing Ding; ChiyuWang; Boshi Liu; etc.  
<font color=orange>**Label:**</font> VQGAN; Clustering    
<font color=orange>**Abastract:**</font> We introduce SGC-VQGAN through Semantic Online Clustering method to enhance token semantics through Consistent Semantic Learning. Utilizing inference results from segmentation model , our approach constructs a temporospatially consistent semantic codebook, addressing issues of codebook collapse and imbalanced token semantics. Our proposed Pyramid Feature Learning pipeline integrates multi-level features to capture both image details and semantics simultaneously.


* [<font size=3>**013 EZIGen: Enhancing zero-shot personalized image generation with precise subject encoding and decoupled guidance**</font>](2024.12.04-2024.12.11/012%20G3PT%20Unleash%20the%20power%20of%20Autoregressive%20Modeling%20in%203D%20Generation.md)  
<font color=orange>**Origin:**</font> Arxiv 2024.09; University of Adelaide, Xidian University **[[Project Code](https://github.com/ZichengDuan/EZIGen)]**  
<font color=orange>**Authors:**</font> Zicheng Duan; Yuxuan Ding; Chenhui Gou; etc.    
<font color=orange>**Label:**</font> Personalization; zero-shot;  
<font color=orange>**Abastract:**</font> employs two main components: a
carefully crafted subject image encoder based on the pretrained UNet of the Stable Diffusion model, following a process that balances the two guidances by separating their dominance stage and revisiting certain time steps to bootstrap subject transfer quality.


* [<font size=3>**014 BAD: BIDIRECTIONAL AUTO-REGRESSIVE DIFFUSION FOR TEXT-TO-MOTION GENERATION**</font>](2024.12.04-2024.12.11/014%20BAD.md)  
<font color=orange>**Origin:**</font> Arxiv 2024.09; Amirkabir University of Technology **[[Project Code](https://github.com/RohollahHS/BAD)]**  
<font color=orange>**Authors:**</font> Seyed Rohollah Hosseyni; Ali Ahmad Rahmani; etc.    
<font color=orange>**Label:**</font> Diffusion; Bidirectional;  
<font color=orange>**Abastract:**</font> we propose Bidirectional Autoregressive Diffusion (BAD), a novel approach that unifies the strengths of autoregressive and mask-based generative models. BAD utilizes a permutation-based corruption technique that preserves the natural sequence structure while enforcing causal dependencies through randomized ordering, enabling the effective capture of both sequential and bidirectional relationships



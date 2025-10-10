### Summary of the Paper: "Squeezing Deep Learning into Mobile and Embedded Devices"

**Authors:**
- Nicholas D. Lane (University College London and Nokia Bell Labs)
- Sourav Bhattacharya and Akhil Mathur (Nokia Bell Labs)
- Petko Georgiev (Google DeepMind)
- Claudio Forlivesi and Fahim Kawsar (Nokia Bell Labs)

**Publication:**
- IEEE Pervasive Computing, 2017

**Overview:**
This paper discusses the challenges and progress in integrating deep learning (DL) models into mobile and embedded devices, which are resource-constrained in terms of memory, computational power, and energy. The authors explore various techniques to optimize DL models for these devices, focusing on inference (execution) rather than training, which is typically done off-device.

**Key Points:**

1. **Resource Constraints:**
   - Deep learning models often have millions of parameters, making them challenging to deploy on devices with limited memory and computational resources.
   - Techniques such as low-precision parameters (8-bit or 16-bit) and weight quantization are used to reduce model size and improve efficiency.

2. **Early Smartphone Sensing Results:**
   - The authors began exploring DL on smartphones in 2014, focusing on activity recognition and context sensing.
   - They found that generic deep networks could outperform hand-crafted features and shallow models, even when constrained to a smaller size.

3. **Low-Power Deep Networks via Heterogeneous Compute:**
   - Digital Signal Processors (DSPs) in smartphones are energy-efficient and can support continuous sensor data processing.
   - The authors demonstrated that deep networks could run efficiently on DSPs, with systems like DeepEar achieving high accuracy in audio context recognition.

4. **Smartwatch Applications:**
   - Smartwatches, with their limited resources, can also benefit from DL.
   - The authors showed that DNNs suitable for smartwatches (around 200,000 parameters) outperformed existing classifiers in various sensing tasks.
   - They also demonstrated the execution of resource-intensive models like VGG on smartwatches using techniques like kernel separation and SVD-based compression.

5. **Embedded Processors:**
   - Embedded processors, such as ARM Cortex series, have even more severe resource constraints.
   - The authors developed a sparse coding method to compress DNNs, enabling them to fit and execute on these devices.
   - Experiments showed significant reductions in model size and execution time, making it feasible to run smartphone-class audio models on embedded processors.

6. **Local Execution of Multiple Deep Models:**
   - Most devices will need to execute multiple DL models for various tasks.
   - The authors designed an inference pipeline that optimizes the execution of multiple CNNs by scheduling and batching layers to maximize resource utilization.
   - The DeepEye prototype, a wearable camera, demonstrated the effectiveness of this pipeline in lifelogging and vision assistance applications.

**Conclusion:**
The paper highlights the progress and potential of deep learning on mobile and embedded devices, emphasizing the importance of resource-efficient techniques. The authors predict continued advancements in activity and context recognition, as well as the potential for on-device training and broader application of DL in control and decision tasks.

**References:**
- The paper cites several key works in the field, including studies on deep learning architectures, compression techniques, and hardware optimizations, providing a comprehensive overview of the current state of research.

</br>
</br>
</br>


### Summary of the Paper: "Visual Sensors Hardware Platforms: A Review"

**Author:**
- Daniel G. Costa, Senior Member, IEEE

**Publication:**
- IEEE Sensors Journal, Vol. 20, No. 8, April 15, 2020

**Abstract:**
This paper reviews the development of visual sensor networks (VSNs) over the past two decades, focusing on the hardware platforms and cameras used in these networks. It provides a taxonomy for visual sensor hardware platforms and discusses how to choose the most appropriate hardware when designing and implementing modern (wireless) visual sensor networks.

**Key Points:**

1. **Introduction:**
   - Visual sensor networks (VSNs) have evolved significantly, contributing to the maturation of the Internet of Things (IoT) landscape.
   - The development of VSNs has been influenced by advancements in hardware platforms and low-power cameras.
   - The paper aims to review the past developments of visual sensors, focusing on hardware platforms and providing a taxonomy for them.

2. **Building Visual Sensors:**
   - Visual sensors consist of a camera, processing unit, storage unit, energy supply, and communication interface.
   - Key performance issues for visual sensors include:
     - **Operation Time:** The time from data acquisition to transmission.
     - **Energy Consumption:** Important for battery-powered devices.
     - **Data Saving:** Efficient storage of visual data.
     - **Visual Data Quality:** Image resolution, brightness, contrast, and compression.
     - **Visual Coverage:** Field of View and camera movement capabilities.

3. **Classifying Visual Sensors Platforms:**
   - **Construction Blocks:**
     - **Sensor Motes:** Early platforms with limited processing and memory capabilities, suitable for scalar data but constrained for visual data.
     - **Open-Source Electronics Platforms:** More powerful and flexible, such as Arduino, Raspberry Pi, and ESP8266, which have become popular for visual sensing applications.
   - **Camera-Enabled Systems:**
     - **User-Centric Boards:** Devices like smartphones, smart glasses, and smartwatches that can be configured as visual sensor nodes.
     - **Application-Centric Boards:** Devices like drones and robots that can be reconfigured for visual sensing tasks.

4. **Two Decades of Visual Sensor Applications and Networks:**
   - The evolution of visual sensors has seen a shift from specialized sensor motes to more powerful and flexible open-source platforms.
   - Key trends include the use of commercial products, open-source platforms, and camera-enabled systems.
   - The paper provides a taxonomy for visual sensor hardware platforms, which can guide the selection of appropriate platforms for specific applications.

5. **Choosing Visual Sensors Platforms:**
   - **Execution:** Size, networking capabilities, robustness, and execution time requirements.
   - **Acquisition:** Cost, purchase availability.
   - **Development:** Programmability, documentation, and community support.
   - **Electronics:** Available interfaces and extension boards.

6. **Available Platforms and Practical Issues:**
   - The evolution of visual sensors has been driven by the availability of more powerful and affordable open-source boards.
   - Combining different approaches (e.g., a drone with a Raspberry Pi) can be highly beneficial.
   - Networking standards like LoRaWAN and 5G are being integrated into visual sensor platforms.
   - High-definition cameras and efficient miniaturized cameras are enhancing the quality of visual data.

7. **A World of Resource-Constrained Sensors?**
   - The traditional concept of "resource constraints" in visual sensing is changing due to the availability of more powerful and energy-efficient hardware.
   - Future developments will likely focus on "computing on the edge" and the integration of AI and machine learning algorithms on sensor nodes.

8. **Conclusion:**
   - The paper provides a comprehensive review of visual sensor hardware platforms, their evolution, and a taxonomy to support future developments in the field.

**References:**
- The paper cites numerous works on sensor networks, IoT, and visual sensor platforms, providing a solid foundation for understanding the current state and future directions of visual sensor networks.

This summary captures the main points and contributions of the paper, highlighting the evolution and current state of visual sensor hardware platforms.

</br>
</br>
</br>



### Summary of the Paper: "Replacing Mobile Camera ISP with a Single Deep Learning Model"

**Authors:**
- Andrey Ignatov (ETH Zurich, Switzerland)
- Luc Van Gool (ETH Zurich, Switzerland)
- Radu Timofte (ETH Zurich, Switzerland)

**Publication:**
- IEEE Sensors Journal, 2020

**Abstract:**
This paper demonstrates that a single end-to-end deep learning model can replace complex hand-crafted camera ISP (Image Signal Processing) pipelines. The authors introduce PyNET, a novel pyramidal CNN architecture designed for fine-grained image restoration, which can convert RAW Bayer data from a mobile camera sensor into high-quality RGB images comparable to those from a professional DSLR camera. The model is trained without prior knowledge of the sensor and optics used in the device. The authors validate their approach using a large-scale dataset of 10,000 RAW–RGB image pairs captured with the Huawei P20 smartphone and a Canon 5D Mark IV DSLR.

**Key Points:**

1. **Introduction:**
   - The quality of mobile photography has improved significantly over the years, driven by advancements in hardware and ISP software.
   - Modern mobile ISPs are complex systems that perform tasks like demosaicing, denoising, white balancing, and color correction.
   - Despite these advancements, mobile ISPs still struggle with issues like noise, detail loss, and color rendering.
   - The authors propose a deep learning model to replace the entire ISP pipeline, aiming to produce high-quality images comparable to those from professional DSLR cameras.

2. **Zurich RAW to RGB Dataset:**
   - A large-scale dataset consisting of 20,000 photos was collected using the Huawei P20 smartphone (12.3 MP Sony Exmor IMX380 sensor) and a Canon 5D Mark IV DSLR.
   - The dataset includes RAW Bayer data from the Huawei P20 and corresponding high-quality RGB images from the Canon 5D Mark IV.
   - The images were captured in various environments and conditions to ensure diversity.
   - The dataset was preprocessed to align the RAW and RGB images using SIFT keypoints and RANSAC, and then divided into training, validation, and testing sets.

3. **Proposed Method:**
   - **PyNET CNN Architecture:**
     - PyNET is a pyramidal CNN architecture designed to process images at multiple scales.
     - The model has an inverted pyramidal shape and processes images at five different scales.
     - Each scale uses convolutional filters of different sizes (3x3 to 9x9) to learn a diverse set of features.
     - The outputs from lower scales are upsampled and combined with features from higher scales to refine the results.
     - The model uses Leaky ReLU activation functions and instance normalization.
     - The training is performed sequentially, starting from the lowest scale and moving up to the original resolution.

   - **Loss Functions:**
     - The loss function varies depending on the scale:
       - **Levels 4-5:** Minimize mean squared error (MSE) for global color and brightness correction.
       - **Levels 2-3:** Combine VGG-based perceptual loss and MSE for refining color and shape properties.
       - **Level 1:** Use a combination of VGG loss, SSIM loss, and MSE for local image corrections like texture enhancement and noise removal.

4. **Experiments:**
   - **Quantitative Evaluation:**
     - The proposed PyNET model was compared with several other deep learning architectures (SPADE, DPED, U-Net, Pix2Pix, SRGAN, VDSR, SRCNN) on the test set.
     - PyNET achieved the highest PSNR and MS-SSIM scores, outperforming the other models.
     - The visual results confirmed the quantitative improvements, with PyNET producing images with better color accuracy and texture detail.

   - **User Study:**
     - A user study was conducted using Amazon Mechanical Turk to assess the perceptual quality of the images.
     - Users rated the images produced by PyNET, the Huawei P20 ISP, and the Canon 5D Mark IV.
     - PyNET scored higher than the Huawei P20 ISP and was closer to the quality of the Canon 5D Mark IV.

   - **Generalization to Other Camera Sensors:**
     - The model was tested on RAW images from a different smartphone (BlackBerry KeyOne) to evaluate its generalization capabilities.
     - PyNET was able to reconstruct high-quality images, demonstrating its potential for use with different camera sensors.

5. **Conclusions:**
   - The proposed PyNET model can effectively replace traditional hand-crafted ISP pipelines, producing high-quality images comparable to those from professional DSLR cameras.
   - The model's performance was validated through quantitative metrics, user studies, and generalization tests.
   - The results show the viability of using a single deep learning model for end-to-end image processing in mobile cameras.
   - Future work could focus on further improving the model's flexibility and performance.

**References:**
- The paper cites numerous works on image processing, deep learning, and ISP techniques, providing a comprehensive background for the proposed approach.

This summary captures the main contributions and findings of the paper, highlighting the effectiveness of the PyNET model in replacing traditional ISP pipelines with a single deep learning solution.

</br>
</br>
</br>

### Summary of the Paper: "Power- and Time-Aware Deep Learning Inference for Mobile Embedded Devices"

**Authors:**
- WOOCUL KANG (Member, IEEE)
- JAEYONG CHUNG (Member, IEEE)

**Affiliations:**
- Department of Embedded Systems Engineering, Incheon National University, Incheon, South Korea
- Department of Electronic Engineering, Incheon National University, Incheon, South Korea

**Corresponding Author:**
- Jaeyong Chung (jychung@inu.ac.kr)

**Funding:**
- This work was supported by the Basic Science Research Program through the National Research Foundation of Korea (NRF) and the Incheon National University Research Grant in 2018.

**Abstract:**
This paper introduces DeepRT, a deep learning inference runtime designed to support predictable inference latency and power consumption for cyber-physical systems (CPS) on mobile and embedded devices. DeepRT uses a Multiple Inputs/Multiple Outputs (MIMO) feedback control architecture to manage multiple Quality-of-Service (QoS) objectives, such as inference latency and power consumption, under unpredictable workloads. The authors demonstrate the effectiveness of DeepRT through a prototype implementation and evaluation.

**Key Points:**

1. **Introduction:**
   - Deep learning is crucial for many CPS applications, such as autonomous vehicles and wearable devices.
   - Inference tasks often need to be performed locally on resource-constrained devices to address latency, power consumption, and bandwidth concerns.
   - Existing approaches focus on "best-effort" performance, leading to unpredictable behavior in dynamic environments.
   - DeepRT aims to provide predictable inference performance by managing multiple QoS objectives simultaneously.

2. **Overview of DeepRT:**
   - **Deep Learning Inference:**
     - Deep learning models consist of layers that transform input data into output.
     - Inference tasks involve passing input data through these layers, often using both CPUs and GPUs.
   - **Service Model:**
     - Applications request inference tasks with a deep learning model and QoS specifications (deadline and power consumption).
     - DeepRT supports soft real-time applications, where missing deadlines is still acceptable but should be minimized.

3. **Power- and Time-Aware Inference:**
   - **QoS Metrics:**
     - **Tardiness:** The ratio of actual inference latency to target inference latency.
     - **Power Consumption:** Proportional to the processor frequency and supply voltage.
   - **QoS Management Architecture:**
     - **MIMO Feedback Control:**
       - Monitors the performance of inference tasks and adjusts CPU and GPU frequencies to meet QoS goals.
       - Uses a linear time-invariant MIMO model to capture the interactions between control inputs (frequencies) and system outputs (tardiness and power).
     - **Feedback Control Procedure:**
       - Computes QoS errors (tardiness and power consumption errors).
       - Adjusts CPU and GPU frequencies to reduce these errors.
       - Uses milestones in the deep learning model to monitor progress and provide timely feedback.

4. **Evaluation:**
   - **Implementation and Testbed:**
     - DeepRT is implemented by extending Caffe, a popular deep learning framework.
     - The testbed uses a NVIDIA Jetson TK1 mobile platform with Ubuntu 14.04 Linux.
     - Power consumption is monitored using a Yokogawa WT310E power meter.
   - **Baselines and Evaluation Goals:**
     - Baselines include Open (default Caffe with on-demand CPU DVFS), MIMO (DeepRT), SISOmax (target tardiness via GPU frequency control), and SISOopen (target tardiness via GPU and on-demand CPU DVFS).
     - Evaluation focuses on supporting multiple QoS goals and robustness against unpredictable workloads.
   - **Average Performance:**
     - DeepRT closely supports target tardiness and power consumption for both CaffeNet and GoogLeNet models.
     - MIMO outperforms other approaches in maintaining QoS goals under varying conditions.
   - **Transient Performance and Robustness:**
     - DeepRT quickly stabilizes tardiness and power consumption in the presence of sudden workload changes.
     - MIMO shows better robustness compared to SISOmax, which only supports tardiness but not power consumption.

5. **Related Work:**
   - **Efficient Deep Learning Inference:**
     - Hardware accelerators and software-based approaches have been proposed to improve inference performance.
     - However, these approaches do not support predictable QoS.
   - **Control Theory:**
     - Feedback control is widely used in computing systems but has not been applied to deep learning inference with multiple QoS goals.
   - **Dynamic Voltage and Frequency Scaling (DVFS):**
     - DVFS is a primary method to control processor speed and power consumption.
     - DeepRT uses PWM to emulate continuous frequency levels using discrete levels.

6. **Conclusions:**
   - DeepRT provides a control-theoretic solution to support predictable inference performance in CPS.
   - The MIMO feedback control architecture effectively manages multiple QoS objectives, such as latency and power consumption.
   - Future work includes extending the feedback controller to include more QoS metrics and supporting adaptive control.

**References:**
- The paper cites numerous works on deep learning, control theory, and power management, providing a comprehensive background for the proposed approach.

This summary captures the main contributions and findings of the paper, highlighting the effectiveness of DeepRT in managing multiple QoS objectives for deep learning inference on mobile and embedded devices.


</br>
</br>
</br>

### Summary of the Paper: "Deep Learning-Based Real-Time Multiple-Object Detection and Tracking from Aerial Imagery via a Flying Robot with GPU-Based Embedded Devices"

**Authors:**
- Sabir Hossain
- Deok-jin Lee (Corresponding Author: deokjlee@kunsan.ac.kr)

**Affiliations:**
- School of Mechanical & Convergence System Engineering, Kunsan National University, 558 Daehak-ro, Gunsan 54150, Korea

**Received:**
- 30 May 2019
- Accepted: 26 July 2019
- Published: 31 July 2019

**Abstract:**
This paper presents a deep learning-based method for real-time multiple-object detection and tracking from aerial imagery using drones equipped with onboard GPU-based embedded devices. The authors developed and compared different embedded systems, including Jetson TX1, TX2, and AGX Xavier, as well as GPU-constrained systems like Raspberry Pi, Latte Panda, and Odroid Xu4, augmented with Intel Movidius Neural Compute Stick (NCS). The study also includes the implementation of a ground station with a GTX 1080 GPU for off-board processing. The effectiveness of the proposed systems is demonstrated through real-time experiments with a small multi-rotor drone.

**Key Points:**

1. **Introduction:**
   - **Target Detection and Tracking:**
     - Increasing demand for target detection and tracking from aerial imagery using drones.
     - Traditional vision-based algorithms have limitations in accuracy and future data prediction.
     - Deep learning algorithms provide more accurate results and can handle unknown future data.
   - **Embedded Systems:**
     - Onboard systems are essential for real-time processing and reduced latency.
     - Off-board systems can handle more complex computations but may face communication issues.
   - **Applications:**
     - Intelligence, surveillance, and reconnaissance missions.
     - Autonomous vehicle guidance systems.
     - Traffic management and emergency response.

2. **Hardware Development of the Drone Framework:**
   - **Drone Specifications:**
     - X-configuration with dimensions 30 cm × 30 cm × 25 cm.
     - 20-minute flight duration and 2.5 kg payload.
     - Equipped with a 5-MP USB 3.0 camera.
   - **Embedded Systems:**
     - **On-Board GPU Systems:**
       - Jetson TX1, TX2, and AGX Xavier.
     - **Off-Board GPU-Based Ground Station:**
       - GTX 1080 GPU.
     - **On-Board GPU-Constrained Systems:**
       - Raspberry Pi, Latte Panda, and Odroid Xu4 with Movidius NCS.

3. **Technical Specifications of Different Embedded Devices:**
   - **Jetson Modules:**
     - **TX1:**
       - Maxwell GPU with 256 CUDA cores.
       - 4 GB LPDDR4 memory.
     - **TX2:**
       - Pascal GPU with 256 CUDA cores.
       - 8 GB LPDDR4 memory.
     - **AGX Xavier:**
       - Volta GPU with 512 cores and Tensor Cores.
       - 16 GB LPDDR4x memory.
   - **GPU-Constrained Devices:**
     - **Raspberry Pi 3:**
       - 1.2 GHz 64-bit quad-core ARMv8 CPU.
       - 1 GB memory.
     - **Latte Panda:**
       - Intel Cherry Trail Z8350 Quad Core CPU.
       - 4 GB DDR3L memory.
     - **Odroid Xu4:**
       - Samsung Exynos5422 Cortex-A15 2 GHz and Cortex-A7 Octa-core CPUs.
       - 2 GB LPDDR3 RAM.
   - **Movidius Neural Compute Stick:**
     - Low-power, high-performance VPU.
     - USB 3.0 Type A connector.
     - Enhances deep learning performance on constrained devices.

4. **Implemented Object Detection Algorithms:**
   - **YOLO (You Only Look Once):**
     - **YOLOv2:**
       - Real-time processing with high accuracy.
       - Improved recall and accuracy with fewer layers.
     - **YOLOv3:**
       - Multi-label classification.
       - Independent logistic classifiers for better performance.
     - **YOLO-9000:**
       - Enhanced with batch normalization and high-resolution classifier.
       - Faster and stronger with multi-scale training.
   - **SSD (Single Shot MultiBox Detector):**
     - Single network for object localization and classification.
     - Uses anchor boxes and convolutional layers for bounding box prediction.
   - **Faster R-CNN:**
     - Region proposal network for faster detection.
     - High accuracy but lower frame rate.
   - **Mask R-CNN:**
     - Extension of Faster R-CNN for pixel-level segmentation.
     - Adds a binary mask to determine object boundaries.
   - **DeepLab-v3:**
     - Semantic segmentation with atrous spatial pyramid pooling.
     - Enhanced with a decoder module for better boundary detection.

5. **Implemented Target Tracking Algorithm:**
   - **Deep SORT:**
     - Integrates appearance information to enhance tracking efficiency.
     - Reduces identity switches by 45%.
     - Uses a convolutional neural network (CNN) trained on a large-scale person re-identification dataset.
   - **Guiding the UAV:**
     - Algorithm to fly the drone toward a target using YOLOv2.
     - Calculates the area of the bounding box and adjusts the drone's yaw angle and forward velocity.

6. **Results:**
   - **Detection Results:**
     - Jetson AGX Xavier showed the best performance with YOLOv3.
     - Faster R-CNN provided accurate results but with low frame rates.
     - YOLOv2 was effective for close-range detection.
   - **Tracking Results:**
     - Deep SORT with YOLOv3 provided robust tracking even from a distance.
   - **Performance Comparison:**
     - Jetson AGX Xavier outperformed other systems in terms of frame rate and accuracy.
     - GPU-constrained systems like Odroid Xu4 with Movidius NCS showed reasonable performance for low-cost, low-power applications.

7. **Discussion:**
   - **Algorithm Selection:**
     - YOLOv3 was chosen for its balance of accuracy and performance.
     - YOLO tiny versions were not suitable for far-distance detection.
   - **Input Resolution:**
     - Higher input resolution improved detection accuracy but reduced frame rate.
   - **Guiding Algorithm:**
     - Effective for single-target tracking but needs improvement for multiple targets.

8. **Conclusions:**
   - Jetson AGX Xavier is a powerful on-board GPU system for real-time object detection and tracking.
   - GPU-constrained systems with Movidius NCS are suitable for low-cost, low-power applications.
   - Deep SORT with YOLOv3 provides robust tracking performance.
   - Further research is needed to improve the guiding algorithm for multiple targets and to enhance overall system robustness.

**References:**
- The paper cites numerous works on deep learning, object detection, and drone systems, providing a comprehensive background for the proposed approach.

This summary captures the main contributions and findings of the paper, highlighting the effectiveness of the proposed deep learning-based systems for real-time multiple-object detection and tracking from aerial imagery using drones.


</br>
</br>
</br>

### Summary of the Paper: "Scheduling of Deep Learning Applications Onto Heterogeneous Processors in an Embedded Device"

**Authors:**
- Duseok Kang (Member, IEEE)
- Jinwoo Oh
- Jongwoo Choi
- Youngmin Yi
- Soonhoi Ha (Fellow, IEEE)

**Affiliations:**
- Department of Computer Engineering, Seoul National University, Seoul 08826, South Korea
- Department of Electrical and Computer Engineering, University of Seoul, Seoul 02504, South Korea

**Corresponding Author:**
- Soonhoi Ha (sha@snu.ac.kr)

**Funding:**
- National Research Foundation of Korea (NRF) funded by the Ministry of Education under Grant 2018R1D1A1B07050463
- Ministry of Science and ICT under Grant 2019R1A2B5B02069406

**Abstract:**
This paper addresses the challenges of scheduling deep learning (DL) applications on heterogeneous processors in embedded devices. The authors propose a scheduling technique based on a Genetic Algorithm (GA) to optimize the throughput and energy consumption of DL applications. The paper also considers practical issues such as Dynamic Voltage and Frequency Scaling (DVFS), CPU utilization constraints, and thermal management. The proposed method is verified on two embedded devices: Galaxy S9 and HiKey970.

**Key Points:**

1. **Introduction:**
   - **On-Device Deep Learning:**
     - Increasing demand for running DL applications directly on embedded devices to avoid privacy concerns and network issues.
     - Embedded devices are becoming more heterogeneous, equipped with multi-core CPUs, GPUs, and NPUs.
     - Need to schedule multiple DL applications concurrently on shared heterogeneous processors.
   - **Challenges:**
     - Task mapping onto single or multiple cores.
     - DVFS impact on task execution times.
     - CPU utilization constraints to avoid overheating.
     - Core shutdown due to low utilization.

2. **Hardware Platform and System Model:**
   - **Galaxy S9:**
     - Mali-G72 MP18 GPU.
     - big.LITTLE CPUs: quad-core M3 at 2.7 GHz and quad-core Cortex-A55 at 1.79 GHz.
     - Aggressive DVFS policy and CPU hot-plug feature.
   - **HiKey970:**
     - Mali-G72 MP12 GPU.
     - big.LITTLE CPUs: quad-core A73 at 2.36 GHz and quad-core Cortex-A53 at 1.8 GHz.
     - NPU for DL acceleration.
     - No DVFS policy.

3. **Proposed Scheduling Framework:**
   - **Task Profiling:**
     - Profiling task execution times and communication overheads on different PEs.
     - Adjusting CPU execution times based on observed CPU frequency and DVFS.
   - **Communication Overhead:**
     - Estimating communication overhead between different PEs using OpenCL APIs.
   - **NPU Profiling:**
     - Indirect performance estimation based on reported performance comparisons.
   - **Baseline Task-Clustering Scheduler:**
     - Partitioning the DNN into sub-networks and mapping them onto processors.
     - Using Integer Linear Programming (ILP) to find the best solution.
   - **GA-Based Scheduler:**
     - Using GA to find Pareto-optimal solutions in terms of throughput and energy consumption.
     - Fitness function includes throughput, energy consumption, and CPU utilization constraints.

4. **Experimental Results:**
   - **Throughput Performance:**
     - GA-based scheduling outperforms task-clustering scheduling in most cases.
     - (1,1,1,1) PE configuration generally provides the best throughput.
   - **Multi-Objective Scheduling:**
     - GA scheduler generates Pareto-optimal solutions for multiple DL applications.
     - Trade-offs between response times and energy consumption are explored.

5. **Verification with Real Hardware Platforms:**
   - **Parallelization of MobileNet v1 and MobileNet v2:**
     - Verification on Galaxy S9 and HiKey970.
     - Error in performance estimation is less than 7% in most cases.
   - **Challenges:**
     - Limitations in ACL implementation for multi-core CPU configurations.
     - Inaccuracies in task and communication profiling.

6. **Conclusion:**
   - The proposed scheduling framework effectively optimizes throughput and energy consumption for DL applications on heterogeneous embedded devices.
   - Practical issues such as DVFS and CPU utilization constraints are considered.
   - Verification with real hardware platforms demonstrates the accuracy of the proposed method.

**References:**
- The paper cites numerous works on deep learning frameworks, scheduling techniques, and hardware platforms, providing a comprehensive background for the proposed approach.

This summary captures the main contributions and findings of the paper, highlighting the effectiveness of the proposed GA-based scheduling technique for deep learning applications on heterogeneous embedded devices.


</br>
</br>
</br>

### Summary of the Paper: "Digital Retina: A Way to Make the City Brain More Efficient by Visual Coding"

**Authors:**
- Wen Gao (Fellow, IEEE)
- Siwei Ma (Senior Member, IEEE)
- Lingyu Duan (Member, IEEE)
- Yonghong Tian (Senior Member, IEEE)
- Peiyin Xing
- Yaowei Wang (Member, IEEE)
- Shanshe Wang (Member, IEEE)
- Huizhu Jia
- Tiejun Huang (Senior Member, IEEE)

**Affiliations:**
- School of Electronics Engineering and Computer Science, Peking University, Beijing, China
- Peng Cheng Laboratory, Shenzhen, China
- Vision Laboratory, Queen Mary University of London, UK

**Corresponding Author:**
- Yonghong Tian (yhtian@pku.edu.cn)

**Funding:**
- National Natural Science Foundation of China (Contracts 62088102, 61825101, U20B2052)

**Abstract:**
This paper introduces the concept of the "Digital Retina," a novel visual computing framework designed to enhance the efficiency and performance of the city brain system. The digital retina aligns high-efficiency sensing models with the Visual Coding for Machine (VCM) paradigm, enabling the city brain to better handle the massive amounts of visual data generated by ubiquitous camera networks. The framework consists of three streams: video, feature, and model, which work collaboratively over an end-edge-cloud platform. The paper discusses the enabling technologies, experimental validations, and potential applications of the digital retina in smart cities.

**Key Points:**

1. **Introduction:**
   - **Urbanization and City Brain:**
     - Rapid urbanization has led to complex social environments, necessitating advanced city management systems.
     - The city brain, a central decision system, relies on data from numerous sensors, including cameras, to monitor and manage urban activities.
   - **Challenges:**
     - The exponential growth of visual data far exceeds current sensing and networking capabilities.
     - Traditional "compression-then-analysis" paradigms are inefficient and degrade the quality of visual features.
     - Privacy concerns arise from the collection and processing of raw visual data.

2. **Digital Retina Concept:**
   - **One-Camera-Three-Streams Mechanism:**
     - Each camera generates three streams: compressed video, compact feature, and model.
     - The compressed video stream is for human monitoring and storage.
     - The compact feature stream is for machine vision tasks.
     - The model stream updates the feature extraction models at the edge and cloud.
   - **Biological Inspiration:**
     - Inspired by the biological retina, which encodes visual information and extracts features for the brain.
     - The digital retina aims to achieve a balance between efficient visual data representation and high-performance analysis.

3. **Enabling Technologies:**
   - **Intelligent Video Compression:**
     - Advanced video coding standards (e.g., AVS2, H.265) and DNN-based methods for efficient video representation.
     - Scene video coding techniques tailored to surveillance videos, exploiting static backgrounds and moving objects.
   - **Compact Feature Representation:**
     - Deep learning-based feature extraction and compression methods (e.g., DFC, DFJC).
     - Standardization efforts (e.g., MPEG CDVS, CDVA) for compact feature descriptors.
   - **Model Compression and Incremental Updating:**
     - Techniques for compressing and updating deep learning models (e.g., federated learning).
     - Standardization activities (e.g., IEEE 2941) for model communication.

4. **Optimization in Video Signal and Feature Representations:**
   - **Generalized Rate-Utility Optimization (GRUO):**
     - A theoretical framework for optimizing the representation of video signals and features.
     - Balances the trade-offs between bitrate, utility, and computational complexity.

5. **Digital Retina System with End-Edge-Cloud Computing:**
   - **Collaborative Computing Paradigm:**
     - Front-end devices (retina-like cameras) handle video encoding, feature extraction, and light intelligent tasks.
     - Edge servers store compressed video streams and perform local analysis.
     - Cloud servers undertake big data analysis and model updates.
   - **Advantages:**
     - Reduces network traffic and computational load.
     - Enhances privacy by transmitting compact features instead of raw images and videos.

6. **Prototype Implementation and Experimental Validations:**
   - **Hardware Implementation:**
     - Design of a digital retina chip (GV9531) supporting high-efficiency video and feature coding.
     - Integration of the chip into a System-on-Chip (SoC) or SoC+FPGA solutions.
   - **Experimental Results:**
     - Validation of the feature stream's efficiency in vehicle recognition and tracking tasks.
     - Demonstration of the model stream's effectiveness in incremental model updating.

7. **City Brain 2.0:**
   - **Enhanced Visual Computing:**
     - Real-time gathering of compact feature streams from distributed cameras.
     - On-demand fetching of compressed video streams for human monitoring.
     - Incremental model updates for improved analysis performance.
   - **Advantages:**
     - Better support for real-world applications and privacy protection.
     - Scalability and adaptability to different urban environments.

8. **Future Work:**
   - **Standardization:**
     - Development of standards for interoperability and system design.
   - **Open Source:**
     - Provision of open-source tools and hardware for developing retina-like cameras.
   - **Large-Scale Test-Bed:**
     - Establishment of a large-scale video big data test-bed to evaluate the digital retina's performance.

**Conclusion:**
The digital retina framework offers a powerful, effective, and efficient solution for visual computing in smart cities. By leveraging three streams—video, feature, and model—the digital retina can significantly improve the city brain's performance in handling massive visual data, while also addressing privacy and computational challenges. The paper's experimental results and prototype implementation demonstrate the feasibility and potential of the digital retina in real-world applications.

**References:**
- The paper cites numerous works on video coding, feature extraction, model compression, and smart city initiatives, providing a comprehensive background for the proposed digital retina framework.


</br>
</br>
</br>

### Summary of the Field of Joint Visual Data Coding and Embedded Visual Analytics

**Introduction:**
The field of Joint Visual Data Coding (JVDC) and Embedded Visual Analytics (EVA) is an emerging interdisciplinary area that combines the principles of data compression, machine learning, and visual analytics to efficiently process, analyze, and visualize large-scale visual data. This field aims to address the challenges of handling vast amounts of visual data, such as images and videos, by integrating data compression techniques with advanced analytics and visualization methods. The goal is to enable real-time, resource-efficient processing and analysis of visual data on embedded devices, which are increasingly prevalent in various applications, including autonomous vehicles, surveillance systems, and smart cities.

**Key Concepts:**

1. **Joint Visual Data Coding (JVDC):**
   - **Data Compression and Analytics Integration:**
     JVDC focuses on developing algorithms that simultaneously compress visual data and extract meaningful features for analytics. Traditional data compression techniques, such as JPEG and H.264, are designed to reduce the size of visual data for storage and transmission but do not consider the analytical value of the data. JVDC aims to bridge this gap by integrating compression with feature extraction and analytics, ensuring that the compressed data retains the essential information needed for subsequent analysis.
   - **Efficiency and Quality:**
     The primary challenge in JVDC is to achieve high compression ratios while maintaining the quality and utility of the data for analytics. This involves developing novel coding schemes that can efficiently represent the data in a compact form while preserving the features that are critical for tasks such as object detection, classification, and tracking.

2. **Embedded Visual Analytics (EVA):**
   - **Resource-Constrained Devices:**
     EVA focuses on performing visual analytics on resource-constrained devices, such as mobile phones, drones, and IoT devices. These devices often have limited computational power, memory, and energy resources, making it challenging to run complex analytics algorithms in real-time. EVA addresses this by optimizing algorithms to run efficiently on these devices, often using techniques such as model compression, quantization, and hardware acceleration.
   - **Real-Time Processing:**
     Real-time processing is a critical requirement in many EVA applications, such as autonomous driving and surveillance. EVA techniques must be designed to handle high data rates and provide timely insights, which is particularly challenging given the resource constraints of embedded devices.

**Key Techniques and Approaches:**

1. **Deep Learning and Neural Networks:**
   - **Feature Extraction:**
     Deep learning models, such as Convolutional Neural Networks (CNNs), are widely used in JVDC and EVA for feature extraction. These models can automatically learn hierarchical features from visual data, which are then used for compression and analytics. For example, a CNN can be trained to identify and compress regions of an image that are most relevant for object detection.
   - **Model Compression:**
     Techniques such as pruning, quantization, and knowledge distillation are used to reduce the size and computational complexity of deep learning models, making them suitable for deployment on embedded devices. These techniques help in achieving a balance between model accuracy and resource efficiency.

2. **Data Compression Techniques:**
   - **Hybrid Coding Schemes:**
     Hybrid coding schemes combine traditional compression methods with deep learning-based approaches to achieve better compression ratios and analytics performance. For example, a hybrid scheme might use a CNN to extract features and a traditional codec to compress the residual data.
   - **Rate-Distortion Optimization:**
     Rate-distortion optimization is a key concept in JVDC, where the goal is to find the optimal trade-off between the compression rate and the distortion (loss of information) in the compressed data. This is particularly important for ensuring that the compressed data remains useful for analytics.

3. **Embedded Systems and Hardware Acceleration:**
   - **Heterogeneous Processors:**
     Embedded devices often use heterogeneous processors, including multi-core CPUs, GPUs, and specialized accelerators like Neural Processing Units (NPUs). Efficient scheduling and resource management techniques are essential for optimizing the performance of visual analytics algorithms on these devices.
   - **Hardware Acceleration:**
     Hardware accelerators, such as FPGAs and ASICs, can significantly speed up the execution of visual analytics algorithms. These accelerators are designed to perform specific tasks, such as convolution operations, more efficiently than general-purpose processors.

**Applications:**

1. **Autonomous Vehicles:**
   - **Real-Time Object Detection and Tracking:**
     Autonomous vehicles require real-time processing of visual data to detect and track objects in the environment. JVDC and EVA techniques can help in efficiently compressing and analyzing the data from multiple cameras and sensors, enabling the vehicle to make timely decisions.
   - **Resource-Efficient Processing:**
     The computational resources in autonomous vehicles are limited, and EVA techniques can help in optimizing the use of these resources to perform complex tasks such as scene understanding and path planning.

2. **Surveillance Systems:**
   - **Anomaly Detection:**
     Surveillance systems can benefit from JVDC and EVA by efficiently compressing and analyzing video streams to detect anomalies and suspicious activities. This can help in reducing the storage and transmission costs while ensuring that the system can respond quickly to potential threats.
   - **Real-Time Monitoring:**
     Real-time monitoring of large areas, such as airports and public spaces, requires the processing of high-resolution video streams. EVA techniques can enable the deployment of surveillance systems on resource-constrained devices, making it possible to monitor these areas more effectively.

3. **Smart Cities:**
   - **Traffic Management:**
     Smart cities can use JVDC and EVA to efficiently process and analyze data from traffic cameras and sensors. This can help in real-time traffic management, reducing congestion, and improving safety.
   - **Environmental Monitoring:**
     Visual data from cameras and sensors can be used to monitor environmental conditions, such as air quality and pollution levels. EVA techniques can help in efficiently processing this data to provide timely insights and alerts.

**Challenges and Future Directions:**

1. **Scalability:**
   - Handling the increasing volume and complexity of visual data is a significant challenge. Future research should focus on developing scalable JVDC and EVA techniques that can handle large-scale data in real-time.

2. **Resource Efficiency:**
   - Optimizing the use of computational and energy resources on embedded devices is crucial. Research should explore new hardware architectures and algorithms that can further improve the efficiency of visual analytics on these devices.

3. **Interdisciplinary Collaboration:**
   - The field of JVDC and EVA requires collaboration between experts in data compression, machine learning, and embedded systems. Interdisciplinary research can lead to innovative solutions that address the unique challenges of this field.

4. **Ethical and Privacy Considerations:**
   - As visual data is often sensitive, ensuring the privacy and security of the data is essential. Future research should consider the ethical implications of JVDC and EVA and develop techniques that protect user privacy while enabling effective data analysis.

**Conclusion:**
The field of Joint Visual Data Coding and Embedded Visual Analytics is at the forefront of addressing the challenges of processing and analyzing large-scale visual data on resource-constrained devices. By integrating data compression with advanced analytics and visualization techniques, JVDC and EVA aim to enable real-time, efficient, and effective processing of visual data in various applications. Future research should focus on developing scalable, resource-efficient, and ethical solutions to further advance this field.

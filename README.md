GenAI is an integrated image-to-object mesh generator for Blender that aims to enable the creation of editable 3D meshes right inside Blender, without the use of third-party programs, through application of machine learning models into a working app.

Developed as part of an applied Masters thesis, titled "AN INTEGRATED IMAGE-TO-MODEL BLENDER ADD-ON: LEVERAGING GENERATIVE AI IN THE CREATION OF 3D ASSETS" for the University of Information Technology (UIT), a subsidiary of VNUHCM. The thesis in question has been successfully defended on June 21st, 2026.

Recommended to use Blender 4.3.0 on Windows. To install, download the pretrained model weights and wheels [here](https://huggingface.co/DoctorTryhard/genai_weights_wheels/tree/main) and move all the .whl files into a new folder, renamed 'wheels'. Then clone this repository, move the 'wheels' folder into the cloned repo and build using the command line:
```
blender --command extension build
```

### Credits:
#### Articles:
- Hong, Y., Zhang, K., Gu, J., Bi, S., Zhou, Y., Liu, D., Liu, F., Sunkavalli, K., Bui, T., Tan, H., [LRM: Large Reconstruction Model for Single Image to 3D](https://arxiv.org/abs/2311.04400) (2023), arXiv:2311.04400
- Tochilkin, D., Pankratz, D., Liu, Z., Huang, Z., Letts, A., Li, Y., Liang, D., Laforte, C., Jampani, V., Cao, Y. P., [TripoSR: Fast 3D Object Reconstruction from a Single Image](https://arxiv.org/abs/2403.02151) (2024),  	arXiv:2403.02151
- Li, W., Liu, J., Yan, H., Chen, R., Liang, Y., Chen, X., Tan, P., Long, X., [CraftsMan3D: High-fidelity Mesh Generation with 3D Native Generation and Interactive Geometry Refiner](https://arxiv.org/abs/2405.14979) (2024), arXiv:2405.14979
- Sun, X., Wu, J., Zhang, X., Zhang, Z., Zhang, C., Xue, T., Tenenbaum, J. B., Freeman, W. T., [Pix3D: Dataset and Methods for Single-Image 3D Shape Modeling](https://arxiv.org/abs/1804.04610) (2018), arXiv:1804.04610
- Chang, A. X., Funkhouser, T., Guibas, L., Hanrahan, P., Huang, Q., Li, Z., Savarese, S., Savva, M., Song, S., Su, H., Xiao, J., Yi, L., Yu, F., [ShapeNet: An Information-Rich 3D Model Repository](https://arxiv.org/abs/1512.03012) (2015), arXiv:1512.03012
#### Code:
- He, Z., Wang, T., [OpenLRM repo](https://github.com/3DTopia/OpenLRM)
- Tochilkin, D. et al., [TripoSR repo](https://github.com/VAST-AI-Research/TripoSR)
- Li, W. et al., [CraftsMan3D repo](https://github.com/HKUST-SAIL/CraftsMan3D)
- Liu, R. et al., [Blender rendering script for dataset preprocessing](https://github.com/cvlab-columbia/zero123/blob/main/objaverse-rendering/scripts/blender_script.py)
#### Datasets
- Sun, X. et al., [Pix3D dataset repo](https://github.com/xingyuansun/pix3d)
- Chang, A. X., et al., [ShapeNet homepage](https://shapenet.org/)
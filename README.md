# Artificial Identities: Analyzing Bias in Diffusion Model-Generated Images of Surgeons

**Authors:**  
Rahul Gorijavolu¹²⁶, Ife Shoyombo¹², Saurav Boparai²³, Andrew S. Cho¹², Emily O’Connell¹,  
Kaushik Madapati²⁴⁶, Vinayak Mathur⁶, Megan K. Applewhite⁷, Anne M. Stey⁵, Leo A. Celi⁶  

**Affiliations:**  
¹ Johns Hopkins University School of Medicine  
² ARGOS (AI for Responsible, Generalizable, and Open Surgical Research Group)  
³ Hackensack Meridian Health School of Medicine  
⁴ UC Berkeley College of Engineering  
⁵ Northwestern University Department of Surgery  
⁶ MIT Laboratory for Computational Physiology  
⁷ University of Chicago Department of Surgery  

---

## 🧩 Overview

This repository supports the study *“Artificial Identities: Analyzing Bias in Diffusion Model-Generated Images of Surgeons.”*  
The project examines how leading text-to-image diffusion models portray surgeons when prompted with the neutral term **“surgeon”**, assessing demographic and contextual bias relative to U.S. surgical workforce benchmarks.

Models analyzed:
- **DALL·E 3** (OpenAI)
- **ImageFX** (Google)
- **FLUX.1-dev** (OpenArt)

---

## 📂 Repository Structure

```
📁 Artificial-Identities/
│
├── data analysis/
│   ├── chi_square_trend.py           # Chi-square test and trend analysis
│   └── significance.py               # Significance testing and visualization helpers
│
├── figures/
│   ├── dalle_results_figure.png      # Main visualization of demographic results
│   └── dalle_results_table.pdf       # Table summarizing comparative outputs
│
├── images/                           # All generated surgeon images (DALL·E 3, ImageFX, FLUX.1-dev)
│
├── results/
│   ├── chi_square_trends_results_r.csv
│   ├── dalle_results.csv
│   └── data_final.csv                # Cleaned dataset for statistical analysis
│
├── scripts/
│   ├── dalle.py                      # DALL·E 3 generation and prompt audit script
│   └── figures.py                    # Figure plotting and data visualization
│
└── README.md
```

---

## 🔬 Study Summary

- **Design:** Cross-sectional image audit  
- **Prompt:** `"surgeon"` (neutral input, default parameters)  
- **Models:** DALL·E 3, ImageFX, FLUX.1-dev  
- **Sample:** 100 images per model (n = 300 total)  
- **Annotations:**  
  - Gender, race/ethnicity, contextual cues (operating room, deformities, etc.)  
  - Three blinded raters (doctoral medical students)  
- **Analysis Tools:**  
  - RStudio (v4.2.1) for statistical evaluation  
  - Python (v3.11.1) for DALL·E 3 prompt audit and intersectionality matrix  

---

## 📊 Highlights

| Model | Female Surgeons | Persons of Color | Deformity Rate |
|--------|-----------------|------------------|----------------|
| **DALL·E 3** | 83% | 67% | 55% |
| **ImageFX** | 4% | 4% | 23% |
| **FLUX.1-dev** | 0% | 0% | 22% |

> DALL·E 3’s API automatically inserted demographic modifiers into neutral prompts (e.g., “female Asian surgeon”), revealing hidden alignment steering that affected both diversity and image fidelity.

---

## 💡 Key Insights

- Diffusion models differ dramatically in demographic portrayal under identical prompts.  
- Alignment mechanisms can overcorrect, improving diversity but introducing realism artifacts.  
- Transparent prompt reporting, fairness auditing, and labeling are essential for responsible use in healthcare imagery.  

---

## 📈 Citation

If you use this repository, please cite:

> Gorijavolu R, Shoyombo I, Boparai S, Cho A, O’Connell E, Madapati K, Mathur V, Applewhite M, Stey A, Celi L.  
> *Artificial Identities: Analyzing Bias in Diffusion Model-Generated Images of Surgeons.*  
> Johns Hopkins University / MIT Laboratory for Computational Physiology, 2025.

---

## ⚖️ Ethics and Data Use

This study used only AI-generated imagery and publicly available datasets.  
No human subjects or patient data were involved; IRB approval was not required.

---

## 🤝 Acknowledgments

Supported by:
- **Johns Hopkins ICTR** (T32TR004928)  
- **MIT Laboratory for Computational Physiology**  
- **Bridge2AI (OT2OD032701)**  

With special thanks to mentors **Anne Stey**, **Megan Applewhite**, and **Leo Celi**, and the ARGOS research group.

---

## 🔗 Links

- Repository: [ARGOS-Lab/Bias-in-Diffusion-Model-Generated-Images-of-Surgeons](https://github.com/ARGOS-Lab/Bias-in-Diffusion-Model-Generated-Images-of-Surgeons)

---

## 🧾 License

This project is licensed under the MIT License.

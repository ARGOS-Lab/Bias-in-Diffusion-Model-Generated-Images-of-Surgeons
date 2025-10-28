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
The work investigates how leading text-to-image diffusion systems represent professional identities—specifically surgeons—under neutral prompting, and compares outputs to real-world workforce demographics.

The study audits three major models:
- **DALL·E 3** (OpenAI)
- **ImageFX** (Google)
- **FLUX.1-dev** (OpenArt)

We identify significant disparities in demographic representation, operating context, and visual realism, highlighting how alignment and bias mitigation strategies can both improve inclusivity and introduce new distortions.

---

## 🔬 Research Questions

1. How do text-to-image models depict surgeons when given a neutral prompt (“surgeon”)?
2. Do generated demographics (gender, race) align with real U.S. surgical workforce statistics?
3. How do alignment or prompt-modification behaviors (e.g., in DALL·E 3) influence representational outcomes?
4. What trade-offs exist between fairness, realism, and authenticity in generative medical imagery?

---

## ⚙️ Methods Summary

- **Design:** Cross-sectional evaluation  
- **Prompt:** `"surgeon"` (neutral, default settings)  
- **Models Evaluated:** DALL·E 3, ImageFX, OpenArt FLUX.1-dev  
- **Sample Size:** 100 images per model (n = 300 total)  
- **Annotation:**  
  - Attributes: Gender, race/ethnicity, hair/eye color, operating context, deformities  
  - Annotators: 3 blinded medical doctoral students  
- **Statistical Analysis:**  
  - Chi-square, Kruskal-Wallis, and Fleiss’ Kappa (RStudio v4.2.1)  
  - Follow-up DALL·E 3 audit: 250 API calls, prompt parsing (Python v3.11.1)

---

## 📊 Results Summary

- **DALL·E 3**: Overrepresented *female* (83%) and *people-of-color* (67%) surgeons  
- **ImageFX / FLUX.1-dev**: Overrepresented *male* and *White* surgeons  
- **Deformities:** Highest in DALL·E 3 (55%)  
- **Prompt Audit:** 75.8% of DALL·E 3’s internal prompts added gender/race modifiers, often favoring “female Asian surgeon” depictions  

While alignment strategies improved diversity, they also introduced higher artifact rates—highlighting tensions between *inclusivity* and *fidelity*.

---

## 🧰 Repository Contents

```
📁 Artificial-Identities/
│
├── data/
│   ├── generated_images/              # Sample or reference outputs (if available)
│   ├── annotations.csv                # Annotator results
│   └── prompt_audit_dalle3.csv        # Revised prompt logs
│
├── scripts/
│   ├── data_preprocessing.R
│   ├── interrater_reliability.R
│   ├── statistical_analysis.R
│   └── dalle3_prompt_audit.py
│
├── figures/
│   ├── demographics_comparison.png
│   ├── deformity_rates.png
│   └── intersectionality_heatmap.png
│
├── results/
│   ├── summary_statistics.csv
│   ├── chi_square_results.csv
│   └── kappa_scores.csv
│
├── README.md
└── LICENSE
```

---

## 💡 Key Findings

- Text-to-image models differ drastically in demographic representation, even under identical prompts.  
- DALL·E 3 actively modifies neutral prompts, introducing race and gender descriptors.  
- “Fairness” adjustments can improve diversity metrics but may degrade image quality.  
- Systematic auditing and transparency (e.g., model cards, labeling) are essential for ethical deployment in healthcare and education.

---

## 📈 Citation

If you use this repository, please cite:

> Gorijavolu R, Shoyombo I, Boparai S, Cho A, O’Connell E, Madapati K, Mathur V, Applewhite M, Stey A, Celi L.  
> *Artificial Identities: Analyzing Bias in Diffusion Model-Generated Images of Surgeons.*  
> Johns Hopkins University / MIT Laboratory for Computational Physiology, 2025.

---

## 📜 Ethics and Data Use

This project used only AI-generated imagery and publicly available data.  
No human or patient data were involved, and IRB approval was not required.

---

## 🤝 Acknowledgments

This research was supported by:
- **Johns Hopkins Institute for Clinical and Translational Research (ICTR)**  
- **MIT Laboratory for Computational Physiology**  
- **NIH NCATS (T32TR004928)**  
- **Bridge2AI (OT2OD032701)**  

We thank **Anne Stey**, **Megan Applewhite**, and **Leo Celi** for mentorship, and the ARGOS team for contributions to annotation and statistical validation.

---

## 🔗 Links

- **Publication:** *(in preparation / under submission)*  
- **Code Repository:** [ARGOS-Lab/Bias-in-Diffusion-Model-Generated-Images-of-Surgeons](https://github.com/ARGOS-Lab/Bias-in-Diffusion-Model-Generated-Images-of-Surgeons)
- **ARGOS Research Group:** [https://argos-lab.org](https://argos-lab.org)

---

## 🧾 License

This project is licensed under the MIT License — see the `LICENSE` file for details.

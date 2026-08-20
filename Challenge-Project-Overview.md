# Forecasting Risk of Harmful Algal Blooms in Coastal Marine Ecosystems

**Company / Org:** Oregon State University, Socio-Environmental Analysis Lab  
**Challenge Advisor:** Jack Buckner, bucknejo@oregonstate.edu  
**AI Studio Coach:** Hrushikesh Shetty, hrushikesh.shetty@breakthroughtech.org   
**Program:** Break Through Tech AI Studio - Fall 2026

---

## 🏢 About Oregon State University

Oregon State University is a leading public research university focused on advancing knowledge in various fields, including environmental sciences. The Socio-Environmental Analysis Lab uses data analytics and machine learning to address pressing ecological challenges.

---

## 🎯 The Challenge

### Project Summary
In this project, you will use oceanographic data from the European Union's Copernicus Marine Service and machine learning classification models to forecast the risk of harmful algal bloom (HAB) events in coastal marine ecosystems. This will help the Socio-Environmental Analysis Lab at Oregon State University develop insurance and financial risk management tools for coastal and marine industries.

### Success Criteria
A globally deployable model that predicts HAB events from environmental data, together with an unbiased estimate of the model's skill when forecasting future events.

### Project Milestones
Use these milestones to guide your work. Your team will create a **GitHub Projects board** to track tasks within each milestone.

| Month | Milestone | Key Activities |
|-------|-----------|----------------|
| **September** | Data understanding | Explore the event dataset and document the temporal and geographic distribution of harmful algae events and their impacts on humans and ecosystems. |
|               | Feature engineering | Calculate statistics from the Copernicus Marine data to use as predictors in the ML models, including the mean, 95th percentile, and variance of ocean variables over the affected area. |
|               | Create model-building dataset | Create a processed dataset for model training that includes the target events from HAEDAT and synthetic non-events. Pair these events with the engineered features from the Copernicus Marine data. Separate the dataset into a training set used to build and experiment with models and a validation set to test the model's performance on unseen data. |
| **October** | Model development | Train a baseline model, then experiment with algorithms and additional features. |
|             | Model testing | Build a leave-future-out cross-validation pipeline to run on the training data for model tuning and iteration. Avoid using the validation data at this stage. |
| **November** | Model evaluation | Test the model on the unseen validation dataset and compute final performance metrics. |
|              | Presentation | Create the final presentation, including background on the economic impacts of harmful algae, the motivation behind the seasonal forecasting system, and key performance metrics that illustrate how the model addresses this need. |

> **Note for the team:** Please create a GitHub Projects board in this repository to break these milestones into weekly tasks. Go to the **Projects** tab → **New project** → Choose **Board** → Add columns for each month.


---

## 📊 Dataset

**Name and Source:**
1. [Harmful Algae Event Database (HAEDAT)](https://obis.org/dataset/62ddad25-2a19-485d-9bae-7eb3a40a71c5)
2. [Global Ocean Physics Analysis and Forecast](https://data.marine.copernicus.eu/products)
3. [Global Ocean Biogeochemistry Analysis and Forecast](https://data.marine.copernicus.eu/products)

**Format:** CSV and netcdf
**Size:** 5 GB to 10 GB  
**Location:**
You can find a copy of the HAEDAT database in the `data/raw` directory of this GitHub repository. You will access the global ocean data products using the Copernicus Marine Toolbox API, which has both a command line and a Python interface. The `copernicusmarine` directory provides instructions on how to use the Copernicus Marine Toolbox along with examples of basic usage.

### Key Details
- Numerical, quantitative, time series, geospatial, and remote sensing data provided in CSV/TSV and Parquet formats. Sources include internal lab datasets and the Copernicus Marine Service.
- Please see the `copernicusmarine` subdirectory for a brief tutorial on loading Copernicus Marine Toolbox data through the Python API. Detailed documentation can be found [here](https://toolbox-docs.marine.copernicus.eu/en/stable/python-interface.html).

---

## 🛠️ Suggested Approach

**ML Problem Type:** Classification, time series analysis, geospatial analysis

**Recommended Libraries:**
- scikit-learn
- pandas
- xarray
- copernicusmarine
- matplotlib

**Validation Strategy:** Leave-future-out cross-validation

**Evaluation Metrics:**
- Precision-recall curves
- F1 score

---

## 📚 Resources to Get Started

The following resources will help your team understand the problem space and potential technical approaches for this project:

**Background Reading:**
- Brenckman et al. 2025, "A Review of Harmful Algal Blooms: Causes, Effects, Monitoring, and Prevention Methods" (see the `literature` folder).
- [National Oceanic and Atmospheric Administration on the economic impacts of harmful algae](https://coastalscience.noaa.gov/news/total-economic-impact-of-2018-red-tide-now-estimated-at-2-7b/).

**Technical Tutorials:**
- [Tutorial on using the copernicusmarine Python library for data acquisition and visualization](https://help.marine.copernicus.eu/en/articles/4854800-how-to-open-and-visualize-copernicus-marine-data-using-python)
- [Tutorial for leave-future-out cross-validation](https://towardsdatascience.com/how-to-cross-validation-with-time-series-data-9802a06272c6/)
- [Tutorial for cross-validation on spatial data](https://towardsdatascience.com/spatial-cross-validation-using-scikit-learn-74cb8ffe0ab9/)

**Other:**
- [Ocean OS, a startup working in this space](https://www.oceanos.earth/)

---

## 🤝 How We'll Work Together

**Check-ins:** During our biweekly 45-min AI Studio Lab Section meeting block (2nd and 4th week of every month)   
**Communication:** Email: bucknejo@oregonstate.edu   
**Response time:** Within 48 hours on weekdays   
**Recommended Tools:**
- **Coding:** Google Colab
- **Collaboration:** GitHub, Notion
- **Virtual Meetings:** Zoom, Google Meet

---

## 🚀 Getting Started

1. **Review this overview document** and note any questions for our first meeting
2. **Begin reviewing the dataset** using the link above
3. **Read the GitHub Projects documentation** [here](https://docs.github.com/en/issues/planning-and-tracking-with-projects/learning-about-projects/about-projects)

I'm excited to work with you!

---

## ❓ Questions?

Please bring any questions to our first meeting during the week of August 24th (Break Through Tech's Bridge to Studio - Session B).

---

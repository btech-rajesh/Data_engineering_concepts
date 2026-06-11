## MLflow End-to-End Example — Documentation

Overview
- **Purpose:** Companion documentation for `notebooks/mlflow-end-to-end-example.ipynb`. This file provides a clear, runnable sequence of steps, commands, and relevant UI screenshots to reproduce the notebook workflow.
- **Notebook file:** [notebooks/mlflow-end-to-end-example.ipynb](notebooks/mlflow-end-to-end-example.ipynb)

Prerequisites
- Follow the environment setup guides in this repo: [setup-windows.md](setup-windows.md), [setup-ubuntu.md](setup-ubuntu.md), [setup-macos.md](setup-macos.md).
- Python packages used by the notebook: `pandas`, `seaborn`, `matplotlib`, `scikit-learn`, `mlflow`, `xgboost`, `hyperopt`, `flask`. The notebook installs some packages via `%pip` when run in Databricks.
- Databricks workspace + cluster running an ML LTS runtime (notebook recommends Databricks Runtime 15.4 LTS ML or newer).

Quick start (Databricks)
1. Launch Databricks workspace and create a cluster. Use an ML LTS runtime, then attach the cluster to the notebook.
2. Import the notebook: `notebooks/mlflow-end-to-end-example.ipynb` and open it in Databricks.
3. Run cells top-to-bottom. If the notebook prompts to install packages, allow the `%pip` installs.

Quick start (local / script)
1. Install dependencies in a venv (example):

```bash
python -m venv .venv
.venv\Scripts\activate
pip install pandas seaborn matplotlib scikit-learn mlflow xgboost hyperopt flask
```

2. If running the script version `notebooks/mlflow-end-to-end-example.py`, ensure dataset paths are local (the notebook uses `/databricks-datasets/...`). Download the UCI wine CSVs and update paths in the script.

Repository layout (relevant files)
- `notebooks/mlflow-end-to-end-example.ipynb` — Primary tutorial notebook.
- `notebooks/mlflow-end-to-end-example.py` — Script form of the notebook.
- `screenshots/` — UI screenshots used in this doc.
- `terraform/` — IaC used to provision Azure resources for the tutorial.

Step-by-step walkthrough (ordered, with images)

1) Read and merge the data
- Actions: load `winequality-white.csv` and `winequality-red.csv`, create `is_red` column, concat and rename columns.
- Notebook cells: first read/concat cells in the notebook.

2) Visualize data (plots)
- Actions: histogram of `quality`, convert to binary (>=7), boxplots for features vs quality.
- Relevant cell(s): Seaborn/Matplotlib visualization cells.
- Example visualization image:

![Data distribution and boxplots](screenshots/Screenshot%202026-02-18%20153653.png)

3) Preprocess and split
- Actions: check missing values, set `high_quality = (data.quality >= 7).astype(int)`, split into train/val/test with `train_test_split`.

4) Baseline model training and MLflow logging
- Actions: Train a `RandomForestClassifier`, compute AUC, and log params/metrics and model with MLflow (pyfunc wrapper used).
- Key MLflow calls: `mlflow.start_run`, `mlflow.log_param`, `mlflow.log_metric`, `mlflow.pyfunc.log_model`.
- MLflow runs sidebar (example):

![MLflow runs view](screenshots/Screenshot%202026-02-18%20153701.png)

5) Register baseline model in MLflow Model Registry
- Actions: call `mlflow.register_model(...)`, then promote by setting alias `Production` with `MlflowClient().set_registered_model_alias(...)`.
- Models page example:

![Models page](screenshots/Screenshot%202026-02-18%20153711.png)

6) Hyperparameter sweep (XGBoost + Hyperopt)
- Actions: install `xgboost` and `hyperopt`, define `search_space`, run `fmin` with `SparkTrials`, and use MLflow autologging to record runs.
- Sweep results example (sort by `auc`):

![Hyperparameter sweep results](screenshots/Screenshot%202026-02-18%20153729.png)

7) Promote best run to production
- Actions: identify best run with `mlflow.search_runs(order_by=['metrics.auc DESC'])`, `mlflow.register_model(...)`, archive old alias and set new `Production` alias.

8) Batch inference with Spark UDF
- Actions: persist a sample DataFrame to a Delta table, load the registered model via `mlflow.pyfunc.spark_udf(spark, "models:/<name>@production")`, and apply to Delta.
- Delta/UDF example:

![Delta table / UDF results](screenshots/Screenshot%202026-02-18%20153748.png)

9) Model serving (optional)
- Actions: register model, create serving endpoint in Databricks UI (Serving → Create serving endpoint → select model/version), generate a Databricks token and call the endpoint with a JSON body.
- Example serving UI / invocation screenshot:

![Serving endpoint example](screenshots/Screenshot%202026-02-18%20153935.png)

Note: the notebook contains an example `score_model` helper that posts JSON to the serving endpoint; set `DATABRICKS_TOKEN` in environment before calling.

Using screenshots
- All example images are in `screenshots/`. Filenames have spaces — percent-encode spaces when embedding in Markdown (e.g., `Screenshot%202026-02-18%20153701.png`).
- Suggested placement: put visualization images next to plotting steps and UI screenshots next to MLflow/Models/Serving sections.

Run checklist (Databricks)
- Create cluster (ML LTS runtime) and attach notebook.
- Install notebook `%pip` dependencies if requested by the notebook.
- Replace placeholder values in notebook cells (for example, `table_path = "/workspace/<your_user>/delta/wine_data"`).

Run checklist (local/script)
- Ensure dependencies installed in a Python environment.
- Replace Databricks-specific dataset paths with local CSV paths.
- If using MLflow server/registry locally, configure `MLFLOW_TRACKING_URI` and `MLFLOW_TRACKING_USERNAME/PASSWORD` as needed.

Terraform / infra notes
- Use the `terraform/` folder to provision Azure resources. Follow the main `README.md` instructions: `terraform init`, `terraform plan -out terraform.plan`, `terraform apply terraform.plan`, and `terraform destroy` when done.

Helpful tips
- Replace any placeholder usernames or paths before running (e.g., `table_path = "/workspace/your_user/delta/wine_data"`).
- If you hit Model Registry permissions errors, ensure the model name is unique, or check Databricks RBAC settings.

Next options I can do for you
- Embed more plot PNGs from `screenshots/` inline at specific notebook locations.
- Convert this `documentation.md` into the main `README.md` or generate a small MkDocs site.

---
Generated to accompany `notebooks/mlflow-end-to-end-example.ipynb` and the project's setup guides.

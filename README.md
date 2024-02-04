# Finetune MEDIAR project for worms detection
## Content
 - code
   - inference - code part for inference
   - train - code part for model training
 - data
   - Data for testing - https://drive.google.com/file/d/1VPFhFB-MKogfRdc63wlM-hVk-8CMi94d/view?usp=sharing
   - Load train data from: https://drive.google.com/file/d/1_P6CzW-OnISIimxYtiKME_AKz-RF5zhh/view?usp=sharing
   - result_example.png - result examples
 - models - weights of trained models
   - model phase 1 - https://drive.google.com/file/d/1ctmXVRPG7e2ZJ1JqrIEN5t-ZmyK5KXTl/view?usp=sharing
   - model phase 2 - https://drive.google.com/file/d/1OGp-rb8wOZz8JKHZsjm7957z3OeyK6lA/view?usp=sharing
 - util_workbook_MEDIAR_worms.ipynb - never mind, but if you have some problem you can try it on colab

## Install project
### Clone MEDIAR github repo
git clone https://github.com/Lee-Gihun/MEDIAR.git

cd MEDIAR

### Clone MEDIAR_worms github repo
git clone https://github.com/YasminaSiddiki/MEDIAR_worms.git

### Replace files: generate_mapping.py, Trainer.py from MEDIAR_worms to MEDIAR

### Install dependencies
pip install -r requirements.txt

pip install segmentation-models-pytorch==0.3.1

pip install wandb

wandb off

## Train models
### Prepare data
python MEDIAR_worms/code/train/prepare_data.py your_data.zip

### Generate mapping
python MEDIAR_worms/code/train/generate_mapping.py --root=data/dataset

### Load weights for fine-tuning
mkdir weights

mkdir weights/pretrained

gdown https://drive.google.com/uc?id=1v5tYYJDqiwTn_mV0KyX5UEonlViSNx4i -O weights/pretrained/phase1.pth

gdown https://drive.google.com/uc?id=1NHDaYvsYz3G0OCqzegT-bkNcly2clPGR -O weights/pretrained/phase2.pth

### Train model
python main.py --config_path=MEDIAR_worms/code/train/your_configure.json

for phase1/phase2 use finetuning1.json/finetuning2.json

## Model inference
### If your data is in .png, convert to .tiff
python MEDIAR_worms/code/inference/transform_data_png_to_tiff.py --input_dir=dir_with_png --output_dir=output_dir

### Make prediction
python MEDIAR_worms/code/inference/inference.py --input_dir=dir_with_tiff --output_dir=output_dir

## Results
Our result after fine-tuning: 
precession: 1
recall: 0.79

### phase1
prediction examples:
![My Image](data/result_example_phase1.png)

### phase2
prediction examples:
![My Image](data/result_example_phase2.png)

### ensemble
prediction examples:
![My Image](data/result_example_ensemble.png)

model=model_se_resnext50_32_4d_WP12_WD_e-1
gpu=0
fold=0
conf=./conf/${model}.py

python -m src.cnn.main train ${conf} --fold ${fold} --gpu ${gpu}

model=model_se_resnext101_32_4d_WP3_WD_e-1
gpu=1
fold=0
conf=./conf/${model}.py

python -m src.cnn.main train ${conf} --fold ${fold} --gpu ${gpu}
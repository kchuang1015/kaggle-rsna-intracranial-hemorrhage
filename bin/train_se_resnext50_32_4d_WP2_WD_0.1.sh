model=model_se_resnext50_32_4d_WP2_WD_0.1
gpu=0
fold=0
conf=./conf/${model}.py

python -m src.cnn.main train ${conf} --fold ${fold} --gpu ${gpu}

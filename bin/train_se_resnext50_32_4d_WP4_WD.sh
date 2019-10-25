model=model_se_resnext50_32_4d_WP4_WD
gpu=1
fold=0
conf=./conf/${model}.py

python -m src.cnn.main train ${conf} --fold ${fold} --gpu ${gpu}

model=model_SqueezeNet1_1_WP8_WD_e-1
gpu=4
fold=0
conf=./conf/${model}.py

python -m src.cnn.main train ${conf} --fold ${fold} --gpu ${gpu}

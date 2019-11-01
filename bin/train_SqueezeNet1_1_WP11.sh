model=model_SqueezeNet1_1_WP11
gpu=5
fold=0
conf=./conf/${model}.py

python -m src.cnn.main train ${conf} --fold ${fold} --gpu ${gpu}

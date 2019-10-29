model=model_inceptionresnetv2_WP6_WD_0.1
gpu=4
fold=0
conf=./conf/${model}.py

python -m src.cnn.main train ${conf} --fold ${fold} --gpu ${gpu}

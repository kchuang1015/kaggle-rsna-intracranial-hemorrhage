model=model_inceptionresnetv2_WP8_WD_0.1
gpu=7
fold=0
conf=./conf/${model}.py

python -m src.cnn.main train ${conf} --fold ${fold} --gpu ${gpu}

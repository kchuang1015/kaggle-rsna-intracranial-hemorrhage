model=model_inceptionresnetv2_WP2_WD_FL2
gpu=3
fold=0
conf=./conf/${model}.py

python -m src.cnn.main train ${conf} --fold ${fold} --gpu ${gpu}

model=model_inceptionresnetv2_WP2_WD_FL3
gpu=4
fold=0
conf=./conf/${model}.py

python -m src.cnn.main train ${conf} --fold ${fold} --gpu ${gpu}

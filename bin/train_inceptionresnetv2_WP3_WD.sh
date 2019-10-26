model=model_inceptionresnetv2_WP3_WD
gpu=1
fold=0
conf=./conf/${model}.py

python -m src.cnn.main train ${conf} --fold ${fold} --gpu ${gpu}

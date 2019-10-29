model=model_inceptionresnetv2_WP9_WD
gpu=5
fold=0
conf=./conf/${model}.py

python -m src.cnn.main train ${conf} --fold ${fold} --gpu ${gpu}

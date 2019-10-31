model=model_inceptionresnetv2_WP2_WD_FL5
gpu=7
fold=0
conf=./conf/${model}.py

python -m src.cnn.main train ${conf} --fold ${fold} --gpu ${gpu}

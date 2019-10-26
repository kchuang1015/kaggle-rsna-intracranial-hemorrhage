model=model_inceptionresnetv2_WP2_WD_NPre
gpu=0
fold=0
conf=./conf/${model}.py

python -m src.cnn.main train ${conf} --fold ${fold} --gpu ${gpu}

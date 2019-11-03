model=model_inceptionresnetv2_WP12_WD_fold4
gpu=3
fold=4
conf=./conf/${model}.py

python -m src.cnn.main train ${conf} --fold ${fold} --gpu ${gpu}

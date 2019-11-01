model=model_inceptionresnetv2_WP11_WD_fold4
gpu=4
fold=4
conf=./conf/${model}.py

python -m src.cnn.main train ${conf} --fold ${fold} --gpu ${gpu}

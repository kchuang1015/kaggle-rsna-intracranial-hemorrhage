model=model_inceptionresnetv2_WP11_WD_fold3
gpu=3
fold=3
conf=./conf/${model}.py

python -m src.cnn.main train ${conf} --fold ${fold} --gpu ${gpu}

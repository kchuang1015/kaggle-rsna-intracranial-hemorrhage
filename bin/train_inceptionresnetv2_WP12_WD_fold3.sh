model=model_inceptionresnetv2_WP12_WD_fold3
gpu=2
fold=3
conf=./conf/${model}.py

python -m src.cnn.main train ${conf} --fold ${fold} --gpu ${gpu}

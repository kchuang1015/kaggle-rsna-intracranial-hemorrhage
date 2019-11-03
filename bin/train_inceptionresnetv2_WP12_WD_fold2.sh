model=model_inceptionresnetv2_WP12_WD_fold2
gpu=1
fold=2
conf=./conf/${model}.py

python -m src.cnn.main train ${conf} --fold ${fold} --gpu ${gpu}

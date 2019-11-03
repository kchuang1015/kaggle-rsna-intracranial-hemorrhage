model=model_inceptionresnetv2_WP12_WD_fold1
gpu=0
fold=1
conf=./conf/${model}.py

python -m src.cnn.main train ${conf} --fold ${fold} --gpu ${gpu}

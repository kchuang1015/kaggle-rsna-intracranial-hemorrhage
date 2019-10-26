model=model_pnasnet5large_WP6_WD
gpu=4
fold=0
conf=./conf/${model}.py

python -m src.cnn.main train ${conf} --fold ${fold} --gpu ${gpu}

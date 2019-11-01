model=model_pnasnet5large_WP11_WD_fold2
gpu=2
fold=2
conf=./conf/${model}.py

python -m src.cnn.main train ${conf} --fold ${fold} --gpu ${gpu}

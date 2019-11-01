model=model_pnasnet5large_WP11_WD_fold1
gpu=1
fold=1
conf=./conf/${model}.py

python -m src.cnn.main train ${conf} --fold ${fold} --gpu ${gpu}

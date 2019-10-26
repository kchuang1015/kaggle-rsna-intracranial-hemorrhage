model=model_pnasnet5large_WP4_WD_NPre_NPre
gpu=2
fold=0
conf=./conf/${model}.py

python -m src.cnn.main train ${conf} --fold ${fold} --gpu ${gpu}

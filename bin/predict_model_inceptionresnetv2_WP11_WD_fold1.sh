model=model_inceptionresnetv2_WP11_WD_fold1
gpu=1
fold=1
ep=4
tta=6
clip=1e-6
conf=./conf/${model}.py

snapshot=./model/${model}/fold${fold}_ep${ep}.pt
valid=./model/${model}/fold${fold}_ep${ep}_valid_tta${tta}.pkl
test=./model/${model}/fold${fold}_ep${ep}_test_tta${tta}.pkl
sub=./data/submission/${model}_fold${fold}_ep${ep}_test_tta${tta}.csv

python -m src.cnn.main test ${conf} --snapshot ${snapshot} --output ${test} --n-tta ${tta} --fold ${fold} --gpu ${gpu}
python -m src.postprocess.make_submission --input ${test} --output ${sub} --clip ${clip}
kaggle competitions submit rsna-intracranial-hemorrhage-detection -m "" -f ${sub}


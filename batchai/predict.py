import numpy as np
from sklearn.svm import OneClassSVM
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from azure.storage.blob import BlockBlobService
import pickle
import sys
import json
import datetime
import pandas as pd
import io

# query params
device = int(sys.argv[1])
tag = int(sys.argv[2])

# input/output params
config_file = sys.argv[3]
with open(config_file) as f:
    j = json.loads(f.read())

blob_account = j['blob_account']
blob_key = j['blob_key']
models_blob_container = j['models_blob_container']
data_blob_container = j['data_blob_container']
data_blob_name = j['data_blob']
predictions_blob_container = j['predictions_blob_container']

model_name = 'model_{0}_{1}'.format(device, tag)

blob_service = BlockBlobService(
    account_name=blob_account, account_key=blob_key)

# get data
data_blob = blob_service.get_blob_to_bytes(data_blob_container, data_blob_name)
data = pd.read_csv(io.BytesIO(data_blob.content))
data = data[(data['Device']==device) & (data['Tag']==tag)]
tss = data['TS']
vals = np.array(data['Value'])

# load model
model_blob = blob_service.get_blob_to_bytes(models_blob_container, model_name)
pipe = pickle.loads(model_blob.content)

# predict
preds = pipe.predict(vals.reshape(-1, 1))
preds = np.where(preds == 1, 0, 1) # 1 indicates an anomaly, 0 otherwise

# csv results
res = pd.DataFrame({'TS':tss,
                    'Device': np.repeat(device, len(preds)),
                    'Tag': np.repeat(tag, len(preds)),
                    'Val': vals,
                    'Prediction': preds})
res = res[['TS', 'Device', 'Tag', 'Val', 'Prediction']]

res_file_name = 'preds_{0}_{1}_{2}'.format(device,
                                               tag,
                                               datetime.datetime.now().strftime('%y%m%d%H%M%S')
                                               )

# save predictions
blob_service.create_blob_from_text(
    predictions_blob_container, res_file_name, res.to_csv(index=None))

from mp_api.client import MPRester
import pandas as pd
#import matplotlib.pyplot as plt

#get data from Materials Project API
mp_id_to_task_id = {}
with MPRester("HEKWFDp0sGOgT9GPRHDQGdPfhEyLnqRL") as mpr:
    summary_docs = mpr.materials.summary.search(material_ids=["mp-149", "mp-13", "mp-22526"],
                                                fields = ["density", "band_gap", "formation_energy_per_atom", "volume"])
    
#converts to list and removes 'fields_not_requested'
data = []
for doc in summary_docs:
    listObj = doc.model_dump()
    listObj.pop('fields_not_requested')
    data.append(listObj)
#print(f'this is data: {data}')

#converts to dataframe
dataFrame = pd.DataFrame(data)
#print(f'this is dataFrame: {dataFrame}')

#removes empty rows, duplicates and anomalous materials
dataFrame = dataFrame.dropna()
dataFrame = dataFrame.drop_duplicates()
dataFrame = dataFrame[(dataFrame['density'] > 0) & (dataFrame['density'] < 20)]
dataFrame = dataFrame[(dataFrame['formation_energy_per_atom'] > -10) & (dataFrame['formation_energy_per_atom'] < 2)]
dataFrame = dataFrame[(dataFrame['volume'] > 5) & (dataFrame['volume'] < 10000)]
dataFrame = dataFrame[(dataFrame['band_gap'] >= 0) & (dataFrame['band_gap'] < 12)]

#description = dataFrame.describe()
#print(description)
#dataFrame["volume"].hist()
#plt.savefig('vloumePlot.png')

#Standardises all values for machine learning. To standardize a dataset means to scale all of the values in the dataset such that the mean value is 0 and the standard deviation is 1.
dataFrame_scaled = (dataFrame-dataFrame.mean())/dataFrame.std()
print(dataFrame_scaled)
from mp_api.client import MPRester
import pandas as pd
import matplotlib.pyplot as plt

#get data from Materials Project API
mp_id_to_task_id = {}
with MPRester("HEKWFDp0sGOgT9GPRHDQGdPfhEyLnqRL") as mpr:
    summary_docs = mpr.materials.summary.search(material_ids=["mp-149", "mp-148"],
                                                fields = ["density", "nsites", "nelements", "volume", "structure", "energy_per_atom", "universal_anisotropy", "homogeneous_poisson"])

#print(summary_docs)    
#converts to list and removes 'fields_not_requested'
data = []
for doc in summary_docs:
    #print(f'this is doc: {doc}')
    listObj = doc.model_dump()
    #Also gets matrix from structure and removes structure'
    matrix = listObj["structure"]["lattice"]["matrix"]
    # Flatten it into 9 values: [m00, m01, m02, m10, m11, m12, m20, m21, m22]
    flat_matrix = []
    for i in matrix:
        for j in i:
            flat_matrix.append(j)
    # Add each flattened value as its own key
    for i, val in enumerate(flat_matrix):
        listObj[f"matrix_{i}"] = val
    listObj.pop('fields_not_requested')
    listObj.pop('structure')
    data.append(listObj)

#converts to dataframe
dataFrame = pd.DataFrame(data)
print(f'this is dataFrame: {dataFrame}')

dataFrame.to_csv("standardised_data.csv", index=False)

#removes empty rows, duplicates and anomalous materials
dataFrame = dataFrame.dropna()
dataFrame = dataFrame.drop_duplicates()

#description = dataFrame.describe()
#print(description)
#dataFrame["volume"].hist()
#plt.savefig('vloumePlot.png')

#Standardises all values for machine learning. To standardize a dataset means to scale all of the values in the dataset such that the mean value is 0 and the standard deviation is 1.
dataFrame_scaled = (dataFrame-dataFrame.mean())/dataFrame.std()
#print(dataFrame_scaled)

from mp_api.client import MPRester


with MPRester("HEKWFDp0sGOgT9GPRHDQGdPfhEyLnqRL") as mpr:
    docs = mpr.materials.summary.search(
        material_ids=["mp-149", "mp-13", "mp-22526"]
    )
    print(docs)
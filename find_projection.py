from __future__ import print_function
import os
from sqlalchemy import create_engine
from epsg import Registry, schema

db = 'epsg-registry-cache.db'
if os.path.exists(db):
    engine = create_engine('sqlite:///epsg-registry-cache.db')
    registry = Registry(engine)
else:
    engine = create_engine('sqlite:///epsg-registry-cache.db')
    registry = Registry(engine)
    print("Downloading EPSG registry, this takes a while...")
    registry.init()

west, south, east, north = -61.83, 11.97, -61.57, 12.26

crss = registry.session.query(schema.ProjectedCRS).join(
    schema.ProjectedCRS.domainOfValidity).filter(
        schema.AreaOfUse.westBoundLongitude <= west).filter(
        schema.AreaOfUse.southBoundLatitude <= south).filter(
        schema.AreaOfUse.eastBoundLongitude >= east).filter(
        schema.AreaOfUse.northBoundLatitude >= north).all()

for crs in crss:
    print("-------------------------------------------------------------")
    print(crs.name, "({})".format(crs.identifier))
    print(crs.scope)
    print(crs.remarks)
    print(crs.domainOfValidity.description)

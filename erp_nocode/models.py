from dataclasses import dataclass, field
from datetime import datetime

from bson import ObjectId

from util.erp_utility_collection import MAIN_COLLECTION
from util.mongo_orm.models import BaseModel

@dataclass
class Business(BaseModel):
    _id: ObjectId = field(default_factory=ObjectId)
    collection_name: str = MAIN_COLLECTION.HB_MODULES_BUSINESSES
    businessId: str = None
    name: str = None
    description: str = None
    createdAt: datetime = datetime.now()

@dataclass
class ModuleField(BaseModel):
    _id: ObjectId = field(default_factory=ObjectId)
    collection_name: str = MAIN_COLLECTION.HB_MODULES_CONFIG_DATA
    businessId: str = None
    module: str = None
    dynamicFields: list = field(default_factory=list) 
    createdAt: datetime = datetime.now()

@dataclass
class Menu(BaseModel):
    _id: ObjectId = field(default_factory=ObjectId)
    collection_name: str = MAIN_COLLECTION.HB_MENU_CONFIG_DATA
    name :str = None
    menuOrder:str = None
    mapModules: [] = None
    created_at :datetime = None
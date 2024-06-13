from dataclasses import dataclass, field
from datetime import datetime

from bson import ObjectId

from util.erp_utility_collection import MAIN_COLLECTION
from util.mongo_orm.models import BaseModel

DESIGN_NAMES = {
    "HADR": {"description": "Header", "template_path": "designs/header.html"},
    "BTN": {"description": "Button", "template_path": "designs/button.html"},
    "INFD": {"description": "Input Field", "template_path": "designs/input_field.html"},
    "CHKB": {"description": "Check Box", "template_path": "designs/check_box.html"},
}

@dataclass
class Business(BaseModel):
    _id: ObjectId = field(default_factory=ObjectId)
    collection_name: str = MAIN_COLLECTION.BUSINESS_ENTITY
    businessId: str = None
    name: str = None
    description: str = None
    createdAt: datetime = datetime.now()


@dataclass
class CustomField(BaseModel):
    _id: ObjectId = field(default_factory=ObjectId)
    collection_name: str = MAIN_COLLECTION.BUSINESS_CONFIG_DATA
    businessId: str = None
    module: str = None
    dynamicFields: list = field(default_factory=list) 
    createdAt: datetime = datetime.now()

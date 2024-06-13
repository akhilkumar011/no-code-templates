from typing import List
from decimal import Decimal
from pydantic import BaseModel, Field


class ErpContact(BaseModel):
    name: str
    primaryType: str = 'customer'
    accountNumber: str
    pan: str = None
    gstin: str = None
    mobile: str
    email: str
    status: str = 'COAC'


class ErpTransaction(BaseModel):
    date: str
    contactCode: str
    contactName: str
    amount: Decimal
    txnType: str
    typeCode: str
    taxType: str


class ErpTransactionLine(BaseModel):
    itemCode: str
    itemName: str
    qty: Decimal
    unitPrice: Decimal
    gstRate: Decimal
    amount: Decimal


class ErpInvoice(ErpTransaction):
    dueDate: str
    lineItems: List[ErpTransactionLine] = Field(default_factory=list)


class ErpAddress(BaseModel):
    address1: str
    address2: str
    city: str
    state: str
    pincode: str
    country: str


# @dataclass
class ErpListMasterRequest(BaseModel):
    page: int
    limit: int
    entityType: str
    searchFor: str = None
    employee: bool = None
    vendor: bool = None
    customer: bool = None
    agent: bool = None
    fromDate: str = None
    contactId: int = None
    tagContactId: int = None
    txnType: str = None


# @dataclass
class ErpListTxnRequest(BaseModel):
    page: int
    limit: int
    searchFor: str = None
    startDate: str = None
    endDate: str = None
    hbCode: str = None
    txnType: str = None
    tagContactId: int = None


# @dataclass
class ErpViewTxnRequest(BaseModel):
    txnNumber: str
    txnType: str


# @dataclass
class ErpViewMasterRequest(BaseModel):
    entityCodeOrName: str
    entityType: str


class ErpTransactionRequest(BaseModel):
    invoiceList: List[ErpInvoice] = Field(default_factory=list)
    # billList: List['ApiBaseTxnEntityTO'] = Field(default_factory=list)
    # journalList: List['ApiBaseTxnEntityTO'] = Field(default_factory=list)
    # expenseList: List['ApiBaseTxnEntityTO'] = Field(default_factory=list)
    # receiveMoneyList: List['ApiBaseTxnEntityTO'] = Field(default_factory=list)
    # spendMoneyList: List['ApiBaseTxnEntityTO'] = Field(default_factory=list)
    # creditNoteList: List['ApiBaseTxnEntityTO'] = Field(default_factory=list)
    # debitNoteList: List['ApiBaseTxnEntityTO'] = Field(default_factory=list)
    # txnPaymentReceiptList: List['ApiTxnPaymentTO'] = Field(default_factory=list)
    # quoteList: List['ApiBaseTxnEntityTO'] = Field(default_factory=list)
    # salesOrderList: List['ApiBaseTxnEntityTO'] = Field(default_factory=list)
    # purchaseOrderList: List['ApiBaseTxnEntityTO'] = Field(default_factory=list)
    # goodsReceiptNoteList: List['ApiBaseTxnEntityTO'] = Field(default_factory=list)


class ErpMasterRequest(BaseModel):
    # contactGroups: List['ContactGroupTO'] = Field(default_factory=list)
    # designations: List['ContactRoleTO'] = Field(default_factory=list)
    contactList: List[ErpContact] = Field(default_factory=list)
    # accountList: List['ApiAccountTO'] = Field(default_factory=list)
    # itemList: List['ApiItemTO'] = Field(default_factory=list)
    # bankAccountList: List['ApiBankTO'] = Field(default_factory=list)
    # branchList: List['ApiTrackingCategoriesOptionTO'] = Field(default_factory=list)
    # categoryList: List['ApiTrackingCategoriesOptionTO'] = Field(default_factory=list)
    # accountGroupList: List['ApiAccountSubTypeTO'] = Field(default_factory=list)
    # proGroupList: List['ApiProGroupTO'] = Field(default_factory=list)
    # proCategoryList: List['ApiProCategoryTO'] = Field(default_factory=list)
    # proAttributeList: List['ApiProAttributeTO'] = Field(default_factory=list)
    # proInventoryList: List['ApiProInventoryTO'] = Field(default_factory=list)
    # proInventoryBatchList: List['ApiProBatchTO'] = Field(default_factory=list)

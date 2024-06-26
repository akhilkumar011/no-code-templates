class ACT_COLLECTION:
    TXN_COMMON_DATA = "txn_common_data"
    TXN_COMMON_DATA_LINE = "txn_common_data_line"
    TXN_JOURNAL_ENTRY = "txn_journal_entry"
    MASTER_CHART_ACCOUNTS = "master_chart_of_accounts"
    TXN_INVENTORY_MOVEMENTS = "txn_inventory_movements"

class DATA_CODE:
    TXN_COMMON_DATA = "T-DATA-01"
    TXN_COMMON_DATA_LINE = "T-DATA-02"
    TXN_COMMON_DATA_LINE_WISE = "T-DATA-03"
    TXN_JOURNAL_ENTRY = "T-DATA-04"
    TXN_COMMON_DATA_JOURNAL_ENTRY = "T-DATA-05"
    MASTER_CHART_ACCOUNTS = "T-DATA-06"
    TXN_STOCK_MOVEMENT = "T-DATA-07"
    TXN_STOCK_VALUATION_AVG = "T-DATA-08"
    TXN_STOCK_VALUATION_FIFO = "T-DATA-09"


ACT_TXN_NAME = {}

ACT_TXN_NAME.update({
    "INV": "Invoice",
    "BILL": "Bill",
    "SCN": "Sales Credit Note",
    "PCN": "Purchase Debit Note",
    "RDP": "Direct Payment",
    "RBI": "Bill Payment",
    "SDP": "Direct Receipt",
    "SBI": "Invoice Receipt",
    "ROP": "Ad-hoc Receipt",
    "SOP": "Over Payment",
    "SOT": "Other Payment",
    "SOA": "On Account Payment",
    "ROA": "On Account Receipt",
    "ROT": "Other Receipt",
    "TRFM": "Transfer Money",
    "EXPC": "Expense",
    "MJ": "Journal",
    "STJL": "Manufacturing Journal",
    "ACR": "Allocate Credit",
    "BACR": "Bulk Allocate Credit",
    "RPP": "Advance Receipt",
    "OPBL": "Opening Balance Inventory",
    "PYMT": "Payment-Receipt Txn-wise",
    "SDN": "Sales Debit Note",
    "BCN": "Bill Credit Note",
    "PGRN": "Purchase GRN",
    "PR": "Purchase Requisition",
    "TRO": "Transfer Order",
    "IO": "Indent Order",
    "PO": "Purchase Order",
    "SO": "Sales Order",
    "QU": "Quote",
    "DCL": "Delivery Challan",
    "MRN": "MRN",
    "MTN": "MTN"
})

TXN_STATUS_ENUM = {
    "INDT": "Draft",
    "INAP": "Awaiting Receipt",
    "PINAP": "Approved",
    "INPD": "Received",
    "INPN": "Pending Approval",
    "INVD": "Void",
    "SCNDT": "Draft",
    "SCNAP": "Awaiting Settlement",
    "SCNPN": "Pending Approval",
    "SCNPD": "Settled",
    "SCNVD": "Void",
    "BDFT": "Draft",
    "BAPP": "Awaiting Payment",
    "BPN": "Pending Approval",
    "BPD": "Paid",
    "BVD": "Void",
    "MJDT": "Draft",
    "MJPT": "Posted",
    "MJVD": "Voided",
    "PMTRE": "Payment Received",
    "PMTVD": "Void Payment",
    "SMDT": "Draft",
    "SMAP": "Awaiting Settlement",
    "SMAA": "Pending Approval",
    "SMPD": "Settled",
    "SMVD": "Void",
    "RMDT": "Draft",
    "RMAP": "Awaiting Settlement",
    "RMPN": "Pending Approval",
    "RMPD": "Settled",
    "RMVD": "Void",
    "PCNDT": "Draft",
    "PCNAP": "Awaiting Settlement",
    "PCNPN": "Submit for Approval",
    "PCNPD": "Settled",
    "PCNVD": "Void",
    "DCDT": "Draft",
    "DCPD": "Pending Approval",
    "DCAP": "Approved",
    "DCPA": "Partially Adjusted",
    "DCPR": "Partially Reversed",
    "DCPI": "Partially Invoiced",
    "DCFA": "Fully Adjusted",
    "DCRV": "Fully Reversed",
    "DCIN": "Fully Invoiced",
    "DCVD": "Voided",
    "QUDT": "Draft",
    "QUAP": "Accepted",
    "QUPD": "Pending Approval",
    "QUST": "Sent",
    "QUVD": "Voided",
    "QUDC": "Declined",
    "QUIN": "Invoiced",
    "QUSO": "Sales Ordered",
    "QUDL": "Deleted",
    "RIDT": "Draft",
    "RIAA": "Pending Approval",
    "RIAP": "Approved",
    "RIDL": "Deleted",
    "RBDT": "Draft",
    "RBAA": "Pending Approval",
    "RBAP": "Approved",
    "RBDL": "Deleted",
    "PODT": "Draft",
    "POPD": "Submit for Approval",
    "POPB": "Partially Billed",
    "POGN": "Fully GRN",
    "PODL": "Deleted",
    "POVD": "Voided",
    "POAP": "Approved",
    "IODT": "Draft",
    "IOPD": "Submit for Approval",
    "IODL": "Deleted",
    "IOVD": "Voided",
    "IOAP": "Approved",
    "ECDT": "Draft",
    "ECPD": "Paid",
    "ECVD": "Voided",
    "ECAP": "Awaiting Authorization",
    "ECDC": "Declined",
    "ECDL": "Deleted",
    "ECAU": "Awaiting Payment",
    "ECAR": "Archived",
    "ECSP": "Submit for Approval",
    "CMDT": "Draft",
    "CMPD": "Paid",
    "CMVD": "Voided",
    "CMAP": "Approved",
    "CMDC": "Declined",
    "CMDL": "Deleted",
    "CMAU": "Awaiting Payment",
    "CMAR": "Archived",
    "CMSP": "Submit for Approval",
    "ACT": "Registered",
    "PND": "Pending for Self Approval",
    "DACT": "Deregistered",
    "RJCT": "Rejected",
    "SUCC": "Success",
    "PNDG": "Pending",
    "PNDP": "Pending For Processing",
    "DUPL": "Duplicate",
    "FAIL": "Failure",
    "PGDT": "Draft",
    "PGQC": "Pending QC",
    "PGPB": "Partially Billed",
    "PGFB": "Fully Billed",
    "PGVD": "Voided",
    "PGAP": "Approved",
    "PGPD": "Submit for Approval",
    "SODT": "Draft",
    "SOPC": "Partially DC",
    "SODC": "Fully DC",
    "SOPI": "Partially Invoiced",
    "SOIN": "Fully Invoiced",
    "SOVD": "Voided",
    "SOAP": "Approved",
    "SOPD": "Submit for Approval",
    "SODL": "Deleted",
    "TODT": "Draft",
    "TOPD": "Submit for Approval",
    "TOAP": "Approved",
    "TOPC": "Partially DC",
    "TODC": "Fully DC",
    "TOPI": "Partially Invoiced",
    "TOIN": "Fully Invoiced",
    "TOVD": "Voided",
    "TODL": "Deleted",
    "SJDT": "Draft",
    "SJPT": "Posted",
    "SJVD": "Voided",
    "TRPD": "Paid",
    "TRVD": "Voided",
    "TRPN": "Pending",
    "TRDT": "Drafted",
    "TRDL": "Deleted",
    "TRPP": "Partially Paid",
    "PORJ": "Rejected",
    "SORJ": "Rejected",
    "IORJ": "Rejected",
    "TORJ": "Rejected",
    "SOSF": "Split Fully",
    "SOSP": "Split Partially",
    "SOPFFI": "Partially Proforma Invoiced",
    "SOPFI": "Fully Proforma Invoiced",
    "DCFR": "Fully Received",
    "DCPRD": "Partially Received",
    "DCPC": "Partially Consumed",
    "DCFC": "Fully Consumed",
    "SDNDT": "Draft",
    "SDNAP": "Awaiting Settlement",
    "SDNPN": "Pending Approval",
    "SDNPD": "Settled",
    "SDNVD": "Void",
    "BCNDT": "Draft",
    "BCNAP": "Awaiting Settlement",
    "BCNPN": "Submit for Approval",
    "BCNPD": "Settled",
    "BCNVD": "Void",
    "PRAP": "Approved",
    "PRDT": "Draft",
    "PRPD": "Pending Approval",
    "PRVD": "Void",
    "PRDL": "Deleted",
    "PRFPO": "Fully PO",
    "PRPPO": "Partially PO",
    "PMTSP": "Settled"
}

# Pipeline of generation
transaction_product_info = [
    {
        "$lookup": {
            "from": "txn_common_data",
            "let": {"txnId": "$txnId"},
            "pipeline": [
                {"$match": {"$expr": {"$eq": ["$txnId", "$$txnId"]}}},
            ],
            "as": "txn_common_data",
        },
    },
    {
        "$addFields": {
            "txn_common_data": {"$arrayElemAt": ["$txn_common_data", 0]},
        },
    },
    {
        "$match": {
            "txn_common_data": {"$ne": None},
        },
    }
]

transaction_jv_info = [
    {
        "$lookup": {
            "from": "txn_common_data",
            "let": {"txnId": "$txnId"},
            "pipeline": [
                {"$match": {"$expr": {"$eq": ["$txnId", "$$txnId"]}}},
            ],
            "as": "txn_common_data",
        },
    },
    {
        "$addFields": {
            "txn_common_data": {"$arrayElemAt": ["$txn_common_data", 0]},
        },
    },
    {
        "$match": {
            "txn_common_data": {"$ne": None},
        },
    }
]

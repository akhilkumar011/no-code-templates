import csv
import math
from datetime import timedelta

from dateutil.relativedelta import relativedelta

from accounting.data_utility.data_model import HbTxnInventoryMovements


def calculate_fifo_valuation(closing_stock_value, inward_result, outward_result, opening_stock_result, end_date):
    data_dict = []
    for key, stock in closing_stock_value.items():
        valuation_finished = False
        remaining_qty = stock['total_qty']
        total_value = 0
        index = 1
        if remaining_qty > 0:
            while not valuation_finished:
                stock_movement: [HbTxnInventoryMovements] = list(
                    HbTxnInventoryMovements.find_by_limit(
                        {"itemId": key, "status": True, "txnDate": {"$lte": end_date}, "adjType": 'INCR',
                         "txnType": {'$in': ['BILL', 'SDP', 'OPBL', 'STJL', 'INVT']}}, index, 100,
                        sort=[("txnDate", -1)]))
                if stock_movement:
                    for stock_move in stock_movement:
                        if remaining_qty > stock_move.qty:
                            remaining_qty -= stock_move.qty
                            total_value += stock_move.qty * stock_move.unitRate
                        elif 0 < remaining_qty <= stock_move.qty:
                            total_value += remaining_qty * stock_move.unitRate
                            remaining_qty = 0
                            valuation_finished = True
                            break
                        else:
                            valuation_finished = True
                            break
                else:
                    valuation_finished = True
                index += index
        data_dict.append({
            "itemId": stock['_id'],
            "itemCode": stock['itemCode'],
            "itemName": stock['itemName'],
            "openingStock": opening_stock_result[key]['openingStock'] if key in opening_stock_result else 0,
            "openingValue": opening_stock_result[key]['openingValue'] if key in opening_stock_result else 0,
            "inwardStock": inward_result[key]['inward_qty'] if key in inward_result else 0,
            "inwardValue": inward_result[key]['inward_value'] if key in inward_result else 0,
            "outwardStock": math.fabs(outward_result[key]['outward_qty'] if key in outward_result else 0),
            "outwardValue": math.fabs(outward_result[key]['outward_value'] if key in outward_result else 0),
            "currentStock": stock['total_qty'],
            "currentValue": total_value
        })
    return sorted(data_dict, key=lambda item: item['itemName'])


def calculate_fifo_method_valuation_opening(opening_stock_value, end_date):
    data_dict = {}
    # opening_stock_value = {3375: opening_stock_value[3375]}
    for key, stock in opening_stock_value.items():
        valuation_finished = False
        remaining_qty = stock['total_qty']
        total_value = 0
        index = 1
        if remaining_qty > 0:
            while not valuation_finished:
                stock_movement: [HbTxnInventoryMovements] = list(
                    HbTxnInventoryMovements().find_by_limit(
                        {"itemId": key, "status": True, "txnDate": {"$lte": end_date}, "adjType": 'INCR',
                         "txnType": {'$in': ['BILL', 'SDP', 'OPBL', 'STJL', 'INVT']}}, index, 100,
                        sort=[("txnDate", -1)]))
                if stock_movement:
                    for stock_move in stock_movement:
                        if remaining_qty > stock_move.qty:
                            remaining_qty -= stock_move.qty
                            total_value += stock_move.qty * stock_move.unitRate
                        elif 0 < remaining_qty <= stock_move.qty:
                            total_value += remaining_qty * stock_move.unitRate
                            remaining_qty = 0
                            valuation_finished = True
                            break
                        else:
                            valuation_finished = True
                            break
                else:
                    valuation_finished = True
                index += index
        data_dict[stock['_id']] = {
            "itemId": stock['_id'],
            "openingStock": stock['total_qty'],
            "openingValue": total_value
        }
    return data_dict


def generate_csv_fifo(dict_stock):
    with open("inventory_valuation_fifo.csv", "w", newline="") as csvfile:
        fieldnames = ["itemId", "itemCode", "itemName", "openingStock", "openingValue",
                      "inwardStock", "inwardValue", "outwardStock", "outwardValue", "currentStock",
                      "currentValue"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(dict_stock)


def generate_csv_avg(dict_stock):
    with open("inventory_valuation_avg.csv", "w", newline="") as csvfile:
        fieldnames = ["itemId", "itemCode", "itemName", "openingStock", "openingAvgCost", "openingValue", "inwardStock",
                      "inwardAvgCost", "inwardValue", "outwardStock", "outwardAvgCost", "outwardValue", "currentStock",
                      "currentAvgCost",
                      "currentValue"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(dict_stock)


def get_avg_method_valuation(closing_stock_value, inward_result, outward_result, opening_stock_result):
    data_dict = []
    for key, stock in closing_stock_value.items():
        avg_cost_value = (inward_result[key]['inward_value'] if key in inward_result else 0) + (
            opening_stock_result[key]['openingValue'] if key in opening_stock_result else 0)
        avg_cost_stock = (inward_result[key]['inward_qty'] if key in inward_result else 0) + (
            opening_stock_result[key]['openingStock'] if key in opening_stock_result else 0)
        avg_cost = avg_cost_value / avg_cost_stock if avg_cost_stock > 0 else 0
        avg_cost_inward = inward_result[key]['inward_value'] / inward_result[key][
            'inward_qty'] if key in inward_result else 0
        avg_cost_opening = opening_stock_result[key]['openingAvgCost'] if key in opening_stock_result else 0
        out_qty = outward_result[key]['outward_qty'] if key in outward_result else 0
        avg_cost_out = 0
        if out_qty > 0:
            avg_cost_out = math.fabs(outward_result[key]['outward_value'] / out_qty)
        total_value = stock['total_qty'] * avg_cost
        data_dict.append({
            "itemId": stock['_id'],
            "itemCode": stock['itemCode'],
            "itemName": stock['itemName'],
            "openingStock": opening_stock_result[key]['openingStock'] if key in opening_stock_result else 0,
            "openingAvgCost": avg_cost_opening,
            "openingValue": opening_stock_result[key]['openingValue'] if key in opening_stock_result else 0,
            "inwardStock": inward_result[key]['inward_qty'] if key in inward_result else 0,
            "inwardAvgCost": avg_cost_inward,
            "inwardValue": inward_result[key]['inward_value'] if key in inward_result else 0,
            "outwardStock": math.fabs(outward_result[key]['outward_qty'] if key in outward_result else 0),
            "outwardAvgCost": avg_cost_out,
            "outwardValue": math.fabs(outward_result[key]['outward_value'] if key in outward_result else 0),
            "currentStock": stock['total_qty'],
            "currentAvgCost": avg_cost,
            "currentValue": total_value
        })
    return sorted(data_dict, key=lambda item: item['itemName'])


def get_avg_method_valuation_opening(opening_stock_value, inward_result):
    data_dict = {}
    for key, stock in opening_stock_value.items():
        avg_cost_inward = 0
        total_value = 0
        if key in inward_result and inward_result[key]['inward_qty'] > 0:
            avg_cost_inward = inward_result[key]['inward_value'] / inward_result[key]['inward_qty']
            total_value = stock['total_qty'] * avg_cost_inward if avg_cost_inward > 0 else 0
        data_dict[stock['_id']] = {
            "itemId": stock['_id'],
            "openingStock": stock['total_qty'],
            "openingAvgCost": avg_cost_inward,
            "openingValue": total_value
        }
    return data_dict


def get_sum_qty_grouped_by_item_id(end_date):
    pipeline = [
        {
            "$match": {
                "txnDate": {"$lte": end_date},
                "maintainQtyFlag": True,
                "status": True
            }
        },
        {
            "$group": {
                "_id": "$itemId",
                "itemName": {"$first": "$itemName"},  # Use $first to accumulate itemName
                "itemCode": {"$first": "$itemCode"},  # Use $first to accumulate itemCode
                "total_qty": {"$sum": "$qty"}
            }
        }
    ]
    documents = list(HbTxnInventoryMovements().aggregate_raw(pipeline))
    dict_data = {}
    for data in documents:
        dict_data[data['_id']] = data
    return dict_data


# 3497
def get_inward_value_grouped_by_item_id(start_date, end_date, return_txn=False):
    txn_type = ['BILL', 'SDP', 'OPBL', 'STJL', 'INVT', 'SCN'] if return_txn else ['BILL', 'SDP', 'OPBL', 'STJL', 'INVT',
                                                                                  'PCN']
    pipeline = [
        {
            "$match": {
                "qty": {"$gt": 0},
                "maintainQtyFlag": True,
                "status": True,
                "$or": [
                    {"adjType": 'INCR'},
                    {"txnType": 'PCN'}
                ],
                "txnType": {"$in": txn_type},
                "txnDate": {"$gte": start_date, "$lte": end_date}
            }
        },
        {
            "$group": {
                "_id": "$itemId",
                "inward_qty": {"$sum": "$qty"},
                "inward_value": {"$sum": {"$multiply": ["$qty", "$unitRate"]}}
            }
        }
    ]
    documents = list(HbTxnInventoryMovements().aggregate_raw(pipeline))
    dict_data = {}
    for data in documents:
        dict_data[data['_id']] = data
    return dict_data


def get_outward_value_grouped_by_item_id(start_date, end_date, return_txn=False):
    txn_type = ['INV', 'RDP', 'INVT', 'PCN'] if return_txn else ['INV', 'RDP', 'INVT', 'SCN']
    pipeline = [
        {
            "$match": {
                "maintainQtyFlag": True,
                "status": True,
                "$or": [
                    {"adjType": 'DECR'},
                    {"txnType": 'SCN'}
                ],
                "txnType": {"$in": txn_type},
                "txnDate": {"$gte": start_date, "$lte": end_date}
            }
        },
        {
            "$group": {
                "_id": "$itemId",
                "outward_qty": {"$sum": "$qty"},
                "outward_value": {"$sum": {"$multiply": ["$qty", "$unitRate"]}}
            }
        }
    ]
    documents = list(HbTxnInventoryMovements().aggregate_raw(pipeline))
    dict_data = {}
    for data in documents:
        dict_data[data['_id']] = data
    return dict_data


def call_inventory_avg(start_date, end_date):
    # opening Stock Value AVG
    start_date_last = start_date - relativedelta(years=1)
    end_date_last = start_date - timedelta(days=1)
    opening_stock = get_sum_qty_grouped_by_item_id(end_date_last)
    print(f'The Opening_stock has {sum(item_data["total_qty"] for item_data in opening_stock.values())} Quantity.')
    print(f'The Opening has {len(opening_stock)} Items.')
    in_value = get_inward_value_grouped_by_item_id(start_date_last, end_date_last)
    opening_value = get_avg_method_valuation_opening(opening_stock, in_value)

    # closing Stock Value AVG
    closing_stock = get_sum_qty_grouped_by_item_id(end_date)
    print(f'The closing_stock has {sum(item_data["total_qty"] for item_data in closing_stock.values())} Quantity.')
    print(f'The closing_stock has {len(closing_stock)} Items.')
    in_value = get_inward_value_grouped_by_item_id(start_date, end_date)
    out_value = get_outward_value_grouped_by_item_id(start_date, end_date)
    closing_value = get_avg_method_valuation(closing_stock, in_value, out_value, opening_value)
    print(f'The Closing Final has {len(closing_value)} Items.')
    # generate_csv_avg(closing_value)
    return closing_value


def call_inventory_fifo(start_date, end_date):
    # opening Stock Value FIFO
    end_date_last = start_date - timedelta(days=1)
    opening_stock = get_sum_qty_grouped_by_item_id(end_date_last)
    print(f'The Opening_stock has {sum(item_data["total_qty"] for item_data in opening_stock.values())} Quantity.')
    print(f'The Opening has {len(opening_stock)} Items.')
    opening_value = calculate_fifo_method_valuation_opening(opening_stock, end_date_last)

    # closing Stock Value FIFO
    closing_stock = get_sum_qty_grouped_by_item_id(end_date)
    print(f'The closing_stock has {sum(item_data["total_qty"] for item_data in closing_stock.values())} Quantity.')
    print(f'The Closing Stock has {len(closing_stock)} Items.')
    in_value = get_inward_value_grouped_by_item_id(start_date, end_date)
    out_value = get_outward_value_grouped_by_item_id(start_date, end_date)
    closing_value = calculate_fifo_valuation(closing_stock, in_value, out_value, opening_value, end_date)
    print(f'The Closing Final has {len(closing_value)} Items.')
    # generate_csv_fifo(closing_value)
    return closing_value

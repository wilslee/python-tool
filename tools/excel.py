# usr/bin/env python
# -*- coding: utf-8 -*-
import xlrd
from xlrd.biffh import XLRDError


class ExcelReader(object):

    _data_set = []

    def read_sheet(self, book, sheet=None):
        if sheet is None:
            sheet_table = book.sheet_by_index(0)
        else:
            try:
                if isinstance(sheet, int):
                    sheet_table = book.sheet_by_index(sheet)
                elif isinstance(sheet, str) and sheet.isdigit():
                    sheet_table = book.sheet_by_index(int(sheet))
                else:
                    sheet_table = book.sheet_by_name(sheet)
            except XLRDError:
                raise XLRDError("没有 {} 这个工作区间".format(sheet))
        return sheet_table

    def get_data_set(self):
        return self._data_set

    def read(self, filename=None, file_contents=None, sheet=None, fields=None,
             header_row=0, start_row=1):
        self._data_set.clear()
        if fields is None:
            return
        book = xlrd.open_workbook(filename=filename, file_contents=file_contents, encoding_override='utf-8')
        sheet_table = self.read_sheet(book, sheet)
        read_list = {}
        # 读取行头，选取需要的数据列
        for cols in range(sheet_table.ncols):
            if sheet_table.cell(header_row, cols).value in fields:
                read_list.update({sheet_table.cell(header_row, cols).value: cols})

        dataset = []
        for r in range(start_row, sheet_table.nrows):
            cols = {}
            for key, c in read_list.items():
                value = sheet_table.cell_value(r, c)
                # 数字转化为字符串
                if sheet_table.cell_type(r, c) == xlrd.XL_CELL_NUMBER:
                    value = str(sheet_table.cell_value(r, c)).strip()
                elif sheet_table.cell_type(r, c) == xlrd.XL_CELL_TEXT:
                    value = str(sheet_table.cell_value(r, c)).strip().strip('\0')
                cols.update({key: value})
            dataset.append(cols)
        self._data_set = dataset

ecreader = ExcelReader()


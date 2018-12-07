# -*- coding: utf-8 -*-
import xdrlib, sys
import xlrd
from numpy import *


def open_excel(file='normalWalkingTest2.xls'):
    data = xlrd.open_workbook(file)
    return data


# 根据索引获取Excel表格中的数据   参数:file：Excel文件路径     colnameindex：表头列名所在行的索引  ，by_index：表的索引
def excel_table_byindex(startRow, file='normalWalkingTest2.xls', colnameindex=8, by_index=0):
    data = open_excel(file)
    table = data.sheets()[by_index]
    nrows = table.nrows #行数
    ncols = table.ncols #列数
    colnames = table.row_values(colnameindex) #每列变量名
    # print(colnames)
    # nrows = 11
    dataList =[]
    dataArray = zeros((int((nrows - startRow)/15)+1, 9))

    # for rowNum in range(0, nrows-startRow):
    rowNum = 0
    while rowNum*15 < nrows-startRow:
        row = table.row_values(rowNum*15+startRow)
        actNormal = row[2:10]
        dataArray[rowNum][1:9] = [actNormal[j]/800 for j in range(len(actNormal))]
        dataArray[rowNum][0] = row[1]
        if row:
            app = {}
            for i in range(0, len(colnames)):
                app[colnames[i]] = row[i]
            dataList.append(app)
        rowNum += 1
        # print(rowNum)

    return dataList, dataArray


def main():
    # data in List/ data in Array
    tableList, tableArray = excel_table_byindex(23) # startRow = num_of_start-1

    # for row in tableList:
    #     print(row)
    # print('\n')
    # print(len(tableList))
    #
    print(tableArray.shape)
    print(tableArray)


if __name__ == "__main__":
    main()
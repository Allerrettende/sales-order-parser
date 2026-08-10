# 销售分析表字段结构

## Header
Sales_Order_No (PK)
Document_No
Document_Date
Customer_Name
Customer_Address
Customer_No
Agent
Reference_Quote_No

## Items
Sales_Order_No (FK)
Line_No
POS_No
Item_Description
Quantity
Unit
Unit_Price
Amount
TC

这个结构支撑：
销售统计
客户分析
产品分析
Material / Service分析
后续SQL Server导入




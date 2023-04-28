## Data Warehouse 

I'm creating a simple data warehouse from scratch in this project. <br>
Used tools: Python, MySQL Server <br>
<br>
### <i>Source:</i><br>
- <lu> Transactions: https://www.kaggle.com/datasets/mashlyn/online-retail-ii-uci 
- <lu> Customers: I retrived unique customer ids from the original dataset and added Gender and DOB columns with randomly generated data. 

<br>

### <i>DWH layers:</i><br>

#### Meta <br>
The purpose of this schema is to logically separate metadata that is not directly related to the source data. Since the data warehouse is very simple, 
it has only one table which provides globally unique load session IDs, independent of layers <br>

#### Staging <br>
In this layer I use Python to handle the data prepare and load processes<br>
- <lu> Before the initial full load, transaction and customer tables are created to store the actual source data, history tables for storing previously loaded data, 
and a meta_load_history table for keeping track of the source, load date, and load status
- <lu> Source files are to be stored in dedicated, separate folders in CSV format. The corresponding script always loads the most recently created source file.
- <lu> After the initial full load, the customer and transaction tables are truncated before the next load session. 
However, the corresponding history tables and meta_load_history table are updated incrementally



#### DW 
Under development. The concept is to apply start schema, load data from Staging to fact and dimension tables with SQL  <br>



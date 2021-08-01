# DWH Coding Solution

## Task 1

The solution for this task is written in Python v3.8 and the file name is `task_1.py`.

`tabulate` package is required to show the result in tabular.

### Solution Summary

The first step of the code is to sort all the files in the given path by the timestamp stored inside each files. Then,
it will read the data from the oldest timestamp. Depends on the operation, it will just create a new record if the
operation is equal to `c`; but if the operation is equal to `u`, it will also create a new record including the
information from the last `c` operation with the same `id`.

Finally, the result will be returned in Dataframe.

## Task 2

The solution for this task is written in Python v3.8 and the file name is `task_2.py`.

`tabulate` package is required to show the result in tabular.

### Solution Summary
   
First, it will use the method from the first task which is to read all data and store them in Dataframe. Then, to get 
the result in a denormalized table, it will do the following steps:
1. Get the Cards data with respective Account ID
2. Get the Savings Accounts data with respective Account ID
3. Fill every event with the Account, Cards and Savings Accounts
4. Clean up some data
5. Choose which fields to show and rename them if needed

## Task 3

Based on what the result shown, the transaction of the Saving Accounts happens `4` times while for the Cards happens `3`
times.

Each of the transaction at the following event:
#### Savings Account transactions: timestamp - `value`
1. 1577955600000 - `15000`
2. 1578648600000 - `40000`
3. 1578654000000 - `21000`
3. 1579505400000 - `33000`

#### Card transactions: timestamp - `value`
1. 1578313800000 - `12000`
2. 1578420000000 - `19000`
3. 1579361400000 - `37000`
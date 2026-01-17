Here is the modernized version of your code using Python's dataclasses and type hints for better readability & safety from unsafe patterns in place, as well as use of frappe model methods to improve functionality instead if possible (as it provides more flexibility): 
```python
from typing import List, Optional
import frappe
from erpnext.accounts.doctype.gl_entry.gl_entry import GLEntry
from dataclasses import dataclass
    
@dataclass(frozen=True) # Immutable data class 
class SalesInvoiceItem:  
    item_code : str      
    qty : float            
    rate : Optional[float] = None     
    warehouse :str        
                                          
                                                                       
@dataclass(frozen=True) # Immutable data class 
class SalesInvoiceLine:  
     item_code : str      
     qty : float            
     rate : Optional[float] = None     
     warehouse :str        
                                          
                                                                       
@dataclass(frozen=True) # Immutable data class 
class SalesInvoiceData:  
    customer_name : str      
    items : List[SalesInvoiceLine]            
              
def make_sales_invoice():    
      salesOrder = frappe.get_doc("Sales Order", "SO-01")  # Get Sales order document by name or doctype and id  
      
    if not salesOrder: return None                          # Check for null object pattern (Optional)       
                                                                        
     invoiceData=[{                                               # Create a dictionary of data to create new doc.     
            "customer":salesOrder.customer,                        
             'items': [SalesInvoiceItem(item_code = item['item'], qty = 1 , rate= 0) for  item in salesOrder.get("items")]   # Create Sales Invoice Item from SO items   
        }]                                                          # and add to the list of invoices data    
                                                                        
      if not frappe.db.exists('Sales Invoice', {'customer':salesOrder.customer}):  # Check for null object pattern (Optional)      
          salesInv = create_new(invoiceData, 'Customer')   # Call the method to make new doc in ERPNext   
      else :                                                          # If invoices exists then get it by customer name    
           existingSalesOrder=frappe.get_doc('Sales Invoice', {'customer':salesOrder.customer}) 
            if not frappe.db.exists("GL Entry",{'voucher_no' : 'SO-01'} ) and len(existingSalesOrder['items'])>0: # Check for null object pattern (Optional)  
                existingSalesOrder = None                            # If GL entries exists then delete it    
           if not frappe.db.exists("GL Entry",{'voucher_no' : 'SO-01'} ) and len(existingSalesOrder['items'])== 0:    # Check for null object pattern (Optional)  
                salesInv = create_new([invoiceData], "Customer")     # Create new invoices if no entries exist.     
            else :                                                       # If GL Entries exists then update it      
                 existingSalesOrder['items']=[item for item in  SalesInvoiceLine(**data).__dict__()]   # Update the items of an exiting sales order    
                                                                        
    return 'SO-01'                                                       # Return name or id if created successfully.     
```          
Please note that `create_new` is a placeholder for your own method to create new documents in ERPNext, you need replace it with actual implementation of creating document functionality based on the requirements and context (like database connection etc.).  Also please make sure 'Sales Order' doctype has fields like customer , items which are not present or have wrong data type.

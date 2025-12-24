## Fuel Surcharge Table Updater

### What this script does
This script updates the **fuel surcharge tables** on the APG website.

It:
- Reads new fuel surcharge data from `new_surcharge.csv`.
- Moves the existing rows from the *current* table into the *historical* table.
- Rebuilds the current table using the same Avia `[av_table] / [av_row]` structure.
- Outputs updated table files ready to paste back into WordPress.

---

### How to use

1. Open the WordPress editor:  
   https://apgecommerce.com/wp-admin/post.php?post=57&action=edit

<img width="1629" height="909" alt="image" src="https://github.com/user-attachments/assets/a6c81748-fd8d-46d8-8fbb-bfcbd7c6724b" />


2. Copy the table contents:
   - **Code block 1** → paste into `OLD_av_table1.txt`
   - **Code block 2** → paste into `OLD_av_table2.txt`


3. Update **only the values** (numbers / percentages) in:
   - **new_surcharge.csv**
Do not change formatting or remove tags, only modify the text data and percentages.


4. This will generate two new files. Copy the contents of these files back into code blocks 1 and 2 in WordPress:
   - **NEW_av_table1.txt** → paste into `Code Block 1`
   - **NEW_av_table2.txt** → paste into `Code Block 2`

5. NOTE: Preview or make these changes in UAT before committing changes to PROD website to confirm.

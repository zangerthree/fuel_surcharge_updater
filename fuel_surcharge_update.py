import os
import csv
import re
import datetime


def log_print(message):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")

def read_text_file(path, encoding='utf-8'):
    with open(path, 'r', encoding=encoding) as f:
        return f.read()


def write_text_file(path, content, encoding='utf-8'):
    with open(path, 'w', encoding=encoding) as f:
        f.write(content)


def extract_row_blocks(table_content):
    # Return regex list of full [av_row]...[/av_row] blocks
    row_pattern = r'(\[av_row[^\]]*\].*?\[/av_row\])'
    matches = list(re.finditer(row_pattern, table_content, re.DOTALL))
    return [m.group(0) for m in matches]


def build_table_from_csv(opening_tag, rows):
    parts = [opening_tag]
    # header
    header_row = "[av_row row_style='']"
    header_row += "[av_cell col_style='']Period[/av_cell]"
    header_row += "[av_cell col_style='']Product[/av_cell]"
    header_row += "[av_cell col_style='']Fuel Surcharge[/av_cell]"
    header_row += "[/av_row]"
    parts.append(header_row)

    for row in rows:
        cells = row[:3]
        while len(cells) < 3:
            cells.append('')
        row_html = "[av_row row_style='']"
        row_html += "[av_cell col_style='']" + cells[0] + "[/av_cell]"
        row_html += "[av_cell col_style='']" + cells[1] + "[/av_cell]"
        row_html += "[av_cell col_style='']" + cells[2] + "[/av_cell]"
        row_html += "[/av_row]"
        parts.append(row_html)

    parts.append('[/av_table]')
    return '\n'.join(parts)


def process_files(base_dir):
    av1_path = os.path.join(base_dir, 'av_table1.txt')
    av2_path = os.path.join(base_dir, 'av_table2.txt')
    csv_path = os.path.join(base_dir, 'new_surcharge.csv')

    if not os.path.exists(csv_path):
        log_print(f'CSV file not found at {csv_path}')
        return False

    # read csv
    try:
        with open(csv_path, newline='', encoding='cp1252') as f:
            reader = csv.reader(f)
            table_values = [ [ (cell or '') for cell in row[:3] ] for row in reader if row ]
        log_print('Read CSV successfully')
    except Exception as e:
        log_print(f'Failed to read CSV: {e}')
        return False

    av1_content = ''
    av2_content = ''
    if os.path.exists(av1_path):
        av1_content = read_text_file(av1_path)
    else:
        log_print(f'{av1_path} not found; a new table will be created')

    if os.path.exists(av2_path):
        av2_content = read_text_file(av2_path)

    # Extract rows from av_table1
    current_rows = []
    opening_tag = "[av_table purpose='pricing' pricing_table_design='avia_pricing_default' id='fuel-surcharges-table']"
    if av1_content:
        # try to capture opening tag
        m = re.search(r'(\[av_table[^\]]*\])', av1_content)
        if m:
            opening_tag = m.group(1)
        # get row blocks
        row_blocks = extract_row_blocks(av1_content)
        if len(row_blocks) > 1:
            # skip header (first block)
            current_rows = row_blocks[1:]
        else:
            current_rows = []

    if current_rows:
        if not av2_content:
            av2_content = "[av_table purpose='pricing' pricing_table_design='avia_pricing_default' id='fuel-surcharges-table-historical']\n"
            av2_content += "[av_row row_style='']"
            av2_content += "[av_cell col_style='']Period[/av_cell]"
            av2_content += "[av_cell col_style='']Product[/av_cell]"
            av2_content += "[av_cell col_style='']Fuel Surcharge[/av_cell]"
            av2_content += "[/av_row]\n[/av_table]"

        # insert after first header closing [/av_row]
        insert_pos = av2_content.find('[/av_row]')
        if insert_pos != -1:
            insert_pos += len('[/av_row]')
            av2_content = av2_content[:insert_pos] + '\n' + '\n'.join(current_rows) + av2_content[insert_pos:]
        else:
            # fallback: append before closing tag
            av2_content = av2_content.replace('[/av_table]', '\n' + '\n'.join(current_rows) + '\n[/av_table]')

        write_text_file(av2_path, av2_content)
        log_print(f'Appended {len(current_rows)} rows to historical table at {av2_path}')

    # Build new current table from CSV and write to av_table1
    new_current_table = build_table_from_csv(opening_tag, table_values)
    write_text_file(av1_path, new_current_table)
    log_print(f'Wrote new current table to {av1_path}')

    return True


if __name__ == '__main__':
    base_dir = os.path.dirname(__file__)
    # perform processing using local files: av_table1, av_table2, new_surcharge.csv
    ok = process_files(base_dir)
    if ok:
        log_print('Processing complete')
    else:
        log_print('Processing failed')
    

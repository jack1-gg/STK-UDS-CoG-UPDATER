import csv
import os
import glob


def get_row(asin, csv_rows, sku=None):
    # return row from asin or asin+sku value
    for row in csv_rows:
        if row["ASIN"].strip() == asin.strip():
            if sku:
                if row["SKU"].strip() == sku.strip():
                    return row
            else:
                return row

    # return empty list no row matches searching params
    return []


class CoG_Updater:
    def __init__(self, ts):
        # constants
        self.TS = ts
        self.PATH = f"./uploads/{self.TS}"

        # variables
        self.uds_rows = None
        self.atp_rows = None
        self.updated_stk_fnames = None
        self.updated_stk = None
        self.stk_rows = None

    def run(self):
        self.read_files()
        self.update_stk()
        self.write_csv()
        self.write_tsv()
        self.clear_files()

    def read_files(self):
        # read and save stk
        stk = open(f"{self.PATH}/stk.tsv", encoding="utf8")
        self.stk_rows = [r for r in csv.DictReader(stk, delimiter="\t")]
        self.updated_stk = []
        self.updated_stk_fnames = [f for f in self.stk_rows[0]]

        # get all .csv files
        csv_files = glob.glob(f"{self.PATH}/*.csv")

        # read and save uds
        fname = csv_files[0]
        uds = open(os.path.join(os.getcwd(), fname), 'r', encoding="utf8")
        self.uds_rows = [r for r in csv.DictReader(uds)]

        # reverse uds_rows list in order to get the latest products while reading the list with get_row()
        self.uds_rows = self.uds_rows[::-1]

    def update_stk(self):
        # read stk rows and update products CoG, VAT, Supplier info, Order number
        for row in self.stk_rows:
            uds_row = get_row(asin=row["ASIN"], csv_rows=self.uds_rows)
            new_row = row
            if new_row["CoG Status"] != "Cog Ok":
                new_row["CoG Status"] = "Check CoG"
                new_row["UNITCOST_VAT_INCLUSIVE(Required)"] = uds_row["BUY"].strip('£')
                new_row["SUPPLIER_LINK(Optional)"] = uds_row["SOURCE"]
                new_row["ORDER_NUMBER(Optional)"] = uds_row["ORDER ID"]
                new_row["SUPPLIER(Optional)"] = uds_row["STORE NAME"]

                # add updated row to the new stk file
                self.updated_stk.append(new_row)

    def write_csv(self):
        # write stk file as .csv
        with open(f"{self.PATH}/updated_stk.csv", "w", encoding="utf8") as f:
            writer = csv.DictWriter(f, fieldnames=self.updated_stk_fnames)
            writer.writeheader()
            for row in self.updated_stk:
                writer.writerow(row)

        # close file
        f.close()

    def write_tsv(self):
        # convert stk file from .csv as .tsv
        with open(f"{self.PATH}/updated_stk.csv", encoding="utf8") as csv_in, open(f"./{self.PATH}/updated_stk.txt", "w", encoding="utf8") as tsv_out:
            csv_in = csv.reader(csv_in)
            tsv_out = csv.writer(tsv_out, delimiter='\t')
            for row in csv_in:
                tsv_out.writerow(row)

    def clear_files(self):
        # delete all useless files
        for f in os.listdir(f"{self.PATH}/"):
            if f.endswith(".txt"):
                continue
            os.remove(os.path.join(f"{self.PATH}/", f))

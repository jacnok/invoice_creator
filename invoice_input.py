# from multiprocessing.managers import Value (I DID NOT WRITE THIS??? Thanks, IDE)

import pylightxl as pxl
import PySimpleGUIQt as sGUI    # TODO: replace with FreeSimpleGui (https://github.com/spyoungtech/FreeSimpleGUI)
import sys
import os
import unicodedata
import re
from dotenv import load_dotenv


class InvInput:
    def __init__(self):

        self.title_list = []
        self.detail_list = []
        self.rationale_list = []
        self.hours_list = []
        self.rate_list = []
        self.percentage_list = []
        self.price_list = []
        self.category_list = []

        self.service = []
        self.serv_rationale = []
        self.serv_rate = []
        self.serv_price = []

        self.disc_type = []
        self.disc_reason = []
        self.disc_percs = []
        self.disc_cost = []
        self.tax_perc = 0.0

        self.invoice_num = 00000                                    # cannot be lower than 10000
        self.client_name = "clientFN1 clientLN2"                    # can also just be clientName
        self.proj_name = "artistName1, songName2 - projectType3"    # can also just be projectName
        self.delivery_date = "November XX, 2099"                    # Month DD, YYYY
        self.delivery_method = "snail mail"                         # ex: a YouTube channel upload, a Google Drive upload, etc.
        self.due_by = "December XX, 2199"                           # Month DD, YYYY

        self.company_name = "Jefferson"
        self.my_address_l1 = "XXXX streetFN Avenue"
        self.my_address_l2 = "Chicago, IL 00000"
        self.my_phone_num = "XXX-XXX-XXXX"
        self.my_contact_l1 = "example.me"
        self.my_contact_l2 = "python-dev@example.me"
        self.form_type = "FORM"

        self.alt_payments = """"""
        self.alt_pay_warning = """"""

    def get_detail_from_title(self, x):
        return self.detail_list[self.title_list.index(x)]

    def get_price_from_category(self, x):
        return self.price_list[self.category_list.index(x)]

    def get_perc_from_category(self, x):
        return self.percentage_list[self.category_list.index(x)]

    def open_read_writeHTMLline(self, x):
        y = """"""

        with open(x, encoding='UTF-8') as my_file:
            for line in my_file:
                y += self.replace_quotes(line) + "<br>"
                print(line)
        return y

    def replace_quotes(self, x):
        a = unicodedata.normalize("NFKD", str(x))
        b = re.sub("[“]+", "&ldquo;", a)
        y = re.sub("[”]+", "&rdquo;", b)
        return y

    def importer(self, f_name1, f_name2, output_place):

        load_dotenv()

        # reads from .env to prevent unnecessary private data leakage
        self.company_name = os.getenv('COMPANY_NAME')
        self.my_address_l1 = os.getenv('ADDRESS_01')
        self.my_address_l2 = os.getenv('ADDRESS_02')
        self.my_phone_num = os.getenv('CONTACT_NUM')
        self.my_contact_l1 = os.getenv('CONTACT_01')
        self.my_contact_l2 = os.getenv('CONTACT_02')

        self.alt_payments = self.open_read_writeHTMLline("alt_payments.txt")
        self.alt_pay_warning = self.open_read_writeHTMLline("alt_pay_warning.txt")

        proj_data = pxl.readxl(f_name1)

        proj_col_list = []

        for col in proj_data.ws(ws='Sheet1').cols:
            proj_col_list.append(col)

        # borrowing this from https://stackoverflow.com/questions/10993612/how-to-remove-xa0-from-string-in-python

        for a in range(len(proj_col_list)):
            for b in range(len(proj_col_list[a])):
                # print(proj_col_list[a][b])
                c = unicodedata.normalize("NFKD", str(proj_col_list[a][b]))
                proj_col_list[a][b] = re.sub("[’]+", "&rsquo;", c)

        # print(proj_col_list) # debug statement

        self.title_list = proj_col_list[0]
        self.detail_list = proj_col_list[1]
        self.rationale_list = proj_col_list[2]
        self.hours_list = proj_col_list[3]
        self.rate_list = proj_col_list[4]
        self.percentage_list = proj_col_list[5]
        self.price_list = proj_col_list[6]
        self.category_list = proj_col_list[7]

        print("\n\nThis is the category list:")
        print(self.category_list)

        try:
            self.form_type = self.get_detail_from_title("Form Type").upper()
        except ValueError:
            print("Probably just an invoice.")
            self.form_type = "INVOICE"
        else:
            print("how did we get here?")

        self.invoice_num = self.get_detail_from_title("Invoice Number")
        print("This is the invoice number: " + self.invoice_num)

        self.client_name = self.get_detail_from_title("Client Name")
        self.proj_name = self.get_detail_from_title("Project Name")
        self.delivery_date = self.get_detail_from_title("Delivery Date")
        self.delivery_method = self.get_detail_from_title("Delivery Method")
        self.due_by = self.get_detail_from_title("Due By")

        for x in range(len(self.category_list)):
            if self.category_list[x] == "Charge":
                self.service.append(self.title_list[x])
                self.serv_rationale.append(self.rationale_list[x])
                self.serv_rate.append(self.rate_list[x])
                self.serv_price.append(self.price_list[x])
                print("Charge was run")     # debug statement

            elif self.category_list[x] == "Discount":
                self.disc_type.append(self.title_list[x])
                self.disc_reason.append(self.rationale_list[x])
                self.disc_percs.append(self.percentage_list[x])
                self.disc_cost.append(self.price_list[x])
                print("Disc was run")       # debug statement

        # print("this is the list of charges:") # debug sequence
        # for x in range(len(self.service)):
        #     print(f"\nService: {self.service[x]} "
        #           f"\n\t Service Rationale: {self.serv_rationale[x]}"
        #           f"\n\t Service Rate: {self.serv_rate[x]}"
        #           f"\n\t Service Price: {self.serv_price[x]}"
        #           )   # debug sequence

        self.tax_perc = float(self.get_perc_from_category("Tax"))
        # print("This is the tax percentage: " + str((self.tax_perc * 100)) + "%")    # debug statement

        # p_total = 0.00
        #
        # for x in self.serv_price:
        #     p_total = p_total + float(x)
        # print("This is the subtotal before discounts or taxes: " + "${:.2f}".format(p_total))   # debug sequence


    def my_gui_creator(self):
        sGUI.theme('Dark2')

        # gets file that has all the regular data we need for the invoice
        if len(sys.argv) == 1:
            event, values = sGUI.Window('Import (Data) Excel File',
                                        [[sGUI.Text('Document to open')],
                                         [sGUI.In(), sGUI.FileBrowse()],
                                         [sGUI.Open(), sGUI.Cancel()]]).read(close=True)
            f_name1 = values[0]
        else:
            f_name1 = sys.argv[1]

        if not f_name1:
            sGUI.popup_error("Cancelling: no filename supplied.", title="Program Exiting Now.")
            raise SystemExit("Cancelling: no filename supplied")
        else:
            sGUI.popup('The filename you chose was: ', f_name1)
    #
    #     # gets file that has all the background data we need for the invoice
    #     if len(sys.argv) == 1:
    #         event, values = sGUI.Window('Import (Background) Excel File',
    #                                     [[sGUI.Text('Document to open')],
    #                                      [sGUI.In(), sGUI.FileBrowse()],
    #                                      [sGUI.Open(), sGUI.Cancel()]]).read(close=True)
    #         f_name2 = values[0]
    #     else:
    #         f_name2 = sys.argv[1]
    #
    #     if not f_name2:
    #         sGUI.popup_error("Cancelling: no filename supplied.", title="Program Exiting Now.")
    #         raise SystemExit("Cancelling: no filename supplied")
    #     else:
    #         sGUI.popup('The filename you chose was: ', f_name2)
    #
    #     output_place = sGUI.popup_get_folder("Output Folder for HTML:")

        f_name2 = ""        # testing
        output_place = ""   # testing

        self.importer(f_name1, f_name2, output_place)

# my_gui_creator()

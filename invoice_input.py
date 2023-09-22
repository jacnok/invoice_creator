import pylightxl as pxl
import PySimpleGUIQt as sGUI

import sys

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

    def get_detail_from_title(self, x):
        return self.detail_list[self.title_list.index(x)]

    def get_price_from_category(self, x):
        return self.price_list[self.category_list.index(x)]

    def get_perc_from_category(self, x):
        return self.percentage_list[self.category_list.index(x)]

    def importer(self, f_name1, f_name2, output_place):
        proj_data = pxl.readxl(f_name1)
        # bkg_data = pxl.readxl(f_name2)

        # proj_full_list = []
        # proj_dict = [{      "title": "Invoice Number",
        #                     "details": ...,
        #                     "serv_rationale": ...,
        #                     "hours": ...
        #
        #             }]

        proj_col_list = []

        # for row in proj_data.ws(ws='Sheet1').rows:
        #     proj_full_list.append(row)
        #     print(row)
        # ...

        for col in proj_data.ws(ws='Sheet1').cols:
            proj_col_list.append(col)
            # print(col)

        # borrowing this from https://stackoverflow.com/questions/10993612/how-to-remove-xa0-from-string-in-python

        import unicodedata

        for a in range(len(proj_col_list)):
            for b in range(len(proj_col_list[a])):
                # print(proj_col_list[a][b])
                c = unicodedata.normalize("NFKD", str(proj_col_list[a][b]))
                proj_col_list[a][b] = c

        # print(proj_col_list)

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

        invoice_num = self.get_detail_from_title("Invoice Number")
        print("This is the invoice number: " + invoice_num)

        client_name = self.get_detail_from_title("Client Name")
        proj_name = self.get_detail_from_title("Project Name")
        delivery_date = self.get_detail_from_title("Delivery Date")
        delivery_method = self.get_detail_from_title("Delivery Method")
        due_by = self.get_detail_from_title("Due By")

        service = []
        serv_rationale = []
        serv_rate = []
        serv_price = []

        disc_type = []
        disc_reason = []
        serv_percs = []
        disc_cost = []

        for x in range(len(self.category_list)):
            if self.category_list[x] == "Charge":
                service.append(self.title_list[x])
                serv_rationale.append(self.rationale_list[x])
                serv_rate.append(self.rate_list[x])
                serv_price.append(self.price_list[x])
                print("Charge was run")

            elif self.category_list[x] == "Discount":
                disc_type.append(self.title_list[x])
                disc_reason.append(self.rationale_list[x])
                serv_percs.append(self.percentage_list[x])
                disc_cost.append(self.price_list[x])
                print("Disc was run")

        tax_perc = float(self.get_perc_from_category("Tax"))
        print("This is the tax percentage: " + str((tax_perc * 100)) + "%")

        p_total = 0.00

        for x in serv_price:
            p_total = p_total + float(x)

        print("This is the subtotal before discounts or taxes: " + "${:.2f}".format(p_total))

        # [[x,x,x,x,x,x,x], [x,x,x,x,x,x], [...], ...]

        # for x in proj_full_list:
        #     proj_dict.append([])
        #     for y in range(7):
        #         match y:
        #             case 0:
        #                 proj_dict[x].update({})





def my_gui_creator():
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

    x = InvInput()

    x.importer(f_name1, f_name2, output_place)


my_gui_creator()

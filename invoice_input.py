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

        self.service = []
        self.serv_rationale = []
        self.serv_rate = []
        self.serv_price = []

        self.disc_type = []
        self.disc_reason = []
        self.disc_percs = []
        self.disc_cost = []
        self.tax_perc = 0.0

        self.invoice_num = 00000  # cannot be lower than 10000
        self.client_name = "clientFN1 clientLN2"  # can also just be clientName
        self.proj_name = "artistName1, songName2 - projectType3"  # can also just be projectName
        self.delivery_date = "November XX, 2099"  # Month DD, YYYY
        self.delivery_method = "snail mail via parcel express"  # ex: a YouTube channel upload, a Google Drive upload, etc.
        self.due_by = "December XX, 2199" # Month DD, YYYY

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
        import re

        for a in range(len(proj_col_list)):
            for b in range(len(proj_col_list[a])):
                # print(proj_col_list[a][b])
                c = unicodedata.normalize("NFKD", str(proj_col_list[a][b]))
                proj_col_list[a][b] = re.sub("[’]+", "&rsquo;", c)

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

        print("this is the list of charges:")
        for x in range(len(self.service)):
            print(f"\nService: {self.service[x]} "
                  f"\n\t Service Rationale: {self.serv_rationale[x]}"
                  f"\n\t Service Rate: {self.serv_rate[x]}"
                  f"\n\t Service Price: {self.serv_price[x]}"
                  )

        self.tax_perc = float(self.get_perc_from_category("Tax"))
        print("This is the tax percentage: " + str((self.tax_perc * 100)) + "%")

        p_total = 0.00

        for x in self.serv_price:
            p_total = p_total + float(x)

        print("This is the subtotal before discounts or taxes: " + "${:.2f}".format(p_total))

        # [[x,x,x,x,x,x,x], [x,x,x,x,x,x], [...], ...]

        # for x in proj_full_list:
        #     proj_dict.append([])
        #     for y in range(7):
        #         match y:
        #             case 0:
        #                 proj_dict[x].update({})

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

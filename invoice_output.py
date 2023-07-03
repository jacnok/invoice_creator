import invoice_input as io_in

# this all needs to go into an Excel sheet that gets called from io_in, and passed along
my_address_l1 = "XXXX streetFN Avenue"
my_address_l2 = "Chicago, IL 00000"
my_phone_num = "XXX-XXX-XXXX"

# this all goes into a different Excel sheet that gets called from io_in, and passed along
invoice_num = 10000                                 # cannot be lower than 10000
client_name = "clientFN clientLN"                   # can also just be clientName
proj_name = "artistName, songName - projectType"    # can also just be projectName
delivery_date = "January XX, 2099"                  # Month DD, YYYY
delivery_method = "snail mail"                      # ex: a YouTube channel upload, a Google Drive upload, etc.

# this will be how we do most of this:
# https://towardsdatascience.com/how-to-easily-create-a-pdf-file-with-python-in-3-steps-a70faaf5bed5

pg1_context = \
    {
        'my_address_l1': my_address_l1,
        'my_address_l2': my_address_l2,
        'my_phone_num': my_phone_num,

        'invoice_num': invoice_num,

        'client_name': client_name,
        'proj_name': proj_name,
        'delivery_date': delivery_date,
        'delivery_method': delivery_method,

    }

charge_list = ""                            # will be raw HTML, consisting of <tr> of charge_HTML_forms all smashed together
disc_list = ""                              # will be raw HTML, consisting of <tr> of disc_HTML_forms all smashed together
due_by = "March XX, 2099"                   # Month DD, YYYY

charge_HTML_form = """
 <tr>
  <td width=222 valign=top style='width:166.35pt;border:solid #AEAAAA 1.0pt;
  border-top:none;padding:0in 5.4pt 0in 5.4pt'>
  <p class=MsoNormal style='margin-bottom:0in;line-height:normal'><span
  style='font-family:"Work Sans"'>{service}</span></p>
  </td>
  <td width=294 style='width:220.5pt;border-top:none;border-left:none;
  border-bottom:solid #AEAAAA 1.0pt;border-right:solid #AEAAAA 1.0pt;
  padding:0in 5.4pt 0in 5.4pt'>
  <p class=MsoListParagraph style='margin-bottom:0in;text-indent:-.25in;
  line-height:normal'><span style='font-family:"Work Sans"'>-<span
  style='font:7.0pt "Times New Roman"'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; </span></span><span
  style='font-family:"Work Sans"'>{rationale}</span></p>
  </td>
  <td width=108 style='width:80.65pt;border-top:none;border-left:none;
  border-bottom:solid #AEAAAA 1.0pt;border-right:solid #AEAAAA 1.0pt;
  padding:0in 5.4pt 0in 5.4pt'>
  <p class=MsoNormal align=right style='margin-bottom:0in;text-align:right;
  line-height:normal'><span style='font-family:"Work Sans"'>$ {price}</span></p>
  </td>
 </tr>
"""

charge_HTML_form_new = ""

disc_HTML_form = """..."""

disc_HTML_form_new = ""


alt_payments = """..."""

service = []
rationale = []
rate = []
price = []

discount = []
reasoning = []
percentage = []
cost = []

for x in service:
    charge_HTML_form_new = charge_HTML_form.format(
                            service=service[x],
                            rationale=rationale[x],
                            price=price[x])
    charge_list = charge_list + charge_HTML_form_new



pg2_context = \
    {
        "charge_list": charge_list,
        "due_by": due_by,
        ...: ...
    }


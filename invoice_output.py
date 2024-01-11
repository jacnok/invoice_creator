import invoice_input as io_in
import jinja2
import pdfkit

obj = io_in.InvInput()                              # this should be pulling everything from the input files
obj.my_gui_creator()

# this all needs to go into an Excel sheet that gets called from io_in, and passed along
my_address_l1 = "XXXX streetFN Avenue"
my_address_l2 = "Chicago, IL 00000"
my_phone_num = "XXX-XXX-XXXX"

# this all goes into a different Excel sheet that gets called from io_in, and passed along
# invoice_num = 10000                                 # cannot be lower than 10000
# client_name = "clientFN clientLN"                   # can also just be clientName
# proj_name = "artistName, songName - projectType"    # can also just be projectName
# delivery_date = "January XX, 2099"                  # Month DD, YYYY
# delivery_method = "snail mail"                      # ex: a YouTube channel upload, a Google Drive upload, etc.

invoice_num = obj.invoice_num
client_name = obj.client_name
proj_name = obj.proj_name
delivery_date = obj.delivery_date
delivery_method = obj.delivery_method


def money(x):
    return "{:.2f}".format(x)


def open_file(x):
    y = ""
    readMyFile = open(x, "r")
    for line in readMyFile:
        y = y + "\n" + line
    readMyFile.close()
    print("File has been closed.")
    return y


# borrowed from this: https://stackoverflow.com/a/38239630 to solve rounding issues
def round_t(val, digits):
    return round(val+10**(-len(str(val))-1), digits)

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

print(pg1_context)

charge_list = ""                            # will be raw HTML, consisting of <tr> of charge_HTML_forms all smashed together
disc_list = ""                              # will be raw HTML, consisting of <tr> of disc_HTML_forms all smashed together

due_by = obj.due_by                  # Month DD, YYYY

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

disc_HTML_form = """
 <tr>
  <td width=222 valign=top style='width:166.35pt;border:solid #AEAAAA 1.0pt;
  border-top:none;padding:0in 5.4pt 0in 5.4pt'>
  <p class=MsoNormal style='margin-bottom:0in;line-height:normal'><span
  style='font-family:"Work Sans"'>{disc_type}</span></p>
  </td>
  <td width=294 style='width:220.5pt;border-top:none;border-left:none;
  border-bottom:solid #AEAAAA 1.0pt;border-right:solid #AEAAAA 1.0pt;
  padding:0in 5.4pt 0in 5.4pt'>
  <p class=MsoListParagraph style='margin-bottom:0in;text-indent:-.25in;
  line-height:normal'><span style='font-family:"Work Sans"'>-<span
  style='font:7.0pt "Times New Roman"'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; </span></span><span
  style='font-family:"Work Sans"'>{disc_reason}</p>
  </td>
  <td width=108 style='width:80.65pt;border-top:none;border-left:none;
  border-bottom:solid #AEAAAA 1.0pt;border-right:solid #AEAAAA 1.0pt;
  padding:0in 5.4pt 0in 5.4pt'>
  <p class=MsoNormal align=right style='margin-bottom:0in;text-align:right;
  line-height:normal'><span style='font-family:"Work Sans"'>(-) $ {disc_cost}</span></p>
  </td>
 </tr>
"""

disc_HTML_form_new = ""


alt_payments = """..."""

service = obj.service
rationale = obj.serv_rationale
rate = obj.serv_rate
price = obj.serv_price

p_total = 0.00

for x in price:
    p_total = round_t((p_total + float(x)), 2)

disc_type = obj.disc_type
disc_reason = obj.disc_reason
percentages = obj.disc_percs
disc_cost = obj.disc_cost
tax_perc = obj.tax_perc



disc_total = 0.00

for x in disc_cost:
    disc_total = round_t((disc_total + float(x)), 2)

for x in range(len(service)):
    charge_HTML_form_new = charge_HTML_form.format(
                            service=service[x],
                            rationale=rationale[x],
                            price=money(float(price[x]))
    )
    charge_list = charge_list + charge_HTML_form_new

for x in range(len(disc_type)):
    disc_HTML_form_new = disc_HTML_form.format(
                            disc_type=disc_type[x],
                            disc_reason=disc_reason[x],
                            disc_cost=money(float(disc_cost[x]))
    )
    disc_list = disc_list + disc_HTML_form_new

subtotal_full = round_t(p_total - disc_total, 2)
tax_total = round_t(subtotal_full * tax_perc, 2)
price_total = round_t(subtotal_full + tax_total, 2)

pg2_context = \
    {
        "charge_list": charge_list,
        "disc_list": disc_list,
        "due_by": due_by,
        "subtotal_init": money(p_total),
        "subtotal_full": money(subtotal_full),
        "price_total": money(price_total),
        "tax_total": money(tax_total),
        "tax_percentage": (tax_perc * 100),
        "disc_total": money(disc_total),
        'invoice_num': invoice_num,
    }


def template_creator():

    template_loader = jinja2.FileSystemLoader('./')   # indicates folder where current HTML template is located.

    template_env = jinja2.Environment(loader = template_loader)

    template1 = template_env.get_template("invoice_pg1.html")
    template2 = template_env.get_template("invoice_pg2.html")

    output_text1 = template1.render(pg1_context)
    output_text2 = template2.render(pg2_context)

    config = pdfkit.configuration(wkhtmltopdf = "C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe")

    pdfkit.from_string(output_text1, 'pg1_generated.pdf', configuration=config)
    pdfkit.from_string(output_text2, 'pg2_generated.pdf', configuration=config)


template_creator()

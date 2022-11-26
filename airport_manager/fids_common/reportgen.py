from fpdf import FPDF
from fids_common import login
from fids_common import settings
from fids_common import displaystr

class ReportPDF(FPDF):
    def __init__(self, connection, *a, **kw):
        self.mysql = connection
        super().__init__(*a, **kw)

    def header(self):
        pass

    # Page footer
    def footer(self):
        # Position at 1.5 cm from bottom
        self.set_y(-15)
        # Arial italic 8
        self.set_font('Arial', '', 8)
        # Page number
        self.cell(0, 10, settings.getstring("airport", "iata")+ "/" + settings.getstring("airport", "icao") + ', page ' + str(self.page_no()) + ' out of {nb}', 0, 0, 'R')

    def colored_table(self, headings, rows, col_widths=(42, 39, 35, 42)):
        # Colors, line width and bold font:
        self.set_fill_color(255, 100, 0)
        self.set_text_color(255)
        self.set_draw_color(255, 0, 0) # border colour
        self.set_line_width(0.3)
        self.set_font(style="B")
        for col_width, heading in zip(col_widths, headings):
            self.cell(col_width, 7, heading, border=1, align="C", fill=True)
        self.ln()
        # Color and font restoration:
        self.set_fill_color(224, 235, 255)
        self.set_text_color(0)
        self.set_font()
        fill = False
        for row in rows:
            for i in range(len(row)):
                self.cell(w=col_widths[i], h=6, txt=str(row[i]), border="LR", align="L", fill=fill)
            self.ln()
            fill = not fill
        self.cell(sum(col_widths), 0, "", "T")
        
    def heading(self):
        self.alias_nb_pages()
        self.add_page()
        # report title
        # Logo
        self.image('resources/airportlogo.png', 10, 8, h=10)
        # Arial bold 15
        self.set_font('Arial', 'B', 25)
        # Move to the right
        # self.cell(80)
        # Title
        self.cell(0, 25, settings.getstring("airport", "name", "Airport Report").upper(), align='C')
        # Line break
        self.ln(13)
        self.set_font('Arial', 'I', 15)
        self.multi_cell(0, 15, settings.getstring("airport", "addr", ""), align='C')
        self.ln(20)
        
    def delay_report(self, outfile):
        self.heading()
        self.set_font('Arial', 'BU', 25)
        self.cell(0, 20, 'Delay Report', align='L')
        self.ln(20)
        # data start

        cursor = self.mysql.cursor()
        cursor.execute("SELECT `ifid`, `ofid`, `from`, `to`, `eta`, `etd`, TIMESTAMPDIFF(MINUTE, `sta`, `eta`) AS 'delayarr', TIMESTAMPDIFF(MINUTE, `std`, `etd`) AS `delaydep` FROM `flight` ORDER BY `eta` ASC;")

        reslist = []
        
        for rec in cursor.fetchall():
            res = [rec[0] or "N/A", rec[1] or "N/A", rec[2] or "N/A", rec[3] or "N/A", str(rec[4]) if rec[2] else "N/A", str(rec[5]) if rec[3] else "N/A", str(rec[6]) if rec[2] else "N/A", str(rec[7]) if rec[3] else "N/A"]
            reslist.append(res)
            
        # for i in range(1, 100):
        #     self.set_font('Arial', 'BU', 16)
        #     self.cell(1, 10, f'Airline {i}', align='L')
        #     self.ln(10)
        #     self.set_font('Arial', '', 10)
        #     self.cell(0, 10, f'No of flights - 20')
        #     self.ln(10)
        #     self.cell(0, 10, f'    Incoming - 20')
        #     self.ln(10)
        #     self.cell(0, 10, f'    Outgoing - 0')
        #     self.ln(10)
        #     self.cell(0, 1, f'', align='L', border="B")
        #     self.ln(5)
        self.set_font('Arial', '', 10)
        self.colored_table(["InCode", "OutCode", "From", "To", "ETA", "ETD", "DelayDep (mins)", "DelayArr (mins)"], reslist, col_widths=(20, 20, 46, 46, 35, 35, 30, 30 ))
        self.ln(10)

        #cursor.execute("SELECT IF(`ifid` IS NULL, LEFT(`ofid`,2), LEFT(`ifid`, 2)), COUNT(*) AS 'noflt', COUNT(TIMESTAMPDIFF(MINUTE, `sta`, `eta`) > 0) AS 'countdelayarr', COUNT(TIMESTAMPDIFF(MINUTE, `sta`, `eta`) < 0) AS 'countearlyarr',  COUNT(TIMESTAMPDIFF(MINUTE, `sta`, `eta`) = 0) AS 'countontimearr', COUNT(TIMESTAMPDIFF(MINUTE, `std`, `etd`) > 0) AS 'countdelaydep', COUNT(TIMESTAMPDIFF(MINUTE, `std`, `etd`) < 0) AS 'countearlydep',  COUNT(TIMESTAMPDIFF(MINUTE, `std`, `etd`) = 0) AS 'countontimedep' FROM `flight` GROUP BY LEFT(`ifid`, 2), IF(`ifid` IS NULL, LEFT(`ofid`, 2), LEFT(`ifid`, 2)) ORDER BY LEFT(`ifid`, 2) ASC;")
        
        cursor.execute("""SELECT
        IF(`ifid` IS NULL, LEFT(`ofid`, 2), LEFT(`ifid`, 2)) as 'iata',
        COUNT(*) AS 'noflt',
        SUM(TIMESTAMPDIFF(MINUTE, `sta`, `eta`) > 0) AS 'countdelayarr',
        SUM(TIMESTAMPDIFF(MINUTE, `sta`, `eta`) < 0) AS 'countearlyarr',
        SUM(IF(`ifid`, TIMESTAMPDIFF(MINUTE, `sta`, `eta`) = 0, 0)) AS 'countontimearr',
        SUM(TIMESTAMPDIFF(MINUTE, `std`, `etd`) > 0) AS 'countdelaydep',
        SUM(TIMESTAMPDIFF(MINUTE, `std`, `etd`) < 0) AS 'countearlydep',
        SUM(IF(`ofid`, TIMESTAMPDIFF(MINUTE, `std`, `etd`) = 0, 0)) AS 'countontimedep'
        FROM
        `flight`
        GROUP BY
        IF(`ifid` IS NULL, LEFT(`ofid`, 2), LEFT(`ifid`, 2))
        ORDER BY
        LEFT(`ifid`, 2) ASC;
        """)

        lst2 = []
        for res in cursor.fetchall():
            iata = res[0]
            # noflt = float(res[1] or 0)
            countdelayarr = float(res[2] or 0)
            countearlyarr = float(res[3] or 0)
            countontimearr = float(res[4] or 0)
            countdelaydep = float(res[5] or 0)
            countearlydep = float(res[6] or 0)
            countontimedep = float(res[7] or 0)
            
            noflt = sum((countdelayarr, countearlyarr, countontimearr, countearlydep, countdelaydep, countontimedep))
            
            relfac = (((-1)*((countdelayarr+countdelaydep)/noflt))
                      + (countearlyarr+countearlydep)/noflt)
            
            lst2.append([iata, "{:.0f}".format(noflt), "{:.0f}".format(countdelayarr), "{:.0f}".format(countearlyarr), "{:.0f}".format(countontimearr), "{:.0f}".format(countdelaydep), "{:.0f}".format(countearlydep), "{:.0f}".format(countontimedep), "{:.4f}".format(relfac)])

        self.set_font('Arial', 'BU', 25)
        self.cell(0, 20, 'Airline-wise Consolidated Delay Report', align='L')
        self.ln(20)
        
        self.set_font('Arial', '', 10)
        self.colored_table(["IATACode", "#flt", "#arrdelay", "#arrearly", "#arrontime", "#depdelay", "#depearly", "#depontime", "R_f"], lst2, col_widths=(29,)*9)
        
        self.ln(10)
        self.set_font('Arial', 'I', 12)
        self.multi_cell(0, txt="NOTE: Reliability factor is the expectation of X, where X is a random variable between -1, 0 and 1. -1 deontes delayed flights, 0 on time, 1 early flights.")

        self.output(outfile)


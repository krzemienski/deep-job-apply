from fpdf import FPDF

# Create instance of FPDF class
pdf = FPDF()

# Add a page
pdf.add_page()

# Set font
pdf.set_font("Arial", size = 12)

# Add text
pdf.cell(200, 10, txt = "JOHN DOE", ln = True, align = 'C')
pdf.cell(200, 10, txt = "Software Engineer", ln = True, align = 'C')
pdf.ln(10)
pdf.cell(200, 10, txt = "EXPERIENCE", ln = True)
pdf.cell(200, 10, txt = "ABC Tech, Software Engineer", ln = True)
pdf.cell(200, 10, txt = "- Developed scalable backend services using Python and FastAPI", ln = True)
pdf.cell(200, 10, txt = "- Implemented frontend interfaces with React and Next.js", ln = True)
pdf.cell(200, 10, txt = "- Utilized Docker for containerization and deployment", ln = True)
pdf.ln(5)
pdf.cell(200, 10, txt = "XYZ Corp, Junior Developer", ln = True)
pdf.cell(200, 10, txt = "- Built RESTful APIs with Django", ln = True)
pdf.cell(200, 10, txt = "- Created automated testing frameworks", ln = True)
pdf.ln(10)
pdf.cell(200, 10, txt = "EDUCATION", ln = True)
pdf.cell(200, 10, txt = "Bachelor of Science in Computer Science", ln = True)
pdf.cell(200, 10, txt = "University of Technology, 2018-2022", ln = True)
pdf.ln(10)
pdf.cell(200, 10, txt = "SKILLS", ln = True)
pdf.cell(200, 10, txt = "Python, JavaScript, React, Docker, FastAPI, Next.js, AWS, Git", ln = True)

# Save the pdf
pdf.output("test_resume.pdf")

"""Builds docs/Khorn_Sokhadom_Lab_Final.pdf from the screenshots folder.

Run from the project root:  python docs/build_report.py
"""
from pathlib import Path

from PIL import Image as PILImage
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import (Image, KeepTogether, PageBreak, Paragraph,
                                SimpleDocTemplate, Spacer, Table, TableStyle)

ROOT = Path(__file__).resolve().parent.parent
SHOTS = ROOT / "screenshots"
OUT = ROOT / "docs" / "Khorn_Sokhadom_Lab_Final.pdf"

GITHUB = "https://github.com/SokhadomKhorn/labfinal"

BLACK = colors.black
title_style = ParagraphStyle("title", fontName="Helvetica-Bold", fontSize=20, leading=26,
                             alignment=TA_CENTER, textColor=BLACK, spaceAfter=10)
subtitle_style = ParagraphStyle("subtitle", fontName="Helvetica", fontSize=13, leading=18,
                                alignment=TA_CENTER, textColor=BLACK)
task_style = ParagraphStyle("task", fontName="Helvetica-Bold", fontSize=16, leading=20,
                            textColor=BLACK, spaceBefore=4, spaceAfter=10)
caption_style = ParagraphStyle("caption", fontName="Helvetica-Bold", fontSize=11.5, leading=15,
                               textColor=BLACK, spaceBefore=6, spaceAfter=6)
body_style = ParagraphStyle("body", fontName="Helvetica", fontSize=11, leading=16, textColor=BLACK)

PAGE_W, PAGE_H = A4
MARGIN = 2 * cm
FRAME_W = PAGE_W - 2 * MARGIN
FRAME_H = PAGE_H - 2 * MARGIN


def shot(name):
    return SHOTS / f"Screenshot 2026-11-12 {name}.png"


def trim_white_right(path, right=None):
    """Copy of the screenshot with the empty white area on the right removed (colours unchanged)."""
    with PILImage.open(path) as im:
        if right is None:
            gray = im.convert("L").point(lambda v: 255 if v < 235 else 0)
            box = gray.getbbox()
            if not box:
                return path
            right = min(im.width, box[2] + 40)
        out = Path(__file__).resolve().parent / ".build" / path.name
        out.parent.mkdir(exist_ok=True)
        im.crop((0, 0, right, im.height)).save(out)
        return out


def figure(caption, path, max_h=None, max_upscale=1.6, trim=False, crop_right=None):
    """Caption + original-colour screenshot, scaled to fit the page (never distorted)."""
    if trim or crop_right:
        path = trim_white_right(path, crop_right)
    with PILImage.open(path) as im:
        w_px, h_px = im.size
    w, h = w_px * 0.75, h_px * 0.75  # pixels -> points at 96 dpi
    max_h = max_h or (FRAME_H - 70)
    scale = min(FRAME_W / w, max_h / h, max_upscale)
    img = Image(str(path), width=w * scale, height=h * scale)
    framed = Table([[img]], style=TableStyle([
        ("BOX", (0, 0), (-1, -1), 0.6, colors.HexColor("#9a9a9a")),
        ("LEFTPADDING", (0, 0), (-1, -1), 0), ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 0), ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
    ]))
    framed.hAlign = "CENTER"
    return KeepTogether([Paragraph(caption, caption_style), framed, Spacer(1, 14)])


def footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 9)
    canvas.setFillColor(BLACK)
    canvas.drawString(MARGIN, 1.1 * cm, "Khorn Sokhadom - Student Management System")
    canvas.drawRightString(PAGE_W - MARGIN, 1.1 * cm, f"Page {doc.page}")
    canvas.restoreState()


story = []

# ---------- Cover ----------
story += [
    Spacer(1, 5 * cm),
    Paragraph("Hands-On Practical Examination", title_style),
    Paragraph("Microservices, Database, Docker &amp; Kubernetes", subtitle_style),
    Spacer(1, 1.2 * cm),
    Paragraph("Student Management System", subtitle_style),
    Spacer(1, 2.5 * cm),
    Paragraph("<b>Student:</b> Khorn Sokhadom", subtitle_style),
    Spacer(1, 6),
    Paragraph("<b>2nd Microservice:</b> Update Student Mobile Number or Password", subtitle_style),
    Spacer(1, 6),
    Paragraph(f'<b>GitHub:</b> <a href="{GITHUB}" color="black"><u>{GITHUB}</u></a>', subtitle_style),
    PageBreak(),
]

# ---------- Overview ----------
overview = [
    ["Microservice", "Pod", "Endpoints (through API Gateway)"],
    ["API Gateway", "Pod 1", "Entry point for every request (port 8080)"],
    ["Registration Service", "Pod 1", "POST /api/register\nGET /api/students\nGET /api/students/:id"],
    ["Update Service", "Pod 2", "PUT /api/update/mobile/:id\nPUT /api/update/password/:id\nPATCH /api/update/:id"],
]
table = Table(overview, colWidths=[4.2 * cm, 2 * cm, FRAME_W - 6.2 * cm])
table.setStyle(TableStyle([
    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
    ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
    ("FONTSIZE", (0, 0), (-1, -1), 10.5),
    ("TEXTCOLOR", (0, 0), (-1, -1), BLACK),
    ("GRID", (0, 0), (-1, -1), 0.6, BLACK),
    ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ("TOPPADDING", (0, 0), (-1, -1), 5), ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
]))
story += [
    Paragraph("Project Overview", task_style),
    Paragraph("Database schema (MongoDB collection <b>students</b>): Student_id, Student_name, "
              "student_mobile, student_email, student_password.", body_style),
    Spacer(1, 10),
    Paragraph("All requests from Postman go through the API Gateway. The API Gateway and the "
              "Registration Service run as two containers in Pod 1; the Update Service runs in Pod 2.",
              body_style),
    Spacer(1, 14),
    table,
    PageBreak(),
]

# ---------- Task 1 ----------
story += [Paragraph("Task 1: Microservices Code", task_style),
          figure("1.1  API Gateway  (api-gateway/server.js)", shot("182559")),
          PageBreak(),
          figure("1.2  Registration Microservice  (registration-service/server.js)", shot("182624")),
          PageBreak(),
          figure("1.3  Update Microservice  (update-service/server.js)", shot("182645")),
          PageBreak()]

# ---------- Task 2 ----------
story += [Paragraph("Task 2: Dockerfile for Each Microservice", task_style),
          figure("2.1  API Gateway Dockerfile", shot("182716"), max_upscale=1.45),
          figure("2.2  Registration Service Dockerfile", shot("182720"), max_upscale=1.45),
          figure("2.3  Update Service Dockerfile", shot("182725"), max_upscale=1.45),
          PageBreak()]

# ---------- Task 3 ----------
story += [Paragraph("Task 3: Kubernetes Minikube Pod Deployment YAML", task_style),
          figure("3.1  Pod YAML  (k8s/pods.yaml) - Pod 1: API Gateway + Registration, Pod 2: Update",
                 shot("182811"), max_h=FRAME_H - 250),
          figure("3.2  Pods running in Minikube  (kubectl get pods)", shot("182827"), max_upscale=1.3),
          PageBreak()]

# ---------- Task 4 ----------
story += [Paragraph("Task 4: Service YAML", task_style),
          figure("4.1  Service YAML  (k8s/services.yaml)", shot("182901")),
          figure("4.2  Services in Minikube  (kubectl get svc)", shot("182852"), max_upscale=1.3),
          figure("4.3  API Gateway service exposed for Postman  (kubectl port-forward)", shot("182927"),
                 max_upscale=1.3),
          PageBreak()]

# ---------- Task 5 ----------
story += [Paragraph("Task 5: Registration Microservice API Call (Postman) and Database", task_style),
          figure("5.1  Register Student - POST /api/register  (201 Created)", shot("183111"),
                 max_h=FRAME_H - 80),
          PageBreak(),
          figure("5.2  Get All Students - GET /api/students", shot("183121")),
          PageBreak(),
          figure("5.3  Get Student By Id - GET /api/students/{id}", shot("183128")),
          PageBreak(),
          figure("5.4  Database - MongoDB Atlas database student_management (collections)",
                 shot("184613"), max_upscale=1.6),
          figure("5.5  Database - student record in the students collection",
                 shot("184609"), trim=True, max_upscale=1.3),
          figure("5.6  Database - counters collection used to generate Student_id",
                 shot("184620"), crop_right=420, max_upscale=1.3),
          PageBreak()]

# ---------- Task 6 ----------
story += [Paragraph("Task 6: Update Microservice API Call (Postman)", task_style),
          figure("6.1  Update Mobile Number - PUT /api/update/mobile/{id}", shot("183146"),
                 max_h=FRAME_H - 80),
          PageBreak(),
          figure("6.2  Update Password - PUT /api/update/password/{id}", shot("183155")),
          PageBreak(),
          figure("6.3  Update Mobile and Password Together - PATCH /api/update/{id}", shot("183210")),
          PageBreak(),
          figure("6.4  Verify Update - GET /api/students/{id}", shot("183218")),
          PageBreak(),
          figure("6.5  Error Handling - update a student that does not exist (404 Not Found)",
                 shot("183239")),
          PageBreak()]

# ---------- Task 7 ----------
story += [Paragraph("Task 7: Source Code on GitHub", task_style),
          Paragraph(f'Repository: <b><a href="{GITHUB}" color="black"><u>{GITHUB}</u></a></b>', body_style),
          Spacer(1, 8),
          Paragraph("The repository contains the three microservices (api-gateway, registration-service, "
                    "update-service) with their Dockerfiles, the Kubernetes YAML files in k8s/, "
                    "the Postman collection in postman/, the screenshots and this report.", body_style)]

doc = SimpleDocTemplate(str(OUT), pagesize=A4, leftMargin=MARGIN, rightMargin=MARGIN,
                        topMargin=MARGIN, bottomMargin=MARGIN,
                        title="Student Management System - Khorn Sokhadom", author="Khorn Sokhadom")
doc.build(story, onFirstPage=lambda c, d: None, onLaterPages=footer)
print("Wrote", OUT)

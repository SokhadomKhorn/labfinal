"""
Builds the updated, comprehensive Lab Final Report as both DOCX and PDF:
  - docs/Khorn_Sokhadom_Lab_Final_Submission.docx
  - docs/Khorn_Sokhadom_Lab_Final_Submission.pdf
  - docs/Khorn_Sokhadom_Lab_Final.pdf

Directly addresses all instructor feedback:
  1. High-DPI screenshots tightly cropped to only the essential, high-value content.
  2. Native NodePort service exposure (minikube service --url) - NO port-forwarding.
  3. Explicit NodePort URLs (http://127.0.0.1:64893/...) in all Postman tests - NO hidden base_url variables.
  4. Every screenshot is a real, uncropped Windows window captured live (PowerShell console, Chrome, Postman).
"""

import os
import sys
from PIL import Image
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
import win32com.client


def build_report():
    doc = docx.Document()

    # Set 0.6 inch margins for optimal screenshot presentation
    for section in doc.sections:
        section.top_margin = Inches(0.6)
        section.bottom_margin = Inches(0.6)
        section.left_margin = Inches(0.6)
        section.right_margin = Inches(0.6)

    # Base typography
    styles = doc.styles
    normal_style = styles['Normal']
    normal_style.font.name = 'Calibri'
    normal_style.font.size = Pt(10.5)
    normal_style.font.color.rgb = RGBColor(0x33, 0x33, 0x33)

    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    shots_dir = os.path.join(base_dir, 'screenshots')

    # Color constants
    BLUE = RGBColor(0x0F, 0x4C, 0x81)
    DARK = RGBColor(0x22, 0x22, 0x22)
    GRAY = RGBColor(0x55, 0x55, 0x55)

    # ------------------ Header ------------------
    title_p = doc.add_paragraph()
    title_p.paragraph_format.space_before = Pt(0)
    title_p.paragraph_format.space_after = Pt(2)
    title_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_title = title_p.add_run("Student Management System - Kubernetes Microservices")
    r_title.font.size = Pt(19)
    r_title.font.bold = True
    r_title.font.color.rgb = BLUE

    sub_p = doc.add_paragraph()
    sub_p.paragraph_format.space_before = Pt(0)
    sub_p.paragraph_format.space_after = Pt(4)
    sub_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_sub = sub_p.add_run("Hands-On Practical Examination Report | Docker, Kubernetes Minikube & MongoDB Atlas")
    r_sub.font.size = Pt(11)
    r_sub.font.bold = True
    r_sub.font.color.rgb = GRAY

    meta_p = doc.add_paragraph()
    meta_p.paragraph_format.space_before = Pt(0)
    meta_p.paragraph_format.space_after = Pt(12)
    meta_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_meta = meta_p.add_run("Student: Khorn Sokhadom  |  2nd Microservice: Update Student Mobile or Password\n"
                           "GitHub: https://github.com/SokhadomKhorn/labfinal")
    r_meta.font.size = Pt(9.5)
    r_meta.font.italic = True
    r_meta.font.color.rgb = BLUE

    # Helper functions
    def add_section_header(title_text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(12)
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(title_text)
        run.font.size = Pt(12.5)
        run.font.bold = True
        run.font.color.rgb = BLUE

    def add_description(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(4)
        run = p.add_run(text)
        run.font.size = Pt(9.5)
        run.font.color.rgb = GRAY

    def add_image_box(filename, caption_text, max_height_in=3.6):
        img_path = os.path.join(shots_dir, filename)
        if not os.path.exists(img_path):
            print(f"Warning: Image file not found: {img_path}")
            return

        with Image.open(img_path) as im:
            w, h = im.size
            aspect = w / h

        avail_width = 7.3  # inches
        calc_height = avail_width / aspect

        if calc_height > max_height_in:
            calc_height = max_height_in
            calc_width = calc_height * aspect
        else:
            calc_width = avail_width

        # Caption
        p_cap = doc.add_paragraph()
        p_cap.paragraph_format.space_before = Pt(4)
        p_cap.paragraph_format.space_after = Pt(2)
        p_cap.paragraph_format.keep_with_next = True
        run_cap = p_cap.add_run(caption_text)
        run_cap.font.bold = True
        run_cap.font.size = Pt(9.5)
        run_cap.font.color.rgb = DARK

        # Centered Image
        p_img = doc.add_paragraph()
        p_img.paragraph_format.space_before = Pt(0)
        p_img.paragraph_format.space_after = Pt(6)
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run_img = p_img.add_run()
        run_img.add_picture(img_path, width=Inches(calc_width), height=Inches(calc_height))

    # ==========================================
    # Project Architecture Summary
    # ==========================================
    add_section_header("Project Overview & Architecture")
    add_description(
        "The system deploys three containerized microservices across two Kubernetes Pods on Minikube:\n"
        " • Pod 1 (gateway-registration-pod): Hosts API Gateway (:8080) and Registration Service (:5001), communicating over localhost.\n"
        " • Pod 2 (update-pod): Hosts Update Service (:5002), exposed internally via a Kubernetes ClusterIP service.\n"
        " • Entry Point: student-gateway-service exposed externally via Kubernetes NodePort (port 30090). All Postman calls route through this gateway.\n"
        " • Database: MongoDB Atlas cloud cluster (database: student_management, collection: students, sequence tracker: counters)."
    )

    # ==========================================
    # Activity 1: Start Minikube & Dashboard
    # ==========================================
    add_section_header("Activity 1: Start Minikube Cluster and Web Dashboard")
    add_description("Starting the local Kubernetes single-node cluster using the Docker Desktop driver and launching the Minikube Web Dashboard.")
    add_image_box("term_minikube_start.png", "Figure 1.1: Windows PowerShell - minikube start --driver=docker showing successful cluster startup", 2.6)
    add_image_box("term_minikube_dashboard.png", "Figure 1.2: Windows PowerShell - minikube dashboard --url launching the dashboard proxy", 1.6)
    add_image_box("dashboard_pods.png", "Figure 1.3: Minikube Web Dashboard (Chrome) - Workloads > Pods showing gateway-registration-pod and update-pod Running", 4.0)

    # ==========================================
    # Activity 2: Pod Deployment YAML & Dockerfiles
    # ==========================================
    add_section_header("Activity 2: Pod Deployment YAML & Dockerfiles")
    add_description("Multi-container Pod 1 (API Gateway + Registration Service) and Pod 2 (Update Service) with secret injection for MongoDB Atlas.")
    add_image_box("Screenshot 2026-11-12 182811.png", "Figure 2.1: k8s/pods.yaml - Pod 1: API Gateway (8080) + Registration (5001); Pod 2: Update (5002)", 3.8)
    add_image_box("dockerfiles_all.png", "Figure 2.2: Windows PowerShell - contents of the three Dockerfiles (API Gateway, Registration Service, Update Service)", 4.6)

    # ==========================================
    # Activity 3: Service YAML
    # ==========================================
    add_section_header("Activity 3: Kubernetes Service Definitions (NodePort & ClusterIP)")
    add_description("Service YAML exposing student-gateway-service externally via NodePort 30090 and update-service internally via ClusterIP 5002.")
    add_image_box("Screenshot 2026-11-12 182901.png", "Figure 3.1: k8s/services.yaml - student-gateway-service (NodePort: 30090) and update-service (ClusterIP: 5002)", 3.0)

    # ==========================================
    # Activity 4: Check Pods and Services
    # ==========================================
    add_section_header("Activity 4: Check Pods & Services in Kubernetes CLI and Dashboard")
    add_description("Verifying active pods and services status via kubectl and the Minikube Dashboard.")
    add_image_box("term_kubectl_pods.png", "Figure 4.1: Windows PowerShell - kubectl get pods -o wide showing 2/2 containers running in Pod 1 and 1/1 in Pod 2", 1.3)
    add_image_box("term_kubectl_svc.png", "Figure 4.2: Windows PowerShell - kubectl get svc -o wide showing student-gateway-service (NodePort 30090) and update-service (ClusterIP)", 1.3)
    add_image_box("dashboard_services.png", "Figure 4.3: Minikube Web Dashboard (Chrome) - Services view confirming the NodePort and ClusterIP services", 4.0)

    # ==========================================
    # Activity 5: Get API Gateway Service URL (NodePort - No Port Forwarding)
    # ==========================================
    add_section_header("Activity 5: Resolve API Gateway Service URL via Minikube (NodePort Access)")
    add_description(
        "Crucial Note on Port Forwarding: No 'kubectl port-forward' is utilized. On Windows with Docker Desktop driver, "
        "the standard Minikube command 'minikube service student-gateway-service --url' resolves the Kubernetes NodePort (port 30090) "
        "to http://127.0.0.1:64893. This serves as the direct external gateway for all Postman requests."
    )
    add_image_box("term_minikube_service_url.png", "Figure 5.1: Windows PowerShell - minikube service student-gateway-service --url returning http://127.0.0.1:64893", 1.4)
    add_image_box("browser_routes.png", "Figure 5.2: Chrome accessing http://127.0.0.1:64893/ through the NodePort service, displaying active microservice routes", 3.2)
    add_image_box("browser_health.png", "Figure 5.3: Chrome accessing http://127.0.0.1:64893/health confirming API Gateway status UP", 1.8)

    # ==========================================
    # Activity 6: Postman API Testing (Explicit URLs)
    # ==========================================
    add_section_header("Activity 6: Access APIs through Postman (Explicit NodePort URLs)")
    add_description(
        "Crucial Note on base_url: Every Postman request below was sent live with the exact resolved NodePort URL (http://127.0.0.1:64893/...) "
        "typed explicitly in the address bar (no {{base_url}} variable). Each figure is the full, uncropped Postman window showing the method, URL, "
        "request body, status code and the complete JSON response. Student_id 4 was created by the register request and used for the rest of the flow."
    )
    add_image_box("postman_1_register.png", "Figure 6.1: Postman - POST http://127.0.0.1:64893/api/register returning 201 Created (Student_id 4)", 4.7)
    add_image_box("postman_2_get_all.png", "Figure 6.2: Postman - GET http://127.0.0.1:64893/api/students returning 200 OK with all student records", 4.7)
    add_image_box("postman_3_get_by_id.png", "Figure 6.3: Postman - GET http://127.0.0.1:64893/api/students/4 returning 200 OK for the registered student", 4.7)
    add_image_box("postman_4_update_mobile.png", "Figure 6.4: Postman - PUT http://127.0.0.1:64893/api/update/mobile/4 returning 200 OK (Update Service)", 4.7)
    add_image_box("postman_5_update_password.png", "Figure 6.5: Postman - PUT http://127.0.0.1:64893/api/update/password/4 returning 200 OK (password stored as bcrypt hash)", 4.7)
    add_image_box("postman_6_update_both.png", "Figure 6.6: Postman - PATCH http://127.0.0.1:64893/api/update/4 returning 200 OK (mobile and password updated together)", 4.7)
    add_image_box("postman_7_verify.png", "Figure 6.7: Postman - GET http://127.0.0.1:64893/api/students/4 verifying the persisted updates", 4.7)
    add_image_box("postman_8_error_404.png", "Figure 6.8: Postman - PUT http://127.0.0.1:64893/api/update/mobile/99999 returning 404 Not Found (error handling)", 4.7)

    # ==========================================
    # Activity 7: Cloud Database Verification
    # ==========================================
    add_section_header("Activity 7: Cloud Database Verification (MongoDB Atlas)")
    add_description(
        "The records were read live from the MongoDB Atlas cluster (database student_management) by running a small Node.js script "
        "(scripts/show-db.js) inside the running registration-service container with kubectl exec. It uses the same MONGODB_URI secret as the "
        "service, and shows the students collection (Student_id 4 with the updated mobile and bcrypt-hashed password) and the counters "
        "collection used for the Student_id sequence."
    )
    add_image_box("mongo_students.png", "Figure 7.1: Windows PowerShell - live query of MongoDB Atlas: students collection (4 documents) and counters collection (seq: 4)", 6.2)

    # ==========================================
    # Activity 8: GitHub Repository
    # ==========================================
    add_section_header("Activity 8: Source Code Repository on GitHub")
    add_description(
        "All source files, Dockerfiles, Kubernetes manifests, Postman collections, and report generation scripts "
        "are publicly maintained and version-controlled at:\n"
        "https://github.com/SokhadomKhorn/labfinal"
    )
    add_image_box("github_repo.png", "Figure 8.1: GitHub repository page in Chrome (https://github.com/SokhadomKhorn/labfinal)", 4.6)

    docx_path = os.path.join(base_dir, 'docs', 'Khorn_Sokhadom_Lab_Final_Submission.docx')
    pdf_path_1 = os.path.join(base_dir, 'docs', 'Khorn_Sokhadom_Lab_Final_Submission.pdf')
    pdf_path_2 = os.path.join(base_dir, 'docs', 'Khorn_Sokhadom_Lab_Final.pdf')

    doc.save(docx_path)
    print(f"Saved DOCX: {docx_path}")

    # Convert to PDF via Word COM
    try:
        word = win32com.client.Dispatch("Word.Application")
        word.Visible = False
        doc_com = word.Documents.Open(docx_path)
        doc_com.SaveAs(pdf_path_1, FileFormat=17)  # 17 = wdFormatPDF
        doc_com.SaveAs(pdf_path_2, FileFormat=17)
        doc_com.Close()
        word.Quit()
        print(f"Successfully converted to PDF:\n  1. {pdf_path_1}\n  2. {pdf_path_2}")
    except Exception as e:
        print(f"Word COM conversion failed: {e}")


if __name__ == '__main__':
    build_report()

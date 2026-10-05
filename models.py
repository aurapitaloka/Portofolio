from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Profile(db.Model):
    __tablename__ = 'profile'
    id = db.Column(db.Integer, primary_key=True)
    # Hero Section
    badge_text = db.Column(db.String(100), default="👋 Halo, Saya")
    full_name = db.Column(db.String(150), default="Aura Pitaloka")
    nav_brand = db.Column(db.String(50), default="AP")
    tagline = db.Column(db.String(200), default="Informatics Engineering Student")
    sub_tagline = db.Column(db.String(200), default="Passionate in QA Testing & Full-Stack Web Development")
    hero_description = db.Column(db.Text, nullable=True)
    avatar = db.Column(db.String(255), default="profile-photo.jpg")
    cv_file = db.Column(db.String(255), default="CV-Aura-Pitaloka.pdf")
    status_badge = db.Column(db.String(100), default="Open to Work & Internship")
    
    # About Section
    about_title = db.Column(db.String(150), default="Tentang Saya")
    about_subtitle = db.Column(db.String(255), default="Dedikasi, Inovasi & Pembelajaran Berkelanjutan")
    about_p1 = db.Column(db.Text, nullable=True)
    about_p2 = db.Column(db.Text, nullable=True)
    
    # Contact & Socials
    email = db.Column(db.String(150), default="aurapitaloka04@gmail.com")
    phone = db.Column(db.String(50), default="+62 815-7513-2226")
    location = db.Column(db.String(150), default="Yogyakarta, Indonesia")
    github_url = db.Column(db.String(255), default="https://github.com/aurapitaloka")
    linkedin_url = db.Column(db.String(255), default="https://www.linkedin.com/in/aura-pitaloka-a00563247/")
    instagram_url = db.Column(db.String(255), default="https://instagram.com/aurapitaloka")
    footer_text = db.Column(db.String(255), default="© 2026 Aura Pitaloka. All rights reserved.")
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class AboutHighlight(db.Model):
    __tablename__ = 'about_highlights'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    icon = db.Column(db.String(100), default="fas fa-check-circle")
    order_num = db.Column(db.Integer, default=0)


class Skill(db.Model):
    __tablename__ = 'skills'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), default="General") # Frontend, Backend, Testing & QA, Tools, Database
    icon_class = db.Column(db.String(100), nullable=True) # e.g. fab fa-python, fas fa-database
    icon_svg_url = db.Column(db.String(255), nullable=True) # for devicon SVG URL or local SVG
    icon_color = db.Column(db.String(50), default="text-teal-400")
    proficiency = db.Column(db.Integer, default=85) # 1 - 100
    order_num = db.Column(db.Integer, default=0)


class Project(db.Model):
    __tablename__ = 'projects'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(100), default="Web Application") # QA / Testing, Web Application, Mobile, Desktop
    short_desc = db.Column(db.String(300), nullable=True)
    full_desc = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.String(255), nullable=True)
    tech_tags = db.Column(db.String(255), nullable=True) # Comma separated
    github_url = db.Column(db.String(255), nullable=True)
    demo_url = db.Column(db.String(255), nullable=True)
    
    # Document links (especially for QA / Capstone projects)
    prd_doc = db.Column(db.String(255), nullable=True)
    test_plan_doc = db.Column(db.String(255), nullable=True)
    test_design_doc = db.Column(db.String(255), nullable=True)
    qa_report_doc = db.Column(db.String(255), nullable=True)
    
    is_featured = db.Column(db.Boolean, default=False)
    order_num = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Experience(db.Model):
    __tablename__ = 'experiences'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False) # e.g. IT Solution Yogyakarta / UKM Pers
    role = db.Column(db.String(150), nullable=False) # e.g. Programmer, Pimpinan Umum
    category = db.Column(db.String(50), default="Pengalaman") # Magang, Organisasi, Pekerjaan
    period = db.Column(db.String(100), nullable=False) # e.g. 2025, 2023 - 2024
    description = db.Column(db.Text, nullable=False)
    tags = db.Column(db.String(255), nullable=True) # Comma separated skills/tags
    badge_color = db.Column(db.String(50), default="teal") # blue, teal, emerald, violet, amber
    order_num = db.Column(db.Integer, default=0)


class Certificate(db.Model):
    __tablename__ = 'certificates'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False) # e.g. Sertifikat Kejuaraan Code 5.0 - Juara 2
    issuer = db.Column(db.String(200), nullable=False) # e.g. Software Development Competition
    category = db.Column(db.String(100), default="Kompetisi") # Magang, Kompetisi, Kursus / Webinar
    year = db.Column(db.String(20), default="2025")
    image_url = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    credential_url = db.Column(db.String(255), nullable=True)
    order_num = db.Column(db.Integer, default=1)


class ContactMessage(db.Model):
    __tablename__ = 'contact_messages'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), nullable=False)
    subject = db.Column(db.String(200), nullable=True)
    message = db.Column(db.Text, nullable=False)
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

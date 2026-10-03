from app import app
from models import db, Profile, AboutHighlight, Skill, Project, Experience

def update_portfolio_content():
    with app.app_context():
        # 1. Update Profile & Hero
        profile = Profile.query.first()
        if not profile:
            profile = Profile()
            db.session.add(profile)

        profile.nav_brand = "AP"
        profile.full_name = "Aura Pitaloka, S.Kom."
        profile.badge_text = "👋 Halo, Saya Aura Pitaloka"
        profile.status_badge = "Open to Work • QA & Web Dev"
        profile.tagline = "Quality Assurance Engineer & Web Developer"
        profile.sub_tagline = "Fresh Graduate S1 Teknik Informatika (IPK 3.73 / Cumlaude)"
        profile.hero_description = (
            "Lulusan baru S1 Teknik Informatika Universitas Harkat Negeri dengan predikat Cumlaude (IPK 3.73). "
            "Berfokus pada penjaminan mutu perangkat lunak (Quality Assurance) berstandar internasional ISO/IEC 25010 "
            "serta perancangan aplikasi web modern yang andal, aman, responsif, dan siap produksi."
        )
        
        profile.about_title = "Profil & Latar Belakang"
        profile.about_subtitle = "Komitmen pada Mutu Perangkat Lunak, Ketelitian Pengujian & Rekayasa Web"
        profile.about_p1 = (
            "Saya adalah Fresh Graduate S1 Teknik Informatika di Universitas Harkat Negeri dengan capaian IPK 3.73 (Cumlaude). "
            "Saya memiliki ketertarikan mendalam serta keahlian praktis dalam siklus pengujian perangkat lunak (Software Testing Life Cycle - STLC), "
            "mulai dari analisis Product Requirement Document (PRD), penyusunan Test Plan dan Test Design, hingga eksekusi Test Case manual "
            "maupun terotomasi mengacu pada standar kualitas ISO/IEC 25010 (Functional Suitability, Performance Efficiency, Usability, dan Security)."
        )
        profile.about_p2 = (
            "Selain berfokus pada QA Engineering, saya juga berpengalaman dalam perancangan aplikasi web (Full-Stack Development) "
            "menggunakan Python (Flask), PHP (Laravel), MySQL, dan Tailwind CSS. Pengalaman magang profesional sebagai Programmer di IT Solution "
            "serta rekam jejak kepemimpinan sebagai Pimpinan Umum pers mahasiswa membekali saya dengan pola pikir analitis yang tajam, "
            "komunikasi lintas divisi yang efektif, dan perhatian tinggi terhadap detail dalam menghadirkan solusi teknologi bebas cacat (defect-free)."
        )

        profile.location = "Yogyakarta, Indonesia"
        profile.footer_text = "© 2026 Aura Pitaloka, S.Kom. • Quality Assurance & Web Development"

        # 2. Update About Highlights
        AboutHighlight.query.delete()
        new_highlights = [
            AboutHighlight(
                title="QA & Software Quality",
                description="Penguasaan metodologi STLC, standar kualitas ISO/IEC 25010, penyusunan Test Case komprehensif, dan automasi pengujian.",
                icon="fas fa-vial-circle-check",
                order_num=1
            ),
            AboutHighlight(
                title="Web & API Engineering",
                description="Pengembangan web modern berbasis Flask, Laravel, arsitektur RESTful API, dan optimasi basis data MySQL.",
                icon="fas fa-code",
                order_num=2
            ),
            AboutHighlight(
                title="Cumlaude & Leadership",
                description="Lulusan berprestasi dengan IPK 3.73, berjiwa kepemimpinan teruji dalam memimpin tim redaksi, komunikatif, dan berintegritas.",
                icon="fas fa-award",
                order_num=3
            ),
        ]
        db.session.bulk_save_objects(new_highlights)

        # 3. Update Skills with clear categories & high relevance to QA + Web
        Skill.query.delete()
        skills_data = [
            # QA & Testing
            {"name": "Katalon Studio", "category": "Testing & QA", "icon_class": "fas fa-vial-circle-check", "icon_color": "text-indigo-400", "proficiency": 92, "order": 1},
            {"name": "Manual Testing & STLC", "category": "Testing & QA", "icon_class": "fas fa-clipboard-check", "icon_color": "text-teal-400", "proficiency": 95, "order": 2},
            {"name": "Test Plan & Test Design", "category": "Testing & QA", "icon_class": "fas fa-file-shield", "icon_color": "text-emerald-400", "proficiency": 94, "order": 3},
            {"name": "ISO/IEC 25010 Quality", "category": "Testing & QA", "icon_class": "fas fa-certificate", "icon_color": "text-amber-400", "proficiency": 90, "order": 4},
            {"name": "Postman (API Testing)", "category": "Testing & QA", "icon_class": "fas fa-paper-plane", "icon_color": "text-orange-400", "proficiency": 88, "order": 5},
            
            # Backend & Database
            {"name": "Python", "category": "Backend", "icon_class": "fab fa-python", "icon_color": "text-blue-400", "proficiency": 88, "order": 6},
            {"name": "Flask", "category": "Backend", "icon_class": "fas fa-pepper-hot", "icon_color": "text-emerald-400", "proficiency": 86, "order": 7},
            {"name": "Laravel", "category": "Backend", "icon_class": "fab fa-laravel", "icon_color": "text-rose-500", "proficiency": 82, "order": 8},
            {"name": "MySQL", "category": "Database", "icon_class": "fas fa-database", "icon_color": "text-amber-400", "proficiency": 88, "order": 9},
            
            # Frontend
            {"name": "HTML5 & CSS3", "category": "Frontend", "icon_class": "fab fa-html5", "icon_color": "text-orange-500", "proficiency": 92, "order": 10},
            {"name": "JavaScript (ES6+)", "category": "Frontend", "icon_class": "fab fa-js", "icon_color": "text-yellow-400", "proficiency": 84, "order": 11},
            {"name": "Tailwind CSS", "category": "Frontend", "icon_class": "fab fa-css3-alt", "icon_color": "text-cyan-400", "proficiency": 90, "order": 12},

            # Mobile & Tools
            {"name": "Flutter", "category": "Mobile", "icon_svg_url": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/flutter/flutter-original.svg", "icon_color": "text-cyan-400", "proficiency": 78, "order": 13},
            {"name": "Git & GitHub", "category": "Tools", "icon_class": "fab fa-git-alt", "icon_color": "text-orange-500", "proficiency": 88, "order": 14},
            {"name": "Figma", "category": "UI/UX & Design", "icon_class": "fab fa-figma", "icon_color": "text-purple-400", "proficiency": 85, "order": 15},
        ]
        new_skills = [
            Skill(
                name=s['name'],
                category=s['category'],
                icon_class=s.get('icon_class'),
                icon_svg_url=s.get('icon_svg_url'),
                icon_color=s.get('icon_color', 'text-teal-400'),
                proficiency=s['proficiency'],
                order_num=s['order']
            ) for s in skills_data
        ]
        db.session.bulk_save_objects(new_skills)

        # 4. Refine Projects to highlight QA and software engineering excellence
        qa_project = Project.query.filter_by(order_num=1).first()
        if qa_project:
            qa_project.title = "QA Testing & ISO/IEC 25010 Quality Audit — Senja App"
            qa_project.category = "Quality Assurance"
            qa_project.short_desc = "Audit mutu perangkat lunak komprehensif berstandar ISO/IEC 25010 pada aplikasi tari tradisional berbasis AI."
            qa_project.full_desc = (
                "Melakukan quality assurance penuh pada Senja App, aplikasi edukasi tari tradisional Indonesia berbasis kecerdasan artifisial. "
                "Cakupan pengujian meliputi penyusunan Product Requirement Document (PRD), Test Plan, Test Design, serta eksekusi Test Case "
                "untuk 16+ modul fungsional (Screen Layout & Operation Test). Mengaudit kesesuaian sistem terhadap empat karakteristik ISO/IEC 25010: "
                "Functional Suitability, Performance Efficiency, Usability, dan Security yang menghasilkan defect analysis dan rekomendasi mitigasi komprehensif."
            )
            qa_project.tech_tags = "ISO/IEC 25010, Test Plan, Test Design, Manual Testing, Katalon Studio, PRD Analysis, QA Reporting"

        # 5. Commit changes
        db.session.commit()
        print("Database porto content successfully upgraded with fresh graduate (IPK 3.73) & professional QA profile!")

if __name__ == '__main__':
    update_portfolio_content()

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
        profile.status_badge = "Open to Work • QA & Software Engineer"
        profile.tagline = "Quality Assurance Engineer & Software Engineer"
        profile.sub_tagline = "Fresh Graduate D4 Teknik Informatika (IPK 3.73 / Cumlaude)"
        profile.hero_description = (
            "Fresh graduate D4 Teknik Informatika dengan predikat Cumlaude (IPK 3.73) yang berfokus pada Software Quality Assurance "
            "dan Software Engineering. Berpengalaman dalam automation testing (Katalon Studio, Postman) serta perancangan aplikasi "
            "multi-platform (Web, Mobile, Desktop) berstandar internasional ISO/IEC 25010."
        )
        
        profile.about_title = "Profil & Latar Belakang"
        profile.about_subtitle = "Komitmen pada Mutu Perangkat Lunak, Ketelitian Pengujian & Rekayasa Perangkat Lunak (Software Engineering)"
        profile.about_p1 = (
            "Saya adalah Fresh Graduate D4 Teknik Informatika di Universitas Harkat Negeri dengan capaian IPK 3.73 (Cumlaude). "
            "Saya memiliki ketertarikan mendalam serta keahlian praktis dalam siklus pengujian perangkat lunak (Software Testing Life Cycle - STLC), "
            "mulai dari analisis Product Requirement Document (PRD), penyusunan Test Plan dan Test Design, hingga eksekusi Test Case manual "
            "maupun terotomasi mengacu pada standar kualitas ISO/IEC 25010 (Functional Suitability, Performance Efficiency, Usability, dan Security)."
        )
        profile.about_p2 = (
            "Sebagai Software Engineer, saya terbiasa merancang dan mengembangkan sistem perangkat lunak yang modular, terstruktur, dan scalable "
            "(Python/Flask, PHP/Laravel, Flutter, Java) dengan integrasi RESTful API serta optimasi database. Prestasi Juara 2 Software Development "
            "Competition AMCC CODE 5.0 (2025) dan pengalaman magang sebagai Programmer di IT Solution memperkuat keahlian teknis saya. "
            "Pemahaman mendalam di sisi rekayasa perangkat lunak ini membuat saya memiliki perspektif menyeluruh dalam SDLC, "
            "sehingga jauh lebih peka dan tajam dalam mengidentifikasi potensi defect saat melakukan pengujian mutu (QA), didukung kemampuan analitis "
            "serta komunikasi tim yang efektif."
        )

        profile.location = "Tegal, Indonesia"
        profile.footer_text = "© 2026 Aura Pitaloka • Quality Assurance & Software Engineering"

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
                title="Software Engineering & Systems",
                description="Pengembangan sistem software yang handal, modular, dan clean code (Python, Laravel, Flutter, Java) dengan arsitektur RESTful API & optimasi database.",
                icon="fas fa-laptop-code",
                order_num=2
            ),
            AboutHighlight(
                title="Cumlaude & Analytical Mindset",
                description="Lulusan berprestasi D4 Teknik Informatika IPK 3.73, pemenang kompetisi software dev, berjiwa kepemimpinan, analitis, dan solutif.",
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

import os
import shutil
from flask import Flask
from config import Config
from models import db, User, Profile, AboutHighlight, Skill, Project, Experience, Certificate

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    return app

def setup_directories():
    base_upload = Config.UPLOAD_FOLDER
    dirs = [
        os.path.join(base_upload, 'profile'),
        os.path.join(base_upload, 'projects'),
        os.path.join(base_upload, 'certificates'),
        os.path.join(base_upload, 'docs')
    ]
    for d in dirs:
        os.makedirs(d, exist_ok=True)
    print("Upload directories verified in static/uploads/.")

def seed_data():
    app = create_app()
    with app.app_context():
        # Create all tables
        db.create_all()
        print("Database tables created successfully!")

        # 1. Admin User
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            admin = User(username='admin')
            admin.set_password('admin123')
            db.session.add(admin)
            print("Default admin user created (Username: admin, Password: admin123)")

        # 2. Profile
        profile = Profile.query.first()
        if not profile:
            profile = Profile(
                nav_brand="AP",
                full_name="Aura Pitaloka, S.Kom.",
                badge_text="👋 Halo, Saya Aura Pitaloka",
                status_badge="Open to Work • QA & Web Dev",
                tagline="Quality Assurance Engineer & Web Developer",
                sub_tagline="Fresh Graduate S1 Teknik Informatika (IPK 3.73 / Cumlaude)",
                hero_description="Lulusan baru S1 Teknik Informatika Universitas Harkat Negeri dengan predikat Cumlaude (IPK 3.73). Berfokus pada penjaminan mutu perangkat lunak (Quality Assurance) berstandar internasional ISO/IEC 25010 serta perancangan aplikasi web modern yang andal, aman, responsif, dan siap produksi.",
                avatar="profile-photo.jpg",
                cv_file="CV-Aura-Pitaloka.pdf",
                about_title="Profil & Latar Belakang",
                about_subtitle="Komitmen pada Mutu Perangkat Lunak, Ketelitian Pengujian & Rekayasa Web",
                about_p1="Saya adalah Fresh Graduate S1 Teknik Informatika di Universitas Harkat Negeri dengan capaian IPK 3.73 (Cumlaude). Saya memiliki ketertarikan mendalam serta keahlian praktis dalam siklus pengujian perangkat lunak (Software Testing Life Cycle - STLC), mulai dari analisis Product Requirement Document (PRD), penyusunan Test Plan dan Test Design, hingga eksekusi Test Case manual maupun terotomasi mengacu pada standar kualitas ISO/IEC 25010 (Functional Suitability, Performance Efficiency, Usability, dan Security).",
                about_p2="Selain berfokus pada QA Engineering, saya juga berpengalaman dalam perancangan aplikasi web (Full-Stack Development) menggunakan Python (Flask), PHP (Laravel), MySQL, dan Tailwind CSS. Pengalaman magang profesional sebagai Programmer di IT Solution serta rekam jejak kepemimpinan sebagai Pimpinan Umum pers mahasiswa membekali saya dengan pola pikir analitis yang tajam, komunikasi lintas divisi yang efektif, dan perhatian tinggi terhadap detail dalam menghadirkan solusi teknologi bebas cacat (defect-free).",
                email="aurapitaloka04@gmail.com",
                phone="+62 815-7513-2226",
                location="Yogyakarta, Indonesia",
                github_url="https://github.com/aurapitaloka",
                linkedin_url="https://www.linkedin.com/in/aura-pitaloka-a00563247/",
                instagram_url="https://instagram.com",
                footer_text="© 2026 Aura Pitaloka, S.Kom. • Quality Assurance & Web Development"
            )
            db.session.add(profile)
            print("Default profile seeded.")

        # 3. About Highlights
        if AboutHighlight.query.count() == 0:
            highlights = [
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
            db.session.bulk_save_objects(highlights)
            print("About highlights seeded.")

        # 4. Skills
        if Skill.query.count() == 0:
            skills_data = [
                {"name": "HTML5", "category": "Frontend", "icon_class": "fab fa-html5", "icon_color": "text-orange-500", "proficiency": 90, "order": 1},
                {"name": "CSS3 / Tailwind", "category": "Frontend", "icon_class": "fab fa-css3-alt", "icon_color": "text-blue-500", "proficiency": 88, "order": 2},
                {"name": "JavaScript", "category": "Frontend", "icon_class": "fab fa-js", "icon_color": "text-yellow-400", "proficiency": 82, "order": 3},
                {"name": "Python", "category": "Backend", "icon_class": "fab fa-python", "icon_color": "text-blue-400", "proficiency": 85, "order": 4},
                {"name": "Flask", "category": "Backend", "icon_class": "fas fa-pepper-hot", "icon_color": "text-emerald-400", "proficiency": 84, "order": 5},
                {"name": "Laravel", "category": "Backend", "icon_class": "fab fa-laravel", "icon_color": "text-red-500", "proficiency": 80, "order": 6},
                {"name": "MySQL", "category": "Database", "icon_class": "fas fa-database", "icon_color": "text-amber-400", "proficiency": 85, "order": 7},
                {"name": "Katalon Studio", "category": "Testing & QA", "icon_class": "fas fa-vial-circle-check", "icon_color": "text-indigo-400", "proficiency": 88, "order": 8},
                {"name": "Flutter", "category": "Mobile", "icon_svg_url": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/flutter/flutter-original.svg", "icon_color": "text-cyan-400", "proficiency": 75, "order": 9},
                {"name": "Figma", "category": "UI/UX & Design", "icon_class": "fab fa-figma", "icon_color": "text-purple-400", "proficiency": 85, "order": 10},
                {"name": "Canva", "category": "UI/UX & Design", "icon_class": "fas fa-palette", "icon_color": "text-pink-400", "proficiency": 90, "order": 11}
            ]
            skills_objs = [
                Skill(
                    name=s['name'], 
                    category=s['category'], 
                    icon_class=s.get('icon_class'), 
                    icon_svg_url=s.get('icon_svg_url'), 
                    icon_color=s['icon_color'], 
                    proficiency=s['proficiency'], 
                    order_num=s['order']
                ) for s in skills_data
            ]
            db.session.bulk_save_objects(skills_objs)
            print("Skills seeded.")

        # 5. Projects
        if Project.query.count() == 0:
            projects_data = [
                {
                    "title": "QA Testing — Senja App (Capstone Project)",
                    "category": "Quality Assurance",
                    "short_desc": "Pengujian QA komprehensif berstandar ISO/IEC 25010 pada aplikasi tari tradisional berbasis AI.",
                    "full_desc": "Melakukan quality assurance penuh pada Senja App, aplikasi pembelajaran tari tradisional berbasis AI, mulai dari penyusunan Product Requirement Document (PRD), Test Plan, Test Design, hingga eksekusi Test Case (mencakup Screen Layout & Operation Test untuk 16+ modul aplikasi) dan Laporan Hasil Pengujian mengacu pada standar ISO/IEC 25010 (Functional Suitability, Performance Efficiency, Usability, Security).",
                    "image_url": "qa-senja-app.png",
                    "tech_tags": "Test Plan, Manual Testing, ISO/IEC 25010, Requirement Analysis, Katalon",
                    "github_url": "",
                    "demo_url": "",
                    "prd_doc": "PRD-Senja-App.pdf",
                    "test_plan_doc": "Test-Plan-Senja-App.pdf",
                    "test_design_doc": "Test-Design-Senja-App.pdf",
                    "qa_report_doc": "Laporan-QA-ISO25010-Senja-App.pdf",
                    "is_featured": False,
                    "order_num": 1
                },
                {
                    "title": "SPK Pemilihan Maskapai Penerbangan",
                    "category": "Web Application",
                    "short_desc": "Sistem pendukung keputusan dengan metode Simple Additive Weighting (SAW) berbasis Laravel.",
                    "full_desc": "Mengembangkan sistem pendukung keputusan menggunakan metode SAW (Simple Additive Weighting) untuk membantu pemilihan maskapai penerbangan terbaik berdasarkan berbagai kriteria dan bobot prioritas. Dibangun menggunakan framework Laravel dan MySQL.",
                    "image_url": "2.png",
                    "tech_tags": "Laravel, PHP, MySQL, Tailwind CSS, Algoritma SAW",
                    "github_url": "https://github.com/aurapitaloka/SPK-SAW-PemWeb2.git",
                    "demo_url": "",
                    "is_featured": False,
                    "order_num": 2
                },
                {
                    "title": "Website Monitoring Pembelajaran Tari",
                    "category": "Web Application",
                    "short_desc": "Platform monitoring proses belajar tari dengan visualisasi progres dan evaluasi siswa.",
                    "full_desc": "Mengembangkan sistem monitoring pembelajaran tari berbasis web untuk membantu pengelolaan dan evaluasi proses belajar tari nusantara. Menggunakan Flask sebagai backend dan Firebase untuk realtime data sinkronisasi.",
                    "image_url": "1.png",
                    "tech_tags": "Flask, Python, Firebase, Bootstrap, REST API",
                    "github_url": "https://github.com/aurapitaloka/Web-Tari",
                    "demo_url": "",
                    "is_featured": False,
                    "order_num": 3
                },
                {
                    "title": "Game Petualangan Sang Pemburu Hutan",
                    "category": "Mobile Game",
                    "short_desc": "Game petualangan 2D/3D dengan gameplay eksplorasi karakter dan tantangan bertingkat.",
                    "full_desc": "Mengembangkan game petualangan berbasis Unity dengan beberapa level permainan, sistem poin, tantangan rintangan, dan mekanisme eksplorasi karakter yang interaktif.",
                    "image_url": "3.png",
                    "tech_tags": "Unity, C#, Mobile Game, Game Design",
                    "github_url": "https://github.com/aurapitaloka/Project-Game-Aura",
                    "demo_url": "",
                    "is_featured": False,
                    "order_num": 4
                },
                {
                    "title": "Aplikasi Kasir Desktop (Point of Sale)",
                    "category": "Desktop Application",
                    "short_desc": "Aplikasi POS desktop untuk manajemen inventaris barang dan pencatatan transaksi toko.",
                    "full_desc": "Mengembangkan aplikasi kasir desktop mandiri untuk membantu proses transaksi penjualan kasir, cetak struk, dan manajemen stok data barang secara terpusat.",
                    "image_url": "epic-electronik.png",
                    "tech_tags": "Java, Java Swing, MySQL, JDBC",
                    "github_url": "https://github.com/aurapitaloka/22090026-AuraPitaloka",
                    "demo_url": "",
                    "is_featured": False,
                    "order_num": 5
                },
                {
                    "title": "Aplikasi TIX CELL (Point of Sale Web)",
                    "category": "Web Application",
                    "short_desc": "Aplikasi POS web untuk transaksi pulsa, paket data, dan layanan konter seluler.",
                    "full_desc": "Mengembangkan aplikasi berbasis web untuk mendukung pengelolaan layanan, stok voucer, dan transaksi harian pada usaha konter TIX CELL dengan backend Flask.",
                    "image_url": "5.png",
                    "tech_tags": "Flask, Python, MySQL, HTML5, CSS3",
                    "github_url": "https://github.com/aurapitaloka/POS-TixCell",
                    "demo_url": "",
                    "is_featured": False,
                    "order_num": 6
                },
                {
                    "title": "Aplikasi Kasir FreshBox",
                    "category": "Web Application",
                    "short_desc": "Aplikasi kasir online pencatatan penjualan dan pesanan produk segar pelanggan.",
                    "full_desc": "Mengembangkan aplikasi kasir berbasis web untuk membantu pencatatan transaksi dan pengelolaan data penjualan serta pemesanan produk customer FreshBox secara real-time.",
                    "image_url": "4.png",
                    "tech_tags": "JavaScript, Firebase, HTML5, CSS3",
                    "github_url": "https://github.com/aurapitaloka/POS-FreshBox",
                    "demo_url": "",
                    "is_featured": False,
                    "order_num": 7
                }
            ]
            for p in projects_data:
                proj = Project(
                    title=p['title'],
                    category=p['category'],
                    short_desc=p.get('short_desc'),
                    full_desc=p['full_desc'],
                    image_url=p['image_url'],
                    tech_tags=p['tech_tags'],
                    github_url=p.get('github_url'),
                    demo_url=p.get('demo_url'),
                    prd_doc=p.get('prd_doc'),
                    test_plan_doc=p.get('test_plan_doc'),
                    test_design_doc=p.get('test_design_doc'),
                    qa_report_doc=p.get('qa_report_doc'),
                    is_featured=p.get('is_featured', False),
                    order_num=p['order_num']
                )
                db.session.add(proj)
            print("Projects seeded.")

        # 6. Experiences
        if Experience.query.count() == 0:
            experiences_data = [
                {
                    "title": "IT Solution Yogyakarta",
                    "role": "Programmer (Magang)",
                    "category": "Magang",
                    "period": "2025",
                    "description": "Sebagai programmer di IT Solution, saya bertanggung jawab untuk mengembangkan dan memelihara aplikasi web menggunakan teknologi modern. Fokus utama saya adalah membuat solusi yang efisien, aman, dan user-friendly untuk kebutuhan klien.",
                    "tags": "Web Development, Programming, Problem Solving, Team Collaboration",
                    "badge_color": "blue",
                    "order_num": 1
                },
                {
                    "title": "Unit Kegiatan Mahasiswa Pers Semata",
                    "role": "Pimpinan Umum",
                    "category": "Organisasi",
                    "period": "2023 - 2024",
                    "description": "Memimpin dan mengelola tim redaksi, bertanggung jawab atas pembagian delegasi tugas, pemantauan kinerja anggota tim, serta menyunting dan menyetujui seluruh publikasi media organisasi.",
                    "tags": "Leadership, Strategic Planning, Event Management, Communication",
                    "badge_color": "teal",
                    "order_num": 2
                },
                {
                    "title": "Forum Riset Teknologi",
                    "role": "Anggota Aktif",
                    "category": "Organisasi",
                    "period": "2022 - 2023",
                    "description": "Aktif dalam diskusi riset kelompok untuk menggali dan mengembangkan ide kreatif teknologi tepat guna, berperan dalam penyusunan proposal riset, serta analisis kebutuhan implementasi sistem informasi.",
                    "tags": "Teamwork, Technology Research, Analytical Thinking",
                    "badge_color": "teal",
                    "order_num": 3
                }
            ]
            for exp in experiences_data:
                e = Experience(
                    title=exp['title'],
                    role=exp['role'],
                    category=exp['category'],
                    period=exp['period'],
                    description=exp['description'],
                    tags=exp['tags'],
                    badge_color=exp['badge_color'],
                    order_num=exp['order_num']
                )
                db.session.add(e)
            print("Experiences seeded.")

        # 7. Certificates
        if Certificate.query.count() == 0:
            certs_data = [
                {
                    "title": "Sertifikat Magang Programmer",
                    "issuer": "IT Solution Yogyakarta",
                    "category": "Magang",
                    "year": "2025",
                    "image_url": "sertifikat.jpg",
                    "description": "Sertifikat penyelesaian program magang profesional sebagai Programmer di IT Solution Yogyakarta.",
                    "order_num": 1
                },
                {
                    "title": "Sertifikat Kejuaraan Code 5.0 (Juara 2)",
                    "issuer": "Software Development Competition",
                    "category": "Kompetisi",
                    "year": "2025",
                    "image_url": "sertifikat-2.png",
                    "description": "Juara 2 pada ajang kompetisi pengembangan perangkat lunak tingkat regional/nasional Code 5.0.",
                    "order_num": 2
                },
                {
                    "title": "Certificate of Completion — Big Data Management",
                    "issuer": "Basics of NoSQL & NewSQL Big Data Management",
                    "category": "Pelatihan",
                    "year": "2025",
                    "image_url": "sertif3.png",
                    "description": "Sertifikat kompetensi pengelolaan database modern berskala besar (NoSQL & NewSQL architecture).",
                    "order_num": 3
                },
                {
                    "title": "Certificate of Completion — AI Technology & Application",
                    "issuer": "Artificial Intelligence Technology and Application",
                    "category": "Pelatihan",
                    "year": "2025",
                    "image_url": "sertif4.png",
                    "description": "Pelatihan intensif implementasi algoritma kecerdasan buatan dan integrasi model machine learning.",
                    "order_num": 4
                },
                {
                    "title": "Certificate of Completion — Overview of AI",
                    "issuer": "AI Basics: Foundational AI Principles",
                    "category": "Pelatihan",
                    "year": "2025",
                    "image_url": "sertif.png",
                    "description": "Sertifikasi pemahaman dasar konsep kecerdasan artifisial, etika data, dan pipeline AI.",
                    "order_num": 5
                }
            ]
            for c in certs_data:
                cert = Certificate(
                    title=c['title'],
                    issuer=c['issuer'],
                    category=c['category'],
                    year=c['year'],
                    image_url=c['image_url'],
                    description=c.get('description'),
                    order_num=c['order_num']
                )
                db.session.add(cert)
            print("Certificates seeded.")

        db.session.commit()
        print("All data successfully seeded into MySQL porto database!")

if __name__ == '__main__':
    setup_directories()
    seed_data()

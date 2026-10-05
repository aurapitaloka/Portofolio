import os
import time
from functools import wraps
from flask import (
    Flask, render_template, request, redirect, url_for, flash, 
    session, jsonify, send_from_directory, abort
)
from werkzeug.utils import secure_filename
from config import Config
from models import (
    db, User, Profile, AboutHighlight, Skill, Project, 
    Experience, Certificate, ContactMessage
)

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

# Helper function to check allowed file extensions
def allowed_file(filename, allowed_types):
    if '.' not in filename:
        return False
    ext = filename.rsplit('.', 1)[1].lower()
    return ext in allowed_types

def save_uploaded_file(file_storage, subfolder, allowed_types):
    if not file_storage or file_storage.filename == '':
        return None
    if not allowed_file(file_storage.filename, allowed_types):
        return None
    
    filename = secure_filename(file_storage.filename)
    timestamp = int(time.time())
    unique_filename = f"{timestamp}_{filename}"
    
    target_dir = os.path.join(app.config['UPLOAD_FOLDER'], subfolder)
    os.makedirs(target_dir, exist_ok=True)
    
    file_path = os.path.join(target_dir, unique_filename)
    file_storage.save(file_path)
    return unique_filename

# Authentication Decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Silakan login terlebih dahulu untuk mengakses panel admin.', 'warning')
            return redirect(url_for('admin_login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

# Context processor for global template variables (e.g. unread messages count)
@app.context_processor
def inject_global_data():
    profile = Profile.query.first()
    unread_messages = 0
    if 'user_id' in session:
        unread_messages = ContactMessage.query.filter_by(is_read=False).count()
    return dict(profile_data=profile, unread_count=unread_messages)

# ==========================================
# PUBLIC FRONTEND ROUTES
# ==========================================

@app.route('/')
def index():
    profile = Profile.query.first()
    if not profile:
        # Fallback if DB empty
        profile = Profile()
        db.session.add(profile)
        db.session.commit()
        
    highlights = AboutHighlight.query.order_by(AboutHighlight.order_num.asc()).all()
    skills = Skill.query.order_by(Skill.order_num.asc()).all()
    
    # Group skills by category for nice modern display tabs or badges
    skill_categories = sorted(list(set(s.category for s in skills if s.category)))
    
    projects = Project.query.order_by(Project.order_num.asc(), Project.id.asc()).all()
    project_categories = sorted(list(set(p.category for p in projects if p.category)))
    project_counts = {cat: 0 for cat in project_categories}
    for p in projects:
        if p.category in project_counts:
            project_counts[p.category] += 1
    
    experiences = Experience.query.order_by(Experience.order_num.asc()).all()
    certificates = Certificate.query.order_by(Certificate.order_num.asc()).all()
    
    return render_template(
        'index.html',
        profile=profile,
        highlights=highlights,
        skills=skills,
        skill_categories=skill_categories,
        projects=projects,
        project_categories=project_categories,
        project_counts=project_counts,
        experiences=experiences,
        certificates=certificates
    )

@app.route('/uploads/<path:subfolder>/<path:filename>')
def serve_upload(subfolder, filename):
    folder = os.path.join(app.config['UPLOAD_FOLDER'], subfolder)
    return send_from_directory(folder, filename)

@app.route('/api/contact', methods=['POST'])
def contact_submit():
    try:
        # Support both JSON payload and regular form submission
        if request.is_json:
            data = request.get_json()
            name = data.get('name', '').strip()
            email = data.get('email', '').strip()
            subject = data.get('subject', 'Pesan dari Portofolio').strip()
            message = data.get('message', '').strip()
        else:
            name = request.form.get('name', '').strip()
            email = request.form.get('email', '').strip()
            subject = request.form.get('subject', 'Pesan dari Portofolio').strip()
            message = request.form.get('message', '').strip()

        if not name or not email or not message:
            return jsonify({'success': False, 'message': 'Semua kolom wajib diisi!'}), 400

        msg = ContactMessage(
            name=name,
            email=email,
            subject=subject,
            message=message
        )
        db.session.add(msg)
        db.session.commit()

        return jsonify({'success': True, 'message': 'Pesan Anda berhasil terkirim! Terima kasih telah menghubungi.'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'Terjadi kesalahan: {str(e)}'}), 500


# ==========================================
# ADMIN AUTHENTICATION
# ==========================================

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if 'user_id' in session:
        return redirect(url_for('admin_dashboard'))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()

        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            session['user_id'] = user.id
            session['username'] = user.username
            flash(f'Selamat datang kembali, {user.username}!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page or url_for('admin_dashboard'))
        else:
            flash('Username atau password salah. Silakan coba lagi.', 'danger')

    return render_template('admin/login.html')

@app.route('/admin/logout')
def admin_logout():
    session.clear()
    flash('Anda telah berhasil keluar (logout).', 'info')
    return redirect(url_for('admin_login'))


# ==========================================
# ADMIN DASHBOARD & CONTENT MANAGEMENT
# ==========================================

@app.route('/admin')
@app.route('/admin/dashboard')
@login_required
def admin_dashboard():
    stats = {
        'projects': Project.query.count(),
        'skills': Skill.query.count(),
        'experiences': Experience.query.count(),
        'certificates': Certificate.query.count(),
        'messages': ContactMessage.query.count(),
        'unread_messages': ContactMessage.query.filter_by(is_read=False).count()
    }
    recent_messages = ContactMessage.query.order_by(ContactMessage.created_at.desc()).limit(5).all()
    latest_projects = Project.query.order_by(Project.created_at.desc()).limit(4).all()
    
    return render_template('admin/dashboard.html', stats=stats, recent_messages=recent_messages, latest_projects=latest_projects)


# 1. PROFILE & SITE IDENTITY
@app.route('/admin/profile', methods=['GET', 'POST'])
@login_required
def admin_profile():
    profile = Profile.query.first()
    if not profile:
        profile = Profile()
        db.session.add(profile)
        db.session.commit()

    if request.method == 'POST':
        # Hero Section
        profile.nav_brand = request.form.get('nav_brand', 'AP').strip()
        profile.badge_text = request.form.get('badge_text', '').strip()
        profile.full_name = request.form.get('full_name', '').strip()
        profile.tagline = request.form.get('tagline', '').strip()
        profile.sub_tagline = request.form.get('sub_tagline', '').strip()
        profile.hero_description = request.form.get('hero_description', '').strip()
        profile.status_badge = request.form.get('status_badge', '').strip()

        # About Section
        profile.about_title = request.form.get('about_title', 'Tentang Saya').strip()
        profile.about_subtitle = request.form.get('about_subtitle', '').strip()
        profile.about_p1 = request.form.get('about_p1', '').strip()
        profile.about_p2 = request.form.get('about_p2', '').strip()

        # Contact & Socials
        profile.email = request.form.get('email', '').strip()
        profile.phone = request.form.get('phone', '').strip()
        profile.location = request.form.get('location', '').strip()
        profile.github_url = request.form.get('github_url', '').strip()
        profile.linkedin_url = request.form.get('linkedin_url', '').strip()
        profile.instagram_url = request.form.get('instagram_url', '').strip()
        profile.footer_text = request.form.get('footer_text', '').strip()

        # Handle Profile Photo Upload
        if 'avatar_file' in request.files:
            avatar = save_uploaded_file(request.files['avatar_file'], 'profile', Config.ALLOWED_IMAGE_EXTENSIONS)
            if avatar:
                profile.avatar = avatar

        # Handle CV Upload
        if 'cv_file' in request.files:
            cv = save_uploaded_file(request.files['cv_file'], 'profile', Config.ALLOWED_DOC_EXTENSIONS)
            if cv:
                profile.cv_file = cv

        db.session.commit()
        flash('Data profil & informasi website berhasil diperbarui!', 'success')
        return redirect(url_for('admin_profile'))

    highlights = AboutHighlight.query.order_by(AboutHighlight.order_num.asc()).all()
    return render_template('admin/profile.html', profile=profile, highlights=highlights)


# 2. ABOUT HIGHLIGHTS CRUD
@app.route('/admin/highlights/add', methods=['POST'])
@login_required
def admin_add_highlight():
    title = request.form.get('title', '').strip()
    description = request.form.get('description', '').strip()
    icon = request.form.get('icon', 'fas fa-check-circle').strip()
    order_num = int(request.form.get('order_num', 0))

    if title and description:
        hl = AboutHighlight(title=title, description=description, icon=icon, order_num=order_num)
        db.session.add(hl)
        db.session.commit()
        flash('Kelebihan / Highlight baru berhasil ditambahkan!', 'success')
    return redirect(url_for('admin_profile'))

@app.route('/admin/highlights/delete/<int:id>', methods=['POST'])
@login_required
def admin_delete_highlight(id):
    hl = AboutHighlight.query.get_or_404(id)
    db.session.delete(hl)
    db.session.commit()
    flash('Highlight berhasil dihapus.', 'info')
    return redirect(url_for('admin_profile'))


# 3. SKILLS MANAGEMENT
@app.route('/admin/skills', methods=['GET', 'POST'])
@login_required
def admin_skills():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        category = request.form.get('category', 'General').strip()
        icon_class = request.form.get('icon_class', '').strip()
        icon_svg_url = request.form.get('icon_svg_url', '').strip()
        icon_color = request.form.get('icon_color', 'text-teal-400').strip()
        proficiency = int(request.form.get('proficiency', 80))
        order_num = int(request.form.get('order_num', 0))

        if name:
            skill = Skill(
                name=name,
                category=category,
                icon_class=icon_class,
                icon_svg_url=icon_svg_url,
                icon_color=icon_color,
                proficiency=proficiency,
                order_num=order_num
            )
            db.session.add(skill)
            db.session.commit()
            flash(f'Skill "{name}" berhasil ditambahkan!', 'success')
            return redirect(url_for('admin_skills'))

    skills = Skill.query.order_by(Skill.category.asc(), Skill.order_num.asc()).all()
    categories = sorted(list(set(s.category for s in skills if s.category)))
    return render_template('admin/skills.html', skills=skills, categories=categories)

@app.route('/admin/skills/edit/<int:id>', methods=['POST'])
@login_required
def admin_edit_skill(id):
    skill = Skill.query.get_or_404(id)
    skill.name = request.form.get('name', skill.name).strip()
    skill.category = request.form.get('category', skill.category).strip()
    skill.icon_class = request.form.get('icon_class', skill.icon_class).strip()
    skill.icon_svg_url = request.form.get('icon_svg_url', skill.icon_svg_url).strip()
    skill.icon_color = request.form.get('icon_color', skill.icon_color).strip()
    skill.proficiency = int(request.form.get('proficiency', skill.proficiency))
    skill.order_num = int(request.form.get('order_num', skill.order_num))

    db.session.commit()
    flash(f'Skill "{skill.name}" berhasil diperbarui!', 'success')
    return redirect(url_for('admin_skills'))

@app.route('/admin/skills/delete/<int:id>', methods=['POST'])
@login_required
def admin_delete_skill(id):
    skill = Skill.query.get_or_404(id)
    db.session.delete(skill)
    db.session.commit()
    flash('Skill berhasil dihapus.', 'info')
    return redirect(url_for('admin_skills'))


# 4. PROJECTS MANAGEMENT
@app.route('/admin/projects')
@login_required
def admin_projects():
    projects = Project.query.order_by(Project.order_num.asc(), Project.id.asc()).all()
    return render_template('admin/projects.html', projects=projects)

@app.route('/admin/projects/add', methods=['GET', 'POST'])
@login_required
def admin_add_project():
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        category = request.form.get('category', 'Web Application').strip()
        short_desc = request.form.get('short_desc', '').strip()
        full_desc = request.form.get('full_desc', '').strip()
        tech_tags = request.form.get('tech_tags', '').strip()
        github_url = request.form.get('github_url', '').strip()
        demo_url = request.form.get('demo_url', '').strip()
        is_featured = bool(request.form.get('is_featured'))
        
        # Safe order_num parsing (default to next available slot)
        raw_order = request.form.get('order_num', '').strip()
        if raw_order:
            try:
                order_num = int(raw_order)
            except ValueError:
                order_num = 1
        else:
            max_order = db.session.query(db.func.max(Project.order_num)).scalar() or 0
            order_num = max_order + 1

        # Handle Cover Image Upload
        image_url = None
        if 'image_file' in request.files:
            image_url = save_uploaded_file(request.files['image_file'], 'projects', Config.ALLOWED_IMAGE_EXTENSIONS)

        # Handle Documents Upload
        prd_doc = save_uploaded_file(request.files.get('prd_doc_file'), 'docs', Config.ALLOWED_DOC_EXTENSIONS) if 'prd_doc_file' in request.files else None
        test_plan_doc = save_uploaded_file(request.files.get('test_plan_file'), 'docs', Config.ALLOWED_DOC_EXTENSIONS) if 'test_plan_file' in request.files else None
        test_design_doc = save_uploaded_file(request.files.get('test_design_file'), 'docs', Config.ALLOWED_DOC_EXTENSIONS) if 'test_design_file' in request.files else None
        qa_report_doc = save_uploaded_file(request.files.get('qa_report_file'), 'docs', Config.ALLOWED_DOC_EXTENSIONS) if 'qa_report_file' in request.files else None

        proj = Project(
            title=title,
            category=category,
            short_desc=short_desc,
            full_desc=full_desc,
            image_url=image_url or "spredsheet.png",
            tech_tags=tech_tags,
            github_url=github_url,
            demo_url=demo_url,
            prd_doc=prd_doc,
            test_plan_doc=test_plan_doc,
            test_design_doc=test_design_doc,
            qa_report_doc=qa_report_doc,
            is_featured=is_featured,
            order_num=order_num
        )
        db.session.add(proj)
        db.session.commit()
        flash(f'Projek "{title}" berhasil ditambahkan dengan nomor urut #{order_num}!', 'success')
        return redirect(url_for('admin_projects'))

    # Calculate default next order for the form
    max_order = db.session.query(db.func.max(Project.order_num)).scalar() or 0
    next_order = max_order + 1
    return render_template('admin/project_form.html', project=None, default_order=next_order)

@app.route('/admin/projects/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def admin_edit_project(id):
    proj = Project.query.get_or_404(id)
    if request.method == 'POST':
        proj.title = request.form.get('title', proj.title).strip()
        proj.category = request.form.get('category', proj.category).strip()
        proj.short_desc = request.form.get('short_desc', proj.short_desc).strip()
        proj.full_desc = request.form.get('full_desc', proj.full_desc).strip()
        proj.tech_tags = request.form.get('tech_tags', proj.tech_tags).strip()
        proj.github_url = request.form.get('github_url', proj.github_url).strip()
        proj.demo_url = request.form.get('demo_url', proj.demo_url).strip()
        proj.is_featured = bool(request.form.get('is_featured'))
        
        raw_order = request.form.get('order_num', '').strip()
        if raw_order:
            try:
                proj.order_num = int(raw_order)
            except ValueError:
                pass

        if 'image_file' in request.files:
            new_img = save_uploaded_file(request.files['image_file'], 'projects', Config.ALLOWED_IMAGE_EXTENSIONS)
            if new_img:
                proj.image_url = new_img

        if 'prd_doc_file' in request.files:
            doc = save_uploaded_file(request.files['prd_doc_file'], 'docs', Config.ALLOWED_DOC_EXTENSIONS)
            if doc: proj.prd_doc = doc

        if 'test_plan_file' in request.files:
            doc = save_uploaded_file(request.files['test_plan_file'], 'docs', Config.ALLOWED_DOC_EXTENSIONS)
            if doc: proj.test_plan_doc = doc

        if 'test_design_file' in request.files:
            doc = save_uploaded_file(request.files['test_design_file'], 'docs', Config.ALLOWED_DOC_EXTENSIONS)
            if doc: proj.test_design_doc = doc

        if 'qa_report_file' in request.files:
            doc = save_uploaded_file(request.files['qa_report_file'], 'docs', Config.ALLOWED_DOC_EXTENSIONS)
            if doc: proj.qa_report_doc = doc

        db.session.commit()
        flash(f'Projek "{proj.title}" berhasil diperbarui!', 'success')
        return redirect(url_for('admin_projects'))

    return render_template('admin/project_form.html', project=proj, default_order=proj.order_num)

@app.route('/admin/projects/move/<int:id>/<string:direction>', methods=['POST'])
@login_required
def admin_move_project(id, direction):
    # Fetch all projects in order
    projects = Project.query.order_by(Project.order_num.asc(), Project.id.asc()).all()
    # Normalize order_num sequentially (1, 2, 3...)
    for idx, p in enumerate(projects, start=1):
        p.order_num = idx
    db.session.commit()

    current_idx = None
    for i, p in enumerate(projects):
        if p.id == id:
            current_idx = i
            break

    if current_idx is not None:
        if direction == 'up' and current_idx > 0:
            target_p = projects[current_idx]
            prev_p = projects[current_idx - 1]
            target_p.order_num, prev_p.order_num = prev_p.order_num, target_p.order_num
            db.session.commit()
            flash(f'Urutan "{target_p.title}" berhasil dinaikkan ke #{target_p.order_num}.', 'success')
        elif direction == 'down' and current_idx < len(projects) - 1:
            target_p = projects[current_idx]
            next_p = projects[current_idx + 1]
            target_p.order_num, next_p.order_num = next_p.order_num, target_p.order_num
            db.session.commit()
            flash(f'Urutan "{target_p.title}" berhasil diturunkan ke #{target_p.order_num}.', 'success')

    return redirect(url_for('admin_projects'))

@app.route('/admin/projects/renumber', methods=['POST'])
@login_required
def admin_renumber_projects():
    projects = Project.query.order_by(Project.order_num.asc(), Project.id.asc()).all()
    for idx, p in enumerate(projects, start=1):
        p.order_num = idx
    db.session.commit()
    flash('Semua nomor urut projek telah dirapikan menjadi berurutan (1, 2, 3...).', 'success')
    return redirect(url_for('admin_projects'))

@app.route('/admin/projects/delete/<int:id>', methods=['POST'])
@login_required
def admin_delete_project(id):
    proj = Project.query.get_or_404(id)
    title = proj.title
    db.session.delete(proj)
    db.session.commit()
    flash(f'Projek "{title}" telah dihapus.', 'info')
    return redirect(url_for('admin_projects'))


# 5. EXPERIENCES MANAGEMENT (Magang, Organisasi, dll.)
@app.route('/admin/experiences', methods=['GET', 'POST'])
@login_required
def admin_experiences():
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        role = request.form.get('role', '').strip()
        category = request.form.get('category', 'Pengalaman').strip()
        period = request.form.get('period', '').strip()
        description = request.form.get('description', '').strip()
        tags = request.form.get('tags', '').strip()
        badge_color = request.form.get('badge_color', 'teal').strip()
        order_num = int(request.form.get('order_num', 0))

        if title and role:
            exp = Experience(
                title=title,
                role=role,
                category=category,
                period=period,
                description=description,
                tags=tags,
                badge_color=badge_color,
                order_num=order_num
            )
            db.session.add(exp)
            db.session.commit()
            flash(f'Pengalaman di "{title}" berhasil ditambahkan!', 'success')
            return redirect(url_for('admin_experiences'))

    experiences = Experience.query.order_by(Experience.order_num.asc()).all()
    return render_template('admin/experiences.html', experiences=experiences)

@app.route('/admin/experiences/edit/<int:id>', methods=['POST'])
@login_required
def admin_edit_experience(id):
    exp = Experience.query.get_or_404(id)
    exp.title = request.form.get('title', exp.title).strip()
    exp.role = request.form.get('role', exp.role).strip()
    exp.category = request.form.get('category', exp.category).strip()
    exp.period = request.form.get('period', exp.period).strip()
    exp.description = request.form.get('description', exp.description).strip()
    exp.tags = request.form.get('tags', exp.tags).strip()
    exp.badge_color = request.form.get('badge_color', exp.badge_color).strip()
    exp.order_num = int(request.form.get('order_num', exp.order_num))

    db.session.commit()
    flash(f'Pengalaman "{exp.title}" berhasil diperbarui!', 'success')
    return redirect(url_for('admin_experiences'))

@app.route('/admin/experiences/delete/<int:id>', methods=['POST'])
@login_required
def admin_delete_experience(id):
    exp = Experience.query.get_or_404(id)
    db.session.delete(exp)
    db.session.commit()
    flash('Pengalaman telah dihapus.', 'info')
    return redirect(url_for('admin_experiences'))


def resequence_certificates(target_cert=None, target_order=None):
    """
    Pastikan semua sertifikat berurutan rapi dari 1 sampai N tanpa angka 0, negatif, atau duplikat.
    Jika target_cert dan target_order diberikan, tempatkan target_cert pada urutan tersebut.
    """
    certs = Certificate.query.order_by(Certificate.order_num.asc(), Certificate.id.asc()).all()
    if target_cert and target_order is not None:
        certs = [c for c in certs if c.id != target_cert.id]
        insert_idx = max(0, min(int(target_order) - 1, len(certs)))
        certs.insert(insert_idx, target_cert)
    for idx, c in enumerate(certs, start=1):
        c.order_num = idx
    db.session.commit()


# 6. CERTIFICATES MANAGEMENT
@app.route('/admin/certificates', methods=['GET', 'POST'])
@login_required
def admin_certificates():
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        issuer = request.form.get('issuer', '').strip()
        category = request.form.get('category', 'Sertifikasi').strip()
        year = request.form.get('year', '2025').strip()
        description = request.form.get('description', '').strip()
        credential_url = request.form.get('credential_url', '').strip()
        try:
            order_num = int(request.form.get('order_num', 1))
        except (ValueError, TypeError):
            order_num = 1
        if order_num < 1:
            order_num = 1

        image_url = None
        if 'image_file' in request.files:
            image_url = save_uploaded_file(request.files['image_file'], 'certificates', Config.ALLOWED_IMAGE_EXTENSIONS)

        if title and issuer:
            cert = Certificate(
                title=title,
                issuer=issuer,
                category=category,
                year=year,
                image_url=image_url or "sertifikat.jpg",
                description=description,
                credential_url=credential_url,
                order_num=order_num
            )
            db.session.add(cert)
            db.session.flush()
            resequence_certificates(target_cert=cert, target_order=order_num)
            flash(f'Sertifikat "{title}" berhasil ditambahkan pada urutan #{cert.order_num}!', 'success')
            return redirect(url_for('admin_certificates'))

    certificates = Certificate.query.order_by(Certificate.order_num.asc(), Certificate.id.asc()).all()
    # Pastikan urutan selalu bersih 1..N
    resequence_needed = any(c.order_num != i for i, c in enumerate(certificates, start=1))
    if resequence_needed:
        resequence_certificates()
        certificates = Certificate.query.order_by(Certificate.order_num.asc(), Certificate.id.asc()).all()

    next_order = len(certificates) + 1
    return render_template('admin/certificates.html', certificates=certificates, next_order=next_order)

@app.route('/admin/certificates/edit/<int:id>', methods=['POST'])
@login_required
def admin_edit_certificate(id):
    cert = Certificate.query.get_or_404(id)
    cert.title = request.form.get('title', cert.title).strip()
    cert.issuer = request.form.get('issuer', cert.issuer).strip()
    cert.category = request.form.get('category', cert.category).strip()
    cert.year = request.form.get('year', cert.year).strip()
    cert.description = request.form.get('description', cert.description).strip()
    cert.credential_url = request.form.get('credential_url', cert.credential_url).strip()
    
    try:
        new_order = int(request.form.get('order_num', cert.order_num))
    except (ValueError, TypeError):
        new_order = cert.order_num
    if new_order < 1:
        new_order = 1

    if 'image_file' in request.files:
        new_img = save_uploaded_file(request.files['image_file'], 'certificates', Config.ALLOWED_IMAGE_EXTENSIONS)
        if new_img:
            cert.image_url = new_img

    resequence_certificates(target_cert=cert, target_order=new_order)
    flash(f'Sertifikat "{cert.title}" berhasil diperbarui (Urutan #{cert.order_num})!', 'success')
    return redirect(url_for('admin_certificates'))

@app.route('/admin/certificates/reorder/<int:id>/<string:direction>', methods=['POST'])
@login_required
def admin_reorder_certificate(id, direction):
    cert = Certificate.query.get_or_404(id)
    certs = Certificate.query.order_by(Certificate.order_num.asc(), Certificate.id.asc()).all()
    
    # Pastikan resequence rapi 1..N
    for idx, c in enumerate(certs, start=1):
        c.order_num = idx
    db.session.commit()
    
    current_idx = None
    for idx, c in enumerate(certs):
        if c.id == cert.id:
            current_idx = idx
            break
            
    if current_idx is not None:
        if direction == 'up' and current_idx > 0:
            target = certs[current_idx - 1]
            certs[current_idx].order_num, target.order_num = target.order_num, certs[current_idx].order_num
            db.session.commit()
            flash(f'Urutan "{cert.title}" berhasil dinaikkan ke posisi #{certs[current_idx].order_num}!', 'success')
        elif direction == 'down' and current_idx < len(certs) - 1:
            target = certs[current_idx + 1]
            certs[current_idx].order_num, target.order_num = target.order_num, certs[current_idx].order_num
            db.session.commit()
            flash(f'Urutan "{cert.title}" berhasil diturunkan ke posisi #{certs[current_idx].order_num}!', 'success')
            
    return redirect(url_for('admin_certificates'))

@app.route('/admin/certificates/delete/<int:id>', methods=['POST'])
@login_required
def admin_delete_certificate(id):
    cert = Certificate.query.get_or_404(id)
    title = cert.title
    db.session.delete(cert)
    db.session.flush()
    resequence_certificates()
    flash(f'Sertifikat "{title}" berhasil dihapus.', 'info')
    return redirect(url_for('admin_certificates'))


# 7. INBOX MESSAGES
@app.route('/admin/messages')
@login_required
def admin_messages():
    messages = ContactMessage.query.order_by(ContactMessage.created_at.desc()).all()
    return render_template('admin/messages.html', messages=messages)

@app.route('/admin/messages/toggle-read/<int:id>', methods=['POST'])
@login_required
def admin_toggle_message_read(id):
    msg = ContactMessage.query.get_or_404(id)
    msg.is_read = not msg.is_read
    db.session.commit()
    return jsonify({'success': True, 'is_read': msg.is_read})

@app.route('/admin/messages/delete/<int:id>', methods=['POST'])
@login_required
def admin_delete_message(id):
    msg = ContactMessage.query.get_or_404(id)
    db.session.delete(msg)
    db.session.commit()
    flash('Pesan berhasil dihapus.', 'info')
    return redirect(url_for('admin_messages'))


# 8. ACCOUNT SETTINGS (Ubah Password & Username)
@app.route('/admin/account', methods=['GET', 'POST'])
@login_required
def admin_account():
    user = User.query.get(session['user_id'])
    if request.method == 'POST':
        new_username = request.form.get('username', '').strip()
        current_password = request.form.get('current_password', '')
        new_password = request.form.get('new_password', '')
        confirm_password = request.form.get('confirm_password', '')

        if not user.check_password(current_password):
            flash('Password saat ini salah!', 'danger')
            return redirect(url_for('admin_account'))

        if new_username:
            user.username = new_username
            session['username'] = new_username

        if new_password:
            if new_password != confirm_password:
                flash('Konfirmasi password baru tidak cocok!', 'danger')
                return redirect(url_for('admin_account'))
            user.set_password(new_password)
            flash('Password berhasil diperbarui!', 'success')

        db.session.commit()
        flash('Pengaturan akun berhasil disimpan!', 'success')
        return redirect(url_for('admin_account'))

    return render_template('admin/account.html', user=user)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
